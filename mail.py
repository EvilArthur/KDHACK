import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import from_email, password
from platform import python_version

msg = MIMEMultipart('alternative')

to_email = 'l0tus0rb@yandex.ru'
message = 'Сообщение сделано при помощи python'
msg['To'] = 'l0tus0rb@yandex.ru'
msg['Subject'] = 'Тема письма'
msg['From'] = 'GosUslugiKids <KDhack2021@yandex.ru>'
msg['Reply-To'] = from_email
msg['Return-Path'] = from_email
msg['X-Mailer'] = 'Python/' + (python_version())


html = '<html><head></head><body><p>' + message + '</p></body></html>'
msg.attach(MIMEText(message, 'plain'))
msg.attach(MIMEText(html, 'html'))


server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
server.login(from_email, password)
server.sendmail(from_email, to_email, msg.as_string())
server.quit()
