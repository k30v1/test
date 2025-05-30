import os
from urllib.request import Request

password = None

if password is None and "GITHUB_ACTIONS" in os.environ:
  req = Request(os.environ["ACTIONS_ID_TOKEN_REQUEST_URL"]) # workflow must have "id-token: write"
  req.add_header("Authorization", f'Bearer {os.environ["ACTIONS_ID_TOKEN_REQUEST_TOKEN"]}')
  print(req)
