import smtplib
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import python_html_font_for_mail
import os
from db import engine


env_path = './config.env'
load_dotenv(dotenv_path=env_path)


async def send_cardAssociation_mail(sender, receiver, sender_password, firstName, cardName, cardContent):



    from_address = sender
    to_address = receiver

    message = MIMEMultipart('Foobar')
    message['Subject'] = 'Wireless Task Tracker Card Association Mail'
    message['From'] = from_address
    message['To'] = to_address
    html = "Hi {} You has been added to the card : {}.\n\n Your work will be\n\n Content : {}".format(
        firstName, cardName, cardContent)
    content = MIMEText(html, 'plain')
    message.attach(content)

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(sender, sender_password)
    mail.sendmail(from_address, to_address, message.as_string())
    mail.close()


async def send_user_logo_upload_mail(sender, receiver, sender_password, firstName,
                               UserLogo):


    from_address = sender
    to_address = receiver

    message = MIMEMultipart('Notification')
    message['Subject'] = 'Wireless Task Tracker'
    message['From'] = from_address
    message['To'] = to_address
    code = "Hi {}, User avatar Logo updated successfully.".format(firstName)
    sub_code = "\nThank you for being customer of Wireless Task Tracker. All the notifications will be send to you regarding your tasks"
    sub_message = "\nYour avatar Logo\n\n "
    credentials = "\n UserLogo :<br><br>\n\n"
    userLogo = MIMEImage(UserLogo)
    print("UserLogo", type(UserLogo))
    splitline = "-"* 120
    dont_reply = "This is an auto generated mail, please Don't reply for this mail, reply mails won't be viewed"
    html = """\
    <html>
      <head>
      </head>
      <body>
        <h1><font color= "black">{code}</font></h1>\n<br>
        <h2><font color= "black">{sub_code}</font></h2>\n<br>
        <h3><font color= "black">{sub_message}</font></h3>\n<br>
        <h3>{credentials}</h3>\n
        <h3>{userLogo}</h3>\n
       <br><br><br>
        <h3>{splitline}</h3>\n
        <h4>{dont_reply}</h4>\n
        </p>
      </body>
    </html>
    """.format(**locals())
    content = MIMEText(html, 'html')
    message.attach(content)

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(sender, sender_password)
    mail.sendmail(from_address, to_address, message.as_string())
    mail.close()


async def send_card_edit_mail(sender, receiver, sender_password, firstName,cardName,function):


    from_address = sender
    to_address = receiver

    message = MIMEMultipart('Notification')
    message['Subject'] = 'Wireless Task Tracker'
    message['From'] = from_address
    message['To'] = to_address
    if function == 'edit' or function == 'Edit' or function == 'EDIT':
        code = "Hi {}, User card has been edited, please visit card to finish the task.".format(firstName)
        cardName = "Your edited card name is {}".format(cardName)
    elif function == 'delete' or function == 'Delete' or function == 'DELETE':
        code = "Hi {}, User card has been deleted, please visit deleted list to confirm".format(firstName)
        cardName = "Your deleted card name is {}".format(cardName)
    sub_code = "\nThank you for being customer of Wireless Task Tracker. All the notifications will be send to you regarding your tasks"
    splitline = "-"* 120
    dont_reply = "This is an auto generated mail, please Don't reply for this mail, reply mails won't be viewed"
    html = """\
    <html>
      <head>
      </head>
      <body>
        <h1><font color= "black">{code}</font></h1>\n<br>
        <h2><font color= "black">{sub_code}</font></h2>\n<br>
        <br>
        <h2><font color= "black">{cardName}</font></h2>\n<br>
       <br><br><br>
        <h3>{splitline}</h3>\n
        <h4>{dont_reply}</h4>\n
        </p>
      </body>
    </html>
    """.format(**locals())
    content = MIMEText(html, 'html')
    message.attach(content)

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(sender, sender_password)
    mail.sendmail(from_address, to_address, message.as_string())
    mail.close()


