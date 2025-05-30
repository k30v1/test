import os
from urllib.request import urlopen, Request
from urllib.parse import urlencode,quote
import json



get_audience = lambda: json.load(urlopen("https://upload.pypi.org/_/oidc/audience"))["audience"]

if "GITHUB_ACTIONS" in os.environ:
    bearer = "Bearer " + os.environ["ACTIONS_ID_TOKEN_REQUEST_TOKEN"] # workflow must have permissions "id-token: write"
    url = os.environ["ACTIONS_ID_TOKEN_REQUEST_URL"]
    url += ("&" if "?" in url else "?") + "audience=" + get_audience()
    req = Request(url)
    req.add_header("Authorization", bearer)
    oidc_token = json.load(urlopen(req))["value"]
else:
    raise RuntimeError("unknown environment")

r = Request(
    url = "https://upload.pypi.org/_/oidc/mint-token",
    data = json.dumps({"token": oidc_token}).encode(),
    headers = {"Content-Type": "application/json", "Accept-encoding": "application/json"},
)
r = urlopen(r).read()
print(r)
pypi_api_token = json.load(r)
#pypi_api_token = json.load(urlopen(req))["token"]
