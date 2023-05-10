import string
import json
from typing import Union
from fastapi import FastAPI, HTTPException
import pyhibp
from pyhibp import pwnedpasswords as pw
import redis

USER_AGENT = "hibp-microapi/0.0.1"
KEY_TIMEOUT = 604800 # 1 week

app = FastAPI()
con = redis.Redis(host='data', port=6379, decode_responses=True)

@app.post("/check/{hash}")
def read_hash(hash: str, q: Union[str, None] = None):
  hash = hash.upper()
  if not is_hex(hash):
    raise HTTPException(status_code=422, detail="Invalid SHA1 hash")
  if len(hash) != 40:
    raise HTTPException(status_code=422, detail="Hash must be 40 characters long")

  prefix = hash[0:5]
  suffix = hash[5:40]

  count = 0
  if len(con.keys(prefix + ":*")) > 0:
    count = con.get(prefix + ":" + suffix)
  else:
    pyhibp.set_user_agent(USER_AGENT)
    resp = pw.suffix_search(prefix)
    for res in resp:
      cnt = int(res.split(":")[1])
      con.setex(prefix + ":" + suffix, KEY_TIMEOUT, cnt)
      if res.startswith(suffix):
        count = cnt
  
  return {"hash": hash, "count": count}

def is_hex(s):
  hex_digits = set(string.hexdigits)
  return all(c in hex_digits for c in s)
