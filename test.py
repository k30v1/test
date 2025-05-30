import os
from urllib.request import urlopen, Request
import json

get_audience = lambda: json.load(urlopen("https://upload.pypi.org/_/oidc/audience"))["audience"]

if "GITHUB_ACTIONS" in os.environ: # do "Trusted publishing"
    url = os.environ["ACTIONS_ID_TOKEN_REQUEST_URL"] # workflow must have permissions "id-token: write"
    bearer = "Bearer " + os.environ["ACTIONS_ID_TOKEN_REQUEST_TOKEN"]
    req = Request(f"{url}?audience={get_audience()}")
    req.add_header("Authorization", bearer)
    oidc_token = json.load(urlopen(req))["value"]
    print('o',len(oidc_token))
