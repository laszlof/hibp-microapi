import string
import json
import os

from fastapi import FastAPI, HTTPException
import pyhibp
from pyhibp import pwnedpasswords as pw
import redis

USER_AGENT = "hibp-microapi/0.0.1"

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_KEY_TIMEOUT = os.getenv('REDIS_KEY_TIMEOUT', 604800) # 1 week

if REDIS_HOST is None:
  raise Exception("REDIS_HOST must be defined.")

app = FastAPI()
con = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.post("/check/{hash_prefix}")
def read_hash_prefix(hash_prefix: str):
  hash_prefix = hash_prefix.upper()
  if not is_hex(hash_prefix):
    raise HTTPException(status_code=422, detail="Invalid SHA1 hash prefix")
  if len(hash_prefix) != 5:
    raise HTTPException(status_code=422, detail="Hash prefix must be 5 characters long")

  res = con.get(hash_prefix)
  if res != None:
    return json.loads(res)
  
  pyhibp.set_user_agent(USER_AGENT)
  obj = []
  for res in pw.suffix_search(hash_prefix):
    suffix,count = res.split(":")
    obj.append({"hash": hash_prefix + suffix, "count": int(count)})

  json_out = json.dumps(obj)
  con.setex(hash_prefix, REDIS_KEY_TIMEOUT, json_out)

  return obj

def is_hex(s):
  hex_digits = set(string.hexdigits)
  return all(c in hex_digits for c in s)
