#!/usr/bin/env python
import sys
from urllib.request import urlopen
from multiprocessing import Pool

if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " <url>")
    print("Example URL: http://localhost")
    exit(1)

url_base = sys.argv[1] + "/check/"
threads = 100

def run_operations(operation, input, pool):
    pool.map(operation, input)

def make_request(prefix):
    url = url_base + prefix
    with urlopen(url) as resp:
      return resp.read()

def generate_prefixes():
    i = 0
    while i < 16**5:
        yield f"{i:05X}"
        i += 1

if __name__ == '__main__':
    process_pool = Pool(threads)
    run_operations(make_request, list(generate_prefixes()), process_pool)
