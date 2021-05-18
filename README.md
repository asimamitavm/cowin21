The basic code is based on Django, Sqlite and python with little bit of SQL.

It allows users to submit a request to get notified about the future vaccine slots by providing the Pincode or the district name.
User gets a list of vaccine slots available in the 7 days.

This is basically a django appication which stores data on sqlite which means you dont have to provision a separate DB for this.
Scheduling of slot_check.py scripts can be done using crontab.

So on a small machine like t2-micro on AWS it can provide servie to multiple users.

Hope it helps someone in these challenging times.


