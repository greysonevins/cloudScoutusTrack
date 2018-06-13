import smtplib
import os

# Gmail Sign In
def sendEmail(header, text):
    TO = os.environ["EMAIL"]
    SUBJECT =  header
    TEXT = text

    gmail_sender = os.environ["EMAIL"]
    gmail_passwd = os.environ["GMAIL_PASS"]

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)
    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except Exception as e:
        print(e)
        print ('error sending mail')

    server.quit()

