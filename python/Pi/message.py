import ssl,smtplib,csv,imghdr

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from optparse import OptionParser
from email.mime.application import MIMEApplication

#location of the .csv file containing a row of addresses
file = "/home/pi/Sand 3D Printer Monitor System/python/Pi/rx_addresses.csv"

rows = []

PORT = 465

smtp_server = "smtp.gmail.com"
sender_email = 'youremail@gmail.com' #Enter your address
password = 'YOURPASSWORD'

context = ssl.create_default_context()

def sendMessage(message):
    with open(file, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

    print(rows[0])
    receiver_email = rows[0]
    #receiver_email = 'mattkday00@gmail.com'

    try:
        with smtplib.SMTP_SSL(smtp_server, PORT, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except:
        print("error")
