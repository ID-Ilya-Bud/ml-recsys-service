import requests
from datetime import datetime

# Делаем GET-запрос к эндпоинту /post/recommendations/ для user_id=200
response = requests.get(
    "http://127.0.0.1:8000/post/recommendations/",
    params={"user_id": 200, "dt": datetime.now(), "limit": 2},
)

print("Рекомендации для пользователя четным user_id [200]:")
print(response.json(), "\n")

### Output:
# Рекомендации для пользователя четным user_id [200]:
# [
#     {
#         "id": 2,
#         "text": "Aids and climate top Davos agenda\n\nClimate change and the fight against Aids are leading the list of concerns for the first day of the World Economic Forum in the Swiss resort of Davos.\n\nSome 2,000 business and political leaders from around the globe will listen to UK Prime Minister Tony Blairs opening speech on Wednesday. Mr Blair will focus on Africas development plans and global warming. Earlier in the day came an update on efforts to have 3 million people on anti-Aids drugs by the end of 2005. The World Health Organisation (WHO) said 700,000 people in poor countries were on life-extending drugs - up from 440,000 six months earlier but amounting to only 12% of the 5.8 million who needed them. A $2bn funding gap still stood in the way of hitting the 2005 target, the WHO said.\n\nThe themes to be stressed by Mr Blair - whose attendance was announced at the last minute - are those he wants to dominate the UKs chairmanship of the G8 group of industrialised states. Other issues to be discussed at the five-day conference range from Chinas\n\neconomic power to Iraqs future after this Sundays elections. Aside from Mr Blair, more than 20 other world leaders are expected to attend including French President Jacques Chirac - due to speak by video link after bad weather delayed his helicopter - and South African President Thabo Mbeki, whose arrival has been delayed by Ivory Coast peace talks. The Ukraines new president, Viktor Yushchenko, will also be there - as will newly elected Palestinian leader Mahmoud Abbas. Showbiz figures will also put in an appearance, from U2 frontman Bono - a well-known campaigner on trade and development issues - to Angelina Jolie, a goodwill campaigner for the UN on refugees.\n\nUnlike previous years, protests against the WEF are expected to be muted. Anti-globalisation campaigners have called off a demonstration planned for the weekend. At the same time, about 100,000 people are expected to converge on the Brazilian resort of Porto Alegre for the World Social Forum - the so-called anti-Davos for campaigners against globalisation, for fair trade, and many other causes.\n\nIn contrast, the Davos forum is dominated by business issues - from outsourcing to corporate leadership - with bosses of more than a fifth of the worlds 500 largest companies scheduled to attend. A survey published on the eve of the conference by PricewaterhouseCoopers said four in ten business leaders were very confident that their companies would see sales rise in 2005. Asian and American executives, however, were much more confident than their European counterparts. But the political discussions, focusing on Iran, Iraq and China, are likely to dominate media attention.\n",
#         "topic": "business",
#     },
#     {
#         "id": 4,
#         "text": "India power shares jump on debut\n\nShares in Indias largest power producer, National Thermal Power Corp (NTPC) have risen 13% on their stock market debut.\n\nThe governments partial sell-off of NTPC is part of a controversial programme to privatise state-run firms. The 865 million share offer, a mix of new shares and sales by the government, raised 54bn rupees($1.2bn). It was Indias second $1bn stock debut in three months, coming after the flotation by software firm Tata. The share offer was eleven times oversubscribed. It is a good investment bet, said Suhas Naik, an investment analyst from ING Mutual Fund. Power needs in India are set to rise and NTPC will benefit from that. Analysts say the success of the NTPC flotation would encourage the government to reduce stakes in more power companies. NTPC has said it will use the money from the share sale to feed the growing needs of the countrys energy-starved economy. The firm is the largest utility company in India, and the sixth largest power producer in the world.\n",
#         "topic": "business",
#     },
# ]
