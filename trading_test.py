from random import random
import sched, datetime, influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token="v41RF2iR1PamA8O-wJ6K_L9mdiFTuVaNBFQLb3Zie4E3oJMHHjORxMUPrXcfciXbhwbtG2c2uDBKrPNzrYZDmA=="
org = "olga@solominov.com"
url = "https://europe-west1-1.gcp.cloud2.influxdata.com"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket="BUCKET"
write_api = client.write_api(write_options=SYNCHRONOUS)

tickers = [ ["ticker" + "0" + str(ticker), 0] if ticker < 10 else ["ticker" + str(ticker), 0] for ticker in range(0, 100) ]

for item in tickers:
    point = (
    Point("measurement")
    .tag("ticker", item[0])
    .field("price", item[1])
    )
    write_api.write(bucket=bucket, org="olga@solominov.com", record=point)


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement

s = sched.scheduler(time.monotonic, time.sleep)
def update_prices(lst, sc):
    for item in lst:
        cur_price = item[1] + generate_movement()
        item[1]=cur_price
        point = (
            Point("measurement")
            .tag("ticker", item[0])
            .field("price", item[1])
            )
        write_api.write(bucket=bucket, org="olga@solominov.com", record=point)
        s.enter(1, 1, update_prices, (tickers,sc))

s.enter(1, 1, update_prices, (tickers,s))
s.run()

