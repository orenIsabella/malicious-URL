#!/usr/bin/env python

##############################################
# Author: Nitay Hason
# Fetch data from VirusTotal
##############################################

import pandas as pd
import requests
import time
import json
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-a','--apikey', help='API key for VirusTotal')
parser.add_argument('-i','--csv_in', help='URLs CSV input file')
parser.add_argument('-o','--json_out', help='JSON output file data')

args = parser.parse_args()
path = os.path.dirname(os.path.abspath(__file__))

api_key    = "89b62770b0861fda0dd038e8b651560b8e638e20b44416edb19ba743388b1479"#args.apikey
csv_in     = "../Datasets/urls/maliciousURLS2020.csv"#args.csv_in
json_out   = "../Datasets/urls/jsonTest/a.json"#args.json_out
error_file = '../Datasets/urls/jsonTest/vt_errors.json'

# vt_url     = 'https://www.virustotal.com/vtapi/v2/url/report'
vt_url     = 'https://www.virustotal.com/vtapi/v2/domain/report'
params     = {'apikey': api_key,'domain':'<domain>'}
df           = pd.read_csv(csv_in, sep=';', header=None, dtype=str)
domains_list = pd.DataFrame(df[0].unique())

vt         = {}
errors     = {}

urls       = domains_list[0]
len_urls   = len(urls)
i          = 0
remaining  = False

while(i<len_urls):
    save = False
    while(remaining):
        if not save:
            with open(json_out, 'w') as out:
                json.dump(vt, out, indent=4, sort_keys=True)
            with open(error_file, 'w') as out:
                json.dump(errors, out, indent=4, sort_keys=True)
            save = True
        time.sleep(60*5)
        response  = requests.get(vt_url, params=params)
        js        = response.json()
        remaining = (js['response_code'] == '204')

    url              = urls[i]
    print(url)
    print()
    params['domain'] = url
    response         = requests.get(vt_url, params=params)
    print(response)
    js               = response.json()
    print(js)
    if js['response_code'] == '204':
        remaining = True
        continue
    i+=1
    print(i, end=",", flush=True)
    vt[url] = js
    time.sleep(2)

with open(json_out, 'w') as out:
    json.dump(vt, out, indent=4, sort_keys=True)

with open(error_file, 'w') as out:
    json.dump(errors, out, indent=4, sort_keys=True)

print('Done')