async def aws_send_email_with_attachment(sender, receiver, firstName, UserName, Password):

    msg = MIMEMultipart()
    msg["Subject"] = "𝕎𝕚𝕣𝕖𝕝𝕖𝕤𝕤 𝕋𝕣𝕒𝕔𝕜𝕖𝕣"
    msg["From"] = sender
    msg["To"] = receiver

    code = "Hi {}, User SignIn has been successfully done.".format(firstName)
    sub_code = "\n𝙏𝙝𝙖𝙣𝙠 𝙮𝙤𝙪 𝙛𝙤𝙧 𝙗𝙚𝙞𝙣𝙜 𝙘𝙪𝙨𝙩𝙤𝙢𝙚𝙧 𝙤𝙛 𝙒𝙞𝙧𝙚𝙡𝙚𝙨𝙨 𝙏𝙖𝙨𝙠 𝙏𝙧𝙖𝙘𝙠𝙚𝙧. 𝘼𝙡𝙡 𝙩𝙝𝙚 𝙣𝙤𝙩𝙞𝙛𝙞𝙘𝙖𝙩𝙞𝙤𝙣𝙨 𝙬𝙞𝙡𝙡 𝙗𝙚 𝙨𝙚𝙣𝙙 𝙩𝙤 𝙮𝙤𝙪 𝙧𝙚𝙜𝙖𝙧𝙙𝙞𝙣𝙜 𝙮𝙤𝙪𝙧 𝙩𝙖𝙨𝙠𝙨."
    sub_message = "\nYour Login Credentials will be\n\n "
    credentials = "\n UserName : {} \n\n<br> Password : {}".format(UserName, Password)
    splitline = "-" * 220
    dont_reply = "𝘛𝘩𝘪𝘴 𝘪𝘴 𝘢𝘯 𝘢𝘶𝘵𝘰 𝘨𝘦𝘯𝘦𝘳𝘢𝘵𝘦𝘥 𝘮𝘢𝘪𝘭, 𝘱𝘭𝘦𝘢𝘴𝘦 𝘋𝘰𝘯'𝘵 𝘳𝘦𝘱𝘭𝘺 𝘧𝘰𝘳 𝘵𝘩𝘪𝘴 𝘮𝘢𝘪𝘭, 𝘳𝘦𝘱𝘭𝘺 𝘮𝘢𝘪𝘭𝘴 𝘸𝘰𝘯'𝘵 𝘣𝘦 𝘷𝘪𝘦𝘸𝘦𝘥"
    html = python_html_font_for_mail.usersignIn.format(**locals())
    content = MIMEText(html, 'html')
    part = MIMEImage(open('wirelesslogo.png', 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename='wirelesslogo.png')
    msg.attach(part)
    msg.attach(content)

    # Convert message to string and send
    client = boto3.client('ses', aws_access_key_id=os.environ.get("ACCESS_KEY"),
                          aws_secret_access_key=os.environ.get("SECRET_KEY"))
    response = client.send_raw_email(
        Source=sender,
        Destinations=[receiver],
        RawMessage={"Data": msg.as_string()}
    )
    print(response)


async def aws_send_cardAssociation_mail(sender, receiver, firstName, cardName, cardContent):
    msg = MIMEMultipart()
    msg["Subject"] = "𝕎𝕚𝕣𝕖𝕝𝕖𝕤𝕤 𝕋𝕣𝕒𝕔𝕜𝕖𝕣"
    msg["From"] = sender
    msg["To"] = receiver

    code = "Hi {}, This is Card Association Notification.".format(firstName)
    sub_code = "\n𝙏𝙝𝙖𝙣𝙠 𝙮𝙤𝙪 𝙛𝙤𝙧 𝙗𝙚𝙞𝙣𝙜 𝙘𝙪𝙨𝙩𝙤𝙢𝙚𝙧 𝙤𝙛 𝙒𝙞𝙧𝙚𝙡𝙚𝙨𝙨 𝙏𝙖𝙨𝙠 𝙏𝙧𝙖𝙘𝙠𝙚𝙧. 𝘼𝙡𝙡 𝙩𝙝𝙚 𝙣𝙤𝙩𝙞𝙛𝙞𝙘𝙖𝙩𝙞𝙤𝙣𝙨 𝙬𝙞𝙡𝙡 𝙗𝙚 𝙨𝙚𝙣𝙙 𝙩𝙤 𝙮𝙤𝙪 𝙧𝙚𝙜𝙖𝙧𝙙𝙞𝙣𝙜 𝙮𝙤𝙪𝙧 𝙩𝙖𝙨𝙠𝙨."
    sub_message = "\nHi {} Your has been Associated to the card    : <b>{} </b>\n\n ".format(firstName,cardName)
    splitline = "-" * 220
    dont_reply = "𝘛𝘩𝘪𝘴 𝘪𝘴 𝘢𝘯 𝘢𝘶𝘵𝘰 𝘨𝘦𝘯𝘦𝘳𝘢𝘵𝘦𝘥 𝘮𝘢𝘪𝘭, 𝘱𝘭𝘦𝘢𝘴𝘦 𝘋𝘰𝘯'𝘵 𝘳𝘦𝘱𝘭𝘺 𝘧𝘰𝘳 𝘵𝘩𝘪𝘴 𝘮𝘢𝘪𝘭, 𝘳𝘦𝘱𝘭𝘺 𝘮𝘢𝘪𝘭𝘴 𝘸𝘰𝘯'𝘵 𝘣𝘦 𝘷𝘪𝘦𝘸𝘦𝘥"
    content = "<font color= 'black'><b>Content</b></font> : {} .....".format(cardContent[0:50])
    html = python_html_font_for_mail.cardAssociation.format(**locals())
    content = MIMEText(html, 'html')
    part = MIMEImage(open('wirelesslogo.png', 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename='wirelesslogo.png')
    msg.attach(part)
    msg.attach(content)

    # Convert message to string and send
    client = boto3.client('ses', aws_access_key_id=os.environ.get("ACCESS_KEY"),
                          aws_secret_access_key=os.environ.get("SECRET_KEY"))
    response = client.send_raw_email(
        Source=sender,
        Destinations=[receiver],
        RawMessage={"Data": msg.as_string()}
    )
    print(response)


def aws_summary_attachment(sender,receiver,firstName,UserName):
    msg = MIMEMultipart()
    msg["Subject"] = "𝕎𝕚𝕣𝕖𝕝𝕖𝕤𝕤 𝕋𝕣𝕒𝕔𝕜𝕖𝕣"
    msg["From"] = sender
    msg["To"] = receiver

    code = "Hi {}, Your Task summary mail.".format(firstName)
    sub_code = "\nThank you for being customer of Wireless Task Tracker. All the notifications will be send to you regarding your tasks"
    sub_message = "\nTill now summary of cards assign to you\n\n "
    credentials = "\n Card Names : {} \n\n<br>".format(UserName)
    splitline = "-"* 220
    dont_reply = "𝘛𝘩𝘪𝘴 𝘪𝘴 𝘢𝘯 𝘢𝘶𝘵𝘰 𝘨𝘦𝘯𝘦𝘳𝘢𝘵𝘦𝘥 𝘮𝘢𝘪𝘭, 𝘱𝘭𝘦𝘢𝘴𝘦 𝘋𝘰𝘯'𝘵 𝘳𝘦𝘱𝘭𝘺 𝘧𝘰𝘳 𝘵𝘩𝘪𝘴 𝘮𝘢𝘪𝘭, 𝘳𝘦𝘱𝘭𝘺 𝘮𝘢𝘪𝘭𝘴 𝘸𝘰𝘯'𝘵 𝘣𝘦 𝘷𝘪𝘦𝘸𝘦𝘥"
    html = """\
    <html>
      <head>
      </head>
      <body>
        <h2><font color= "black">{code}</font></h2>\n<br>
        <h3><font color= "black">{sub_message}</font></h3>\n<br>
        <h3>{credentials}</h3>\n
       <br><br>
       <h3><font color= "black">{sub_code}</font></h3>\n<br>
       <br><br><br>
        <h3>{splitline}</h3>\n
        <h4>{dont_reply}</h4>\n
        </p>
      </body>
    </html>
    """.format(**locals())
    content = MIMEText(html, 'html')
    part = MIMEImage(open('wirelesslogo.png', 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename='wirelesslogo.png')
    msg.attach(part)
    msg.attach(content)

    # Convert message to string and send
    client = boto3.client('ses',aws_access_key_id=os.environ.get("ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("SECRET_KEY"))
    response = client.send_raw_email(
        Source=sender,
        Destinations=[receiver],
        RawMessage={"Data": msg.as_string()}
    )
    print(response)


def generate_summary():
    query = "SELECT userId,cardContent, GROUP_CONCAT(cardId) FROM user_card GROUP BY userId"
    connection = engine.connect()
    result = connection.execute(query)
    qsummary = list(result)
    userId = []
    cards_allocated = []
    for rec in qsummary:
        userId.append(rec[0])
        cards_allocated.append(rec[2])
    __summary = list(zip(userId,[eval(str(x)) for x in cards_allocated]))
    email_list = []
    for user in __summary:
        email_list.append(get_email(user[0])[0][0])
    card_list = []
    for card in __summary:
        card_list.append(list(zip(_get_cardContent(card[1][0],card[1][1]))))
    for email in email_list:
        for card in card_list:
            aws_summary_attachment('engineerdheeraj97@gmail.com',email,"Dheeraj Kumar",card)


def get_email(userid):
    query = "SELECT emailId from user where userId = %s"
    connection = engine.connect()
    result = connection.execute(query,userid)

    return list(result)


def _get_cardContent(cardid1,cardid2):
    query1 = "SELECT cardName from card where cardId = %s"
    connection = engine.connect()
    result1 = connection.execute(query1,cardid1)
    query2 = "SELECT cardName from card where cardId = %s"
    connection = engine.connect()
    result2 = engine.execute(query2,cardid2)
    return list(result1)[0],list(result2)[0]


async def __mfa_authenticator__(mobile):
    client = boto3.client('sns', aws_access_key_id=os.environ.get("ACCESS_KEY"),
                          aws_secret_access_key=os.environ.get("SECRET_KEY"))
    otp = __generate_otp()
    client.publish(
        PhoneNumber="+91"+mobile,
        Message="Your OTP for password updation : {}".format(otp)
    )

    file = open("mfaCode.env", "w")
    file.write("\nmfaCode={}".format(otp))
    file.close()
    return otp



def __generate_otp():
    import math, random
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP




from os import path
if not path.exists('wirelesslogo.png'):
    s3 = boto3.client('s3', aws_access_key_id=os.environ.get("ACCESS_KEY"),
                              aws_secret_access_key=os.environ.get("SECRET_KEY"))
    s3.download_file('wirelesstracker', 'wireless_logo', 'wirelesslogo.png')
else:
    print("Logo already in directory")
    pass


def summary(count=0):
    while True:
        count +=1
        import time
        _seconds_per_hour_ = 3600
        _hours_per_day_ = 24
        time.sleep(_seconds_per_hour_*_hours_per_day_)
        generate_summary()
        print("Task summary sent",count)

# summary()
