import os
import pickle
from datetime import datetime
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from fastapi import FastAPI
from loguru import logger

from database import postgres_connection
from schema import PostGet


# === Вспомогательные функции ===
def load_sql(query: str, dtypes: Dict[str, Any] = None) -> pd.DataFrame:
    """
    Выполняет SQL-запрос через соединение postgres_connection и возвращает DataFrame.

    Аргументы:
        query: SQL-запрос
        dtypes: словарь типов колонок для pd.read_sql (по умолчанию None)

    Возвращает:
        pd.DataFrame с результатом запроса

    Исключения:
        RuntimeError, если произошла ошибка при выполнении запроса
    """
    conn = postgres_connection()

    try:
        df = pd.read_sql(query, conn, dtype=dtypes)
    except Exception as e:
        raise RuntimeError(
            f"❌ Ошибка при выполнении SQL-запроса: {e}\nЗапрос: {query}"
        ) from e
    finally:
        conn.close()

    return df


def load_model(model_path: str = "model.pkl"):
    """
    Загружает ML-модель из pickle-файла.

    Если код запускается в LMS-окружении (IS_LMS=1),
    путь берётся из переменной окружения MODEL_PATH.
    Иначе используется локальный путь, переданный пользователем.

    Исключения:
        FileNotFoundError — если файл модели не найден.
        RuntimeError — если произошла ошибка при загрузке модели.
    """
    if os.environ.get("IS_LMS", "0") == "1":
        model_path = os.environ["MODEL_PATH"]

    logger.info(f"Загрузка модели из файла {model_path}...")

    try:
        with open(model_path, "rb") as file:
            model = pickle.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ Файл модели не найден: {model_path}")
    except Exception as e:
        raise RuntimeError(f"❌ Ошибка при загрузке модели: {e}") from e

    logger.success("Модель успешно загружена")

    return model


def load_features(path: str) -> pd.DataFrame:
    try:
        df = pd.read_pickle(path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"❌ Файл с признаками не найден: {path}. "
            f"Похоже, признаки не пересчитаны — см. datacon.ipynb"
        )
 
    return df


# === Загрузка основных ресурсов ===
logger.info("Инициализация сервиса...")

# Создаём объект FastAPI
app = FastAPI()

# Загружаем модель в память
model = load_model()

# TODO: загрузите сохранённые признаки пользователей из БД
user_features = load_features("user_features.pkl")

# TODO: загрузите сохранённые признаки постов из БД
post_features = load_features("post_features.pkl")

post_text_raw = load_sql(query="SELECT post_id, text, topic FROM public.post_text_df")
post_text_raw = post_text_raw.rename(columns={'post_id': 'id'})

logger.success("Сервис успешно инициализирован")


# Эндпойнт для получения рекомендаций
@app.get("/post/recommendations/", response_model=List[PostGet])
def recommended_posts(user_id: int, dt: datetime, limit: int = 10) -> List[PostGet]:
    hour = dt.hour
    dayofweek = dt.weekday()
    is_weekend = int(dayofweek in (5, 6))

    user_row = user_features[user_features['user_id'] == user_id]

    if user_row.empty:
        top_posts = post_features.head(limit)
        top_posts = top_posts.rename(columns={'post_id': 'id'})
        top_posts = top_posts[['id']].merge(post_text_raw, on='id', how='left')
        posts_dict = top_posts[['id', 'text', 'topic']].to_dict(orient='records')
        recs = [PostGet(**post) for post in posts_dict]
        return recs

    user_row = user_row.iloc[0]

    X = post_features.copy()

    for col in user_features.columns:
        if col == 'user_id':
            continue
        X[col] = user_row[col]

    X['user_id'] = user_id
    X['hour'] = hour
    X['dayofweek'] = dayofweek
    X['is_weekend'] = is_weekend
    last_seen_at = pd.to_datetime(user_row['last_seen_at'])
    X['hours_of_last_action'] = (dt - last_seen_at).total_seconds() / 3600

    feature_columns = ['user_id', 'post_id', 'hour', 'dayofweek', 'is_weekend', 'hours_of_last_action', 'gender', 'age', 'country', 'city', 'exp_group', 'os', 'source', 'n_views', 'n_likes', 'like_rate', 'topic', 'text_len', 'text_words', 'post_ctr']

    X_model_input = X[feature_columns]

    predictions = model.predict_proba(X_model_input)[:, 1]
    X['pred_proba'] = predictions

    top_posts = X.sort_values('pred_proba', ascending=False).head(limit)
    top_posts = top_posts.rename(columns={'post_id': 'id'})

    top_posts = top_posts[['id']].merge(post_text_raw, on='id', how='left')

    posts_dict = top_posts[['id', 'text', 'topic']].to_dict(orient='records')
    recs = [PostGet(**post) for post in posts_dict]

    return recs