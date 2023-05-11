#!/usr/bin/env python
import sys
from urllib import request
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
    req = request.Request(url)
    resp = request.urlopen(req)
    return resp.read()

if __name__ == '__main__':
    prefixes = []
    for v in range(0x0, 0xF + 1):
        for w in range(0x0, 0xF + 1):
            for x in range(0x0, 0xF + 1):
                for y in range(0x0, 0xF + 1):
                    for z in range(0x0, 0xF + 1):
                        prefixes.append(
                            format(v, 'X') +
                            format(w, 'X') +
                            format(x, 'X') +
                            format(y, 'X') +
                            format(z, 'X')
                        )
    process_pool = Pool(threads)
    run_operations(make_request, prefixes, process_pool)
