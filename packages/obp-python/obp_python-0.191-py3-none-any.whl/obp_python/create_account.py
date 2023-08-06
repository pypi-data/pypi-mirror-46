import requests
import os
import json

OBP_AUTH_TOKEN = os.getenv('OBP_AUTH_TOKEN')
OBP_API_HOST = os.getenv('OBP_API_HOST')
OBP_BANK_ID = os.getenv('OBP_BANK_ID')
OBP_ACCOUNT_ID = os.getenv('OBP_ACCOUNT_ID')
OBP_ACCOUNT_LABEL = os.getenv('OBP_ACCOUNT_LABEL')
OBP_ACCOUNT_TYPE = os.getenv('OBP_ACCOUNT_TYPE')
OBP_USER_ID = os.getenv('OBP_USER_ID')
OBP_CURRENCY = os.getenv('OBP_CURRENCY')
import pdb;pdb.set_trace()

def createAccount(OBP_AUTH_TOKEN=OBP_AUTH_TOKEN, OBP_API_HOST=OBP_API_HOST, OBP_BANK_ID=OBP_BANK_ID, OBP_ACCOUNT_ID=OBP_ACCOUNT_ID, OBP_USER_ID=OBP_USER_ID, OBP_ACCOUNT_LABEL=OBP_ACCOUNT_LABEL, OBP_ACCOUNT_TYPE=OBP_ACCOUNT_TYPE):

  payload = {
      "user_id": "",
      "label": "",
      "type": "CURRENT",
      "balance": {
        "currency": "EUR",
        "amount": "0"
      },
      "branch_id": "1234",
      "account_routing": {
        "scheme": "OBP",
        "address": "UK123456"
      }
    }
  
  payload['user_id'] = OBP_USER_ID
  payload['label'] = OBP_ACCOUNT_LABEL
  payload['type'] = str(OBP_ACCOUNT_TYPE)
  payload['balance']['currency'] = OBP_CURRENCY

  url = OBP_API_HOST + '/obp/v3.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}'.format(BANK_ID=OBP_BANK_ID, ACCOUNT_ID=OBP_ACCOUNT_ID)
  import pdb;pdb.set_trace()
  
  authorization = 'DirectLogin token="{}"'.format(OBP_AUTH_TOKEN)
  headers = {'Content-Type': 'application/json',
            'Authorization': authorization}
  req = requests.put(url, headers=headers, json=payload)

  if req.status_code == 201 or req.status_code == 200:
    return json.loads(req.text)
  else:
    return json.loads(req.text)

  print(req.text)
  return json.loads(req.text)

if __name__ == '__main__':
  createAccount(OBP_AUTH_TOKEN=OBP_AUTH_TOKEN, OBP_API_HOST=OBP_API_HOST, OBP_BANK_ID=OBP_BANK_ID, OBP_ACCOUNT_ID=OBP_ACCOUNT_ID, OBP_USER_ID=OBP_USER_ID, OBP_ACCOUNT_LABEL=OBP_ACCOUNT_LABEL, OBP_ACCOUNT_TYPE=OBP_ACCOUNT_TYPE)

