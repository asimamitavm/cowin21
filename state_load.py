import requests
import sqlite3

url = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51'}

res = requests.get(url,headers=headers)
data = res.json()
con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

for i in data["states"]:
    st_id = i["state_id"]
    st_name = i["state_name"]
    ins = f"INSERT INTO slots_state(state_name,state_id) values('{st_name}',{st_id});"
    print(ins)
    cur.execute(ins)
    con.commit()

con.close()

