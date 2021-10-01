import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import from_email, password

msg = MIMEMultipart()

to_email = 'l0tus0rb@yandex.ru'
message = 'Сообщение сделано при помощи python'

msg.attach(MIMEText(message, 'plain'))

server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
server.login(from_email, password)
server.sendmail(from_email, to_email, msg.as_string())
server.quit()
