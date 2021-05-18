import boto3,sqlite3

def verify_mail():
    con = sqlite3.connect("/home/ec2-user/cowin/db.sqlite3")
    curs = con.cursor()
    curs.execute("select distinct email from slots_slotrequest")
    mailids = curs.fetchall()
    print(mailids)
    ses_cl = boto3.client('ses',region_name = 'ap-south-1')
    lis = ses_cl.list_identities(IdentityType='EmailAddress')
    verified_ids = lis['Identities']
    print(f"verified ids are {verified_ids}")
    sent = []
    for row in mailids:
        print(f"checking for..... {row[0]}")
        if row[0] not in verified_ids:
            response = ses_cl.verify_email_address(EmailAddress=row[0])
            print(response)
            sent.append(row[0])
    print(sent)
    con.close()

if __name__ == "__main__":
    verify_mail()


