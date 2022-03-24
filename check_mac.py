from netmiko import ConnectHandler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Đọc file allmac sau đó
totalmac=[]
f=open('allmac.txt','r')
lines=f.readlines()
for i in range(0,len(lines)):
    totalmac+=[lines[i].rstrip()]

#khai báo 2 switch
sw_user1={
        		'device_type': 'cisco_ios',
        		'ip': '192.168.177.100',
        		'username': 'admin',
        		'password': 'cisco',
        		'secret': 'cisco',
        		'verbose': False,
}

"""sw_user2={
        		'device_type': 'cisco_ios',
        		'ip': '192.168.177.132',
        		'username': 'admin',
        		'password': 'cisco',
        		'secret': 'cisco',
        		'verbose': False,
}"""

#---------------------Viết hàm gửi mail-------------------#
def sendMail(output,dstMail):
    if(output!=''):
        msg = MIMEMultipart()
        msg['From'] = 'vovinhss@gmail.com'
        msg['To'] = dstMail
        msg['Subject'] = "NEW DEVICE JOIN NETWORK"
        msg.attach(MIMEText(output, 'plain'))
        text=msg.as_string()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
      
        server.login("vovinhss@gmail.com", "Trongvinh123")
        server.sendmail("vovinhss@gmail.com",dstMail,text)
        server.quit()
  
#------------------------Login vào switch và show mac---------------------------------#
output=''
all_switches=[sw_user1]
#all_switches=[sw_user1,sw_user2]
for switches in all_switches:
    net_connect=ConnectHandler(**switches)
    net_connect.enable()
    wr=net_connect.send_command_timing("show mac address-table")
    f=open('mactemp.txt','w')
    f.write(wr)
    f=open('mactemp.txt','r')
    linehai=f.readlines()
for i in range(0,len(linehai)):
    if("Et" in linehai[i]):
        mac=linehai[i].split("    ")[1].replace(" ","")
        port=linehai[i].split("    ")[3]
        vlan=linehai[i].split("    ")[0]
   
#------------------------So sánh với các MAC trong totalmac ban đầu---------------------------------#
#----------Neu khong co trong totalmac thì gửi mail--------------------#

    if (mac not in totalmac):
        output+="WARNING: New device found: "+mac+" on switch "+switches['ip']+" port "+port+" vlan "+vlan+"\n\n"
if(output!=''):
    sendMail(output,"yourgmail@gmail.com")
 