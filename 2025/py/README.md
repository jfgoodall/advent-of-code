# Advent of Code 2024 Solutions
https://adventofcode.com/2024

## Dependencies
```bash
$ python -m pip install -r requirements.txt
```

## `pre-commit` Installation
```bash
$ pre-commit install
$ pre-commit run --all-files
```
## Fetch Puzzle Input
* Log into https://adventofcode.com in a browser and look up the value string of the session cookie
* Create a file `session.cookie` in the repo root director with the following contents:
```json
{ "session": "<value>" }
```
* Run the `get-input.py` script:
```bash
$ ./get-input.py [day=current_day] [year=current_year]
```

## Set Exec Bit for `git` in WSL
```bash
$ git update-index --chmod=+x 'scriptname.ext'
```
