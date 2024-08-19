import requests
import json
import config

#API URL
url = config.vectocore["API_URL"]

# 조회
payload = json.dumps({
  "command": "extream_search",
  "index_name" : "naverx-keyword",
  "question" : "여름, 추석",
  "max_count" : "5"
})

# 생성
# payload = json.dumps({
#     "command": "list",
#     "type": "index"
# })

headers = {
  'x-api-key': config.vectocore["Tenant_Key"], #Tenant Key
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
response_to_json = json.loads(response.text)
  
# 결과 리스트
event_ids = [row['eventid'] for row in response_to_json['response']['result']]

print(event_ids)