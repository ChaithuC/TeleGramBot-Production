import smtplib
from csv import writer
from datetime import datetime
import pytz
import pandas as pd 


#declarations
email_address = 'nicecandy437@gmail.com'
email_password = 'vtkwqnnvvvnvsbpb'
mails = ['phinenice6@gmail.com' ,'221813601004@gitam.in', 'rvcharanchowdary7@icloud.com', 'pavansagar9010242946@gmail.com']
api = '5479313682:AAEsDiC_ZeYy0yB1OYqcfQOo4MmlMCVXP9w'



# send_mail
def Add_Subject_Message_Send(response,Entered_Number, selected_product, inputt, metric):    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(email_address, email_password)
            msg = response
            smtp.sendmail(email_address, mails, msg)
            print("Mails Sent!")
            appending_data_into_csv(Entered_Number, selected_product, inputt, metric)
            print("Data Appended!")


def appending_data_into_csv(Entered_Number, selected_product, inputt, metric):
  Number = Entered_Number
  Product = selected_product
  quantity = inputt + metric
  Address = None
  Customer_Data = None
  Order_Time = datetime.now(pytz.timezone('Asia/Kolkata'))
  
  with open("Order_records.csv", 'a', newline='') as f_object:
    row = [Number, Product, quantity, Address, Customer_Data, Order_Time]
    writer_object = writer(f_object)
    writer_object.writerow(row)  
    f_object.close()


# seeking for customer
def test(mobile_number):
  mobile_number = int(mobile_number)
  print(mobile_number)
  
  df = pd.read_csv("Customers.csv") 
  c = df.loc[df['mobile_number'] == mobile_number]
  if c.empty:
    print("Not data in Database Found")
  else:
    print("data in Database Found")
  return c
