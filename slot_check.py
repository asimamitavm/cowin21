import json
import requests
import sqlite3
from datetime import datetime
from verify import verify_mail
import boto3
from botocore.exceptions import ClientError

def pin_slots():
    con = sqlite3.connect("/home/ec2-user/cowin/db.sqlite3")
    curs = con.cursor()
    curs.execute("select email,pin,date from slots_slotrequest where processed = 'NO' and pin is not NULL")
    request_list = curs.fetchall()
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode="
    for req in request_list:
        mail = req[0]
        pincode = req[1]
        x   = datetime.strptime(req[2],'%Y-%m-%d')
        dt = x.strftime('%d-%m-%Y')
        url_new = url+str(pincode)+str("&date=")+str(dt)
        print(f"URL is {url_new}")
        html = apicall(url_new)
        if len(html) != 0:
            sendSES(mail,html)
            curs.execute(f"UPDATE slots_slotrequest set processed =  'YES' where pin = {pincode} and email = {mail}")
    con.close()

def dist_slots():
    con = sqlite3.connect("/home/ec2-user/cowin/db.sqlite3")
    curs = con.cursor()
    curs.execute("select email,district_id,date from slots_slotrequest where processed = 'NO' and pin is NULL")
    request_list = curs.fetchall()
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="
    for req in request_list:
        mail = req[0]
        distcode = req[1]
        # date =  req[2]
        x   = datetime.strptime(req[2],'%Y-%m-%d')
        dt = x.strftime('%d-%m-%Y')
        url_new = url+str(distcode)+str("&date=")+str(dt)
        print(f"URL is {url_new}")
        html = apicall(url_new)
        if len(html) != 0:
            sendSES(email,html)
            curs.execute(f"UPDATE slots_slotrequest set processed =  'YES' where district_id = {distcode} and email = {mail}")
    con.close()

def apicall(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    res = requests.get(url,headers=headers)
    data = json.loads(res.text)
    center_list = data["centers"]
    #print(center_list)
    HTML = f"""<html>
    <head>
    </head>
    <body>
    <h2> Currently below slots are available. </h2>
        <hr>
        <table style ='font-family: arial, sans-serif;width: 100%; cellpadding="0" cellspacing="0'>
            <tr:nth-child(even) style = 'background-color: #dddddd;'>
                <th style = 'border: 1px solid #dddddd;text-align: left;padding: 8px;'>Center name</th>
                <th style = 'border: 1px solid #dddddd;text-align: left;padding: 8px;'>District</th>
                <th style = 'border: 1px solid #dddddd;text-align: left;padding: 8px;'>Pincode</th>
                <th style = 'border: 1px solid #dddddd;text-align: left;padding: 8px;'>Date</th>
                <th style = 'border: 1px solid #dddddd;text-align: left;padding: 8px;'>Min_age_limit</th>
                <th style = 'border: 1px solid #dddddd;text-align: left;padding: 8px;'>Available_capacity</th>
            </tr> """
    if len(center_list) != 0:
        for center in center_list:
            for sess in center['sessions']:
                HTML =   HTML + f"""<tr:nth-child(even) style = 'background-color: #dddddd;'>
                <td style = 'border: 1px solid #dddddd;text-align:left;padding: 8px;'>{center['name']}</td>
                <td style = 'border: 1px solid #dddddd;text-align:left;padding: 8px;'>{center['district_name']}</td>
                <td style = 'border: 1px solid #dddddd;text-align:left;padding: 8px;'>{center['pincode']}</td>
                <td style = 'border: 1px solid #dddddd;text-align:left;padding: 8px;'>{sess['date']}</td>
                <td style = 'border: 1px solid #dddddd;text-align:left;padding: 8px;'>{sess['min_age_limit']}</td>
                <td style = 'border: 1px solid #dddddd;text-align:left;padding: 8px;'>{sess['available_capacity']}</td></tr>"""
        HTML = HTML + """ </table> </body> </html> """
    else:
        HTML = """"""
    return HTML

def sendSES(RECIPIENT,BODY_HTML):
    """ Check if the mail id is verified, else send verification mail, if verified already, send the slots details"""

    ses_cl = boto3.client('ses',region_name = 'ap-south-1')
    lis = ses_cl.list_identities(IdentityType='EmailAddress')
    verified_ids = lis['Identities']
    if RECIPIENT in verified_ids:
    
        SUBJECT = "Vaccine Slots available"
        CHARSET = "UTF-8"
        SENDER = "asimamitavm@gmail.com"
        client = boto3.client('ses', region_name='ap-south-1')

        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
    else:
        response = ses_cl.verify_email_address(EmailAddress=RECIPIENT)


verify_mail()
pin_slots()
dist_slots()

#text = apicall('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=512&date=31-03-2021')
#f1 = open("tenor.txt","w")
#f1.write("this is tenor")
#f1.write("\n")
#f1.write("and something else")
#f1.close()
#print(ret)
#print(text)
#sendSES('asimamitavm@gmail.com',text)
#print(text)


