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
head = {"Authorization": BearerToken}

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

r = requests.get("https://api.munzee.com/user/current", headers=head)
pp(r)
pp(r.json()["data"])

payload = '{"exclude":"","fields":"munzee_id,friendly_name,latitude,longitude,original_pin_image,proximity_radius_ft,creator_username", "points":{"box1":{"timestamp": 0,"lat2":39.928842,"lng1":-105.141754,"lng2":-105.147290,"lat1":39.925172}}}'
r = requests.post("https://api.munzee.com/map/boundingbox/", headers=head, data=payload)
pp(r)
pp(r.json()["data"])
