import requests
import json
import mariadb
import sys
from pprintpp import pprint as pp

auth = json.load(open('credentials.json'))
munzAuth = json.load(open('munzcreds.json'))
# keys
user = auth["user"]
passwd = auth["pass"]
BearerToken = munzAuth["data"]["token"]["access_token"]

try:
    conn = mariadb.connect(
        user=user,
        password=passwd,
        host="localhost",
        port=3306,
        database="munz"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

r = requests.get("https://api.munzee.com/user/current", headers={"Authorization": BearerToken})
pp(r)
pp(r.text)

