import requests
import sqlite3

url = 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51'}
con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

for num in range(1,38):
    new_url = url+str(num)
    res = requests.get(new_url,headers=headers)
    data = res.json()

    for i in data["districts"]:
        dist_id = i["district_id"]
        dist_name = i["district_name"]
        ins = f"INSERT INTO slots_district(district_name,district_id,state_id) values('{dist_name}',{dist_id},{num});"
        print(ins)
        cur.execute(ins)
        con.commit()

con.close()

