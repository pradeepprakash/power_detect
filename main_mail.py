import smtplib
import getopt, sys

def mail_func(on_off):
   
   smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
   smtp_server.ehlo()
   smtp_server.starttls()
   smtp_server.login('from.name@someemail.com', '<password_here>')
   
   pwr_event = on_off
   msg = 'From: "From_Name" <from.name@someemail.com>\nSubject:<Power State [' + str(pwr_event) + ']'
   print msg
   ### WORKING #####
   smtp_server.sendmail('from.name@someemail.com', 'to.name@someemail.com', msg)
   smtp_server.quit()
   print('Email sent successfully')
