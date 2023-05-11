import string
import json

from fastapi import FastAPI, HTTPException
import pyhibp
from pyhibp import pwnedpasswords as pw

USER_AGENT = "hibp-microapi/0.0.1"

app = FastAPI()

@app.post("/check/{hash_prefix}")
def read_hash_prefix(hash_prefix: str):
  hash_prefix = hash_prefix.upper()
  if not is_hex(hash_prefix):
    raise HTTPException(status_code=422, detail="Invalid SHA1 hash prefix")
  if len(hash_prefix) != 5:
    raise HTTPException(status_code=422, detail="Hash prefix must be 5 characters long")
  
  pyhibp.set_user_agent(USER_AGENT)
  obj = []
  for res in pw.suffix_search(hash_prefix):
    suffix,count = res.split(":")
    obj.append({"hash": hash_prefix + suffix, "count": int(count)})

  return obj

def is_hex(s):
  hex_digits = set(string.hexdigits)
  return all(c in hex_digits for c in s)
