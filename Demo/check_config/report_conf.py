from netmiko import ConnectHandler
import datetime as dt
from datetime import datetime
from datetime import date
import difflib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv
import secure


now = str(datetime.now().strftime("%Y-%m-%d %H:%M")) #%Y-%m-%d, %H:%M:%S
print(now)
router_num = 1 # Count node number

success = 0  
fail = 0
#Creat file name with date-month-year
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
with open('my_backup.csv', 'a', newline='') as f:
    write = csv.writer(f)
    with open('ip.txt') as routers:
        for ip in routers:
            print('Backing up configuration R'+ str(router_num) + ' ' + ip)
            print('.....')
            print(' ')
            R = {
                'device_type':'cisco_ios',
                'ip':ip,
                'username':'admin',
                'password':'cisco',
                'secret':'cisco'
            }
            try:
                #Connect to Devices
                ssh = ConnectHandler(**R)  
                ssh.enable()
                position = ssh.find_prompt() #=> SW1 
                #backup file
                """router_name=position[:-1]   #  -> SW1     
                filename = router_name + '.txt'"""
                #BackUp Data
                get_hostname_router = ssh.send_command_timing('show running-config | include hostname')
                GetHostName_command = ssh.send_command_timing(get_hostname_router)
                hostname_router=get_hostname_router.split(" ")[1]
                print(hostname_router)
                filename_today=hostname_router+"_"+current_date+"_"+current_month+"_"+current_year
                running_cfg=ssh.send_command_timing("show running-config")
                f=open(f"D:\LVTN\Demo\check_config\\backup_config\{filename_today}",'w')
                f.write(running_cfg)
                f.close()

                #Compare Config 
                yesterday_file = hostname_router+"_"+yesterday_date+"_"+yesterday_month+"_"+yesterday_year
                print(yesterday_file)
                filename_today=hostname_router+"_"+current_date+"_"+current_month+"_"+current_year
                print(filename_today)
                with open(f"backup_config/{yesterday_file}", 'r') as old_file, open(f"backup_config/{filename_today}", 'r') as new_file:
                    difference += difflib.HtmlDiff().make_file(fromlines = old_file.readlines(), tolines = new_file.readlines(), fromdesc = 'Yesterday '+hostname_router, todesc = 'Today '+hostname_router)

            except:
                print('~ Backup failed !!! , check error in file backup_error.log ~')
                print('\n')
                
                #write in log file
                with open("backup_error.log", 'a') as logf:
                    logf.write('Backup Failed on ')
                    logf.write(now)
                    logf.write(" - Cannot connect via SSH or Telnet to SW")
                    logf.write(str(router_num))
                    logf.write(' ')
                    logf.write(ip)
                    logf.write('\n')
                router_name = 'Router' + str(router_num)
                ##write.writerow([router_name, router_num, ip, 'failed', now])

                fail += 1
                router_num += 1 
                
                #continue       
            
            """with open(f"backupFiles/{filename}", "w") as log_file:
                log_file.write("#"*26)
                log_file.write(' DATE: '+ now + ' ')
                log_file.write("#"*26 + '\n')
                log_file.write(show_run)
            print('~ Successful !! ~')
            print('\n')"""
            write
            ##write.writerow([sw_name, router_num, ip, 'successful', now])
            router_num += 1
            success += 1
        
        write.writerow(['Hosts', 'Status','Count' 'Date'])
        write.writerow([router_num - 1, 'successful', success, now])
        write.writerow([router_num - 1, 'failed', fail, now])

        print('*'*35+' DONE!!! '+'*'*35)
        print("-> Successful:",success)
        print("-> Failed:",fail)

# #Mail Service
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
server.login(secure.user_gmail, secure.pass_gmail)
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()
    