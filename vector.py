import requests
import json

#API URL
url = "https://58wq5zhhc1.execute-api.ap-northeast-2.amazonaws.com/Dev/api"

# 조회
payload = json.dumps({
  "command": "extream_search",
  "index_name" : "naverx-keyword",
  "question" : "여름, 럭셔리",
  "max_count" : "5"
})

# 생성
# payload = json.dumps({
#     "command": "list",
#     "type": "index"
# })

headers = {
  'x-api-key': '9874c49a-6513-4243-a155-4b6be050c11b', #Tenant Key
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
response_to_json = json.loads(response.text)
for row in response_to_json['response']['result']:
    print(row['eventid'])