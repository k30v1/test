import os
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json



import requests
get_audience = lambda: json.load(urlopen("https://upload.pypi.org/_/oidc/audience"))["audience"]
#get_audience = lambda: requests.get("https://upload.pypi.org/_/oidc/audience").json()["audience"]

if "GITHUB_ACTIONS" in os.environ:
    url = os.environ["ACTIONS_ID_TOKEN_REQUEST_URL"] # workflow must have permissions "id-token: write"
    bearer = "Bearer " + os.environ["ACTIONS_ID_TOKEN_REQUEST_TOKEN"]
    url += "?" + urlencode({"audience":get_audience()})
    #req = Request(url)
    #req.add_header("Authorization", bearer)
    #r = urlopen(req)
    #r = r.read().decode()
    #print(r)
    #oidc_token = json.loads(r)["value"]
    
    r = requests.get(url, params={"audience": get_audience()}, headers={"Authorization": bearer})
    print(r.text)
    oidc_token = r.json()["value"]
    
    print('o',len(oidc_token))
else:
    raise RuntimeError("unknown environment")

import requests
r = requests.post(
    "https://upload.pypi.org/_/oidc/mint-token",
    json={'token': oidc_token},
    timeout=5,  # S113 wants a timeout
)
print(len(r.text), r.text)
