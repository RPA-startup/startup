import requests
import json
import config

def search_events(question):
    # 벡터 API 호출
    url = config.vectocore["API_URL"]
    payload = json.dumps({
        "command": "extream_search",
        "index_name": "naverx-keyword",
        "question": question,
        "max_count": "5"
    })
    
    headers = {
      'x-api-key': config.vectocore["Tenant_Key"], # Tenant Key
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_to_json = json.loads(response.text)
    
    # 결과에서 eventid 리스트를 추출
    event_ids = [row['eventid'] for row in response_to_json['response']['result']]
    return event_ids
