import requests
import csv

# constants
AUTHORIZATION_URL = 'https://www.zooplus.de/tierarzt/api/v2/token?debug=authReduxMiddleware-tokenIsExpired'
FILENAME = "result.csv"
my_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "sec-sh-ua": '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    "sec-sh-ua-mobile": '?0',
    'Referer': 'https://www.zooplus.de/'
    }

number_of_contact = int(input('Set a number of contacts: '))
DATA_URL = f'https://www.zooplus.de/tierarzt/api/v2/results?animal_99=true&page=1&from=0&size={number_of_contact}'
data_set = []

session = requests.Session()

session.headers.update(my_headers)
response = session.get(AUTHORIZATION_URL)
raw_token = response.json()
session.headers.update({'authorization': f'Bearer {raw_token["token"]}'})
response_2 = session.get(DATA_URL)

for item in response_2.json()['results']:
    temp_dict = {}
    temp_dict['name_feature'] = item['name']
    temp_dict['work_time'] = item['open_time']
    temp_dict['rating'] = item['avg_review_score']
    temp_dict['address'] = f"{item['address']}\n{item['zip']}\n{item['city']}"
    data_set.append(temp_dict)

with open(FILENAME, "w", newline='', encoding='UTF-8') as file:
    columns = ['name_feature', 'work_time', 'rating', 'address']
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(data_set)
