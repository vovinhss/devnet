from netmiko import ConnectHandler
import datetime as dt
from datetime import datetime
from datetime import date
import difflib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

Router1= {
		'device_type': 'cisco_ios',
		'ip': '192.168.177.10',
		'username': 'admin',
		'password': 'cisco',
		'secret': 'cisco',
		'verbose': False,
		}

Router2= {
		'device_type': 'cisco_ios',
		'ip': '192.168.177.20',
		'username': 'admin',
		'password': 'cisco',
		'secret': 'cisco',
		'verbose': False,
		}

all_routers=[Router1,Router2]
##create filename with date-month-year
current_time=datetime.now()
current_date=current_time.strftime("%d")
current_month=current_time.strftime("%m")
current_year=current_time.strftime("%Y")

#date,month,year of yesterday

yesterday = dt.date.today()-dt.timedelta(days=1)
yesterday_date=yesterday.strftime("%d")
yesterday_month=yesterday.strftime("%m")
yesterday_year=yesterday.strftime("%Y")
difference=""
#login to each router
for routers in all_routers:
	net_connect=ConnectHandler(**routers)
	net_connect.enable()

##Get hostname router
	get_hostname_router="show running-config | include hostname"
	GetHostName_command = net_connect.send_command_timing(get_hostname_router)
	hostname_router=GetHostName_command.split(" ")[1]

##set filename for backup file of today
	filename_today=hostname_router+"_"+current_date+"_"+current_month+"_"+current_year

#show run and store in file with name above
	running_cfg=net_connect.send_command_timing("show running-config")
	f=open(filename_today,'w')
	f.write(running_cfg)
	f.close()
##-------------Compare two file---------------## 
 #find filename yesterday
	yesterday_file = hostname_router+"_"+yesterday_date+"_"+yesterday_month+"_"+yesterday_year
	print(yesterday_file)
	filename_today=hostname_router+"_"+current_date+"_"+current_month+"_"+current_year
	print(filename_today)
 #Extract different between two files
	with open(yesterday_file, 'r') as old_file, open(filename_today, 'r') as new_file:
		difference += difflib.HtmlDiff().make_file(fromlines = old_file.readlines(), tolines = new_file.readlines(), fromdesc = 'Yesterday '+hostname_router, todesc = 'Today '+hostname_router)
##-----------SEND EMAIL TO ADMIN ABOUT DIFFERENT----------------#

fromaddr = 'vovinhss@gmail.com'
toaddr = 'vovinhss@gmail.com'

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'Daily Configuration Management Report '
msg.attach(MIMEText(difference, 'html'))

#Sending the email via Gmail's SMTP server on port 587
server = smtplib.SMTP('smtp.gmail.com', 587)

#SMTP connection is in TLS (Transport Layer Security) mode. All SMTP commands that follow will be encrypted.
server.starttls()

#Logging in to Gmail and sending the e-mail
server.login("vovinhss@gmail.com", "Trongvinh123")
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()

