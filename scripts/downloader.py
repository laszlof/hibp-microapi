#!/usr/bin/env python
import sys
import json
from multiprocessing import Pool
import pyhibp
from pyhibp import pwnedpasswords as pw

threads = 100

USER_AGENT = "hibp-microapi-downloader/0.0.1"
OUTPUT_DIR = "../public"

def run_operations(operation, input, pool):
    pool.map(operation, input)

def make_request(prefix):
    pyhibp.set_user_agent(USER_AGENT)
    obj = []
    for res in pw.suffix_search(prefix):
        suffix,count = res.split(":")
        obj.append({"hash": prefix + suffix, "count": int(count)})
    with open(OUTPUT_DIR + "/" + prefix, 'w') as f:
        json.dump(obj, f, indent=2)

def generate_prefixes():
    i = 0
    while i < 16**5:
        yield f"{i:05X}"
        i += 1

if __name__ == '__main__':
    process_pool = Pool(threads)
    run_operations(make_request, list(generate_prefixes()), process_pool)
