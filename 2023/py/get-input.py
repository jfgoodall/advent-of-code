#!/usr/bin/env python
"""
Usage: get-input.py <day> [<year> default: current year]

Requires a session.cookie file (json) with one entry that looks like:
    { "session": "<value" }
"""
import datetime
import json
import sys

import requests

today = datetime.date.today()
day = today.day
year = today.year

if len(sys.argv) == 2:
    day = int(sys.argv[1])
elif len(sys.argv) == 3:
    day = int(sys.argv[1])
    year = int(sys.argv[2])
elif len(sys.argv) > 3:
    raise TypeError("Usage: get-input.py <day> [<year> default: current year]")

URL = f"https://adventofcode.com/{year}/day/{day}/input"
FILE = f"day{day:02}-input.dat"

with open("session.cookie") as cookie_file:
    cookies_json = cookie_file.read()
cookies_dict = json.loads(cookies_json)
cookies = requests.utils.cookiejar_from_dict(cookies_dict)

response = requests.get(URL.format(day), cookies=cookies)
response.raise_for_status()

with open(f"day{day:02}-input.dat", "wb") as outfile:
    outfile.write(response.content)
