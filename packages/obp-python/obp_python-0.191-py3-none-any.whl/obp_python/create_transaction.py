import requests
import os
import json

OBP_AUTH_TOKEN = os.getenv('OBP_AUTH_TOKEN')
OBP_API_HOST = os.getenv('OBP_API_HOST')
OBP_BANK_ID = os.getenv('OBP_BANK_ID')
OBP_ACCOUNT_ID = os.getenv('OBP_ACCOUNT_ID')
OBP_CURRENCY = os.getenv('OBP_CURRENCY')
OBP_TRANSACTION_AMOUNT = os.getenv('OBP_TRANSACTION_AMOUNT')
OBP_TRANSACTION_DESCRIPTION = os.getenv('OBP_TRANSACTION_DESCRIPTION')

def createTransaction(OBP_API_HOST=OBP_API_HOST):


  url = OBP_API_HOST + '/obp/v3.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transaction-request-types/SANDBOX_TAN/transaction-requests'.format(BANK_ID=OBP_BANK_ID, ACCOUNT_ID=OBP_ACCOUNT_ID, VIEW_ID='owner')

  authorization = 'DirectLogin token="{}"'.format(OBP_AUTH_TOKEN)
  headers = {'Content-Type': 'application/json',
            'Authorization': authorization}
  payload = {
  "to": {
    "bank_id": "bnpp-irb.01.dz.dz",
    "account_id": "TestThree"
  },
  "value": {
    "currency": "EUR",
    "amount": "10"
  },
  "description": "this is for work"
  }

  payload['to']['bank_id'] = OBP_BANK_ID
  payload['to']['account_id'] = OBP_ACCOUNT_ID
  payload['value']['currency'] = OBP_CURRENCY
  payload['value']['amount'] = str(OBP_TRANSACTION_AMOUNT)
  payload['description'] = OBP_TRANSACTION_DESCRIPTION


  req = requests.post(url, headers=headers, json=payload)
  import pdb;pdb.set_trace()
  if req.status_code == 201 or req.status_code == 200:
    return json.loads(req.text)
  else:
    return json.loads(req.text)


if __name__ == '__main__':
  print(createTransaction(OBP_API_HOST=OBP_API_HOST))
  
