import os
from urllib.request import urlopen, Request
import json

get_audience = lambda: json.load(urlopen("https://upload.pypi.org/_/oidc/audience"))["audience"]

if "GITHUB_ACTIONS" in os.environ:
    url = os.environ["ACTIONS_ID_TOKEN_REQUEST_URL"] # workflow must have permissions "id-token: write"
    bearer = "Bearer " + os.environ["ACTIONS_ID_TOKEN_REQUEST_TOKEN"]
    req = Request(f"{url}?audience={get_audience()}")
    req.add_header("Authorization", bearer)
    oidc_token = json.load(urlopen(req))["value"]
    print('o',len(oidc_token))
else:
    raise RuntimeError("unknown environment")

url = "https://upload.pypi.org/_/oidc/mint-token"
data = json.dumps({"token": oidc_token}).encode()
pypi_token = json.load(urlopen(url, data))["token"]
print(pypi_token[:10])
print(111, len(pypi_token))
