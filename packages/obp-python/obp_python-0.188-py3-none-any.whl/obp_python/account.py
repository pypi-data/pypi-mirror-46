import requests
import os
import json

OBP_AUTH_TOKEN = os.getenv('AUTH_TOKEN', False)
OBP_API_HOST = os.getenv('OBP_API_HOST', False)

def getMyAccounts(OBP_AUTH_TOKEN=OBP_AUTH_TOKEN, OBP_API_HOST=OBP_API_HOST):


  url = OBP_API_HOST + '/obp/v3.1.0/my/accounts'

  authorization = 'DirectLogin token="{}"'.format(OBP_AUTH_TOKEN)
  headers = {'Content-Type': 'application/json',
            'Authorization': authorization}
  req = requests.get(url, headers=headers)

  if req.status_code == 201 or req.status_code == 200:
    return json.loads(req.text)
  else:
    return json.loads(req.text)

  print(req.text)
  return json.loads(req.text)

if __name__ == '__main__':
  #OBP_AUTH_TOKEN = os.getenv('OBP_AUTH_TOKEN', input("OBP_AUTH_TOKEN -->"))
  #OBP_API_HOST = os.getenv('OBP_API_HOST', input("OBP_API_HOST -->"))
  print(getMyAccounts(OBP_AUTH_TOKEN=OBP_AUTH_TOKEN, OBP_API_HOST=OBP_API_HOST))

