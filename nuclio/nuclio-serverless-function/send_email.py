import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def mail_content_prepare(pdf_name, bucket_name):
    mail_content = """Hello,
This is a mail from Nuclio Serverless function. Somebody uploaded <{}> file to the <{}> bucket.
Thank You
""".format(pdf_name, bucket_name)
    return mail_content

def send_to_gmail(pdf_name, bucket_name):
    #The mail addresses and password
    sender_address = ''
    sender_pass = ''
    receiver_address = ''
    
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = f"Somebody uploaded <{pdf_name}> file"   #The subject line
    
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content_prepare(pdf_name, bucket_name), 'plain'))
    
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

