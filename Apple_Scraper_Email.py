
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import time
import smtplib
import csv
import sys
import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from config import from_email
from config import password
from config import api_key, user_name, email_url



def Apple_Scraper():

            
            response_email = requests.get(email_url, auth=(user_name, api_key))
            data=response_email.json()

            
            url = "https://showmojo.com/8dd2eea08f/listings/"

            response = get(url)

            html_soup = BeautifulSoup(response.text, "html.parser")
            type(html_soup)
            properties = html_soup.find_all("div", class_ = "iframeListing")
            print(len(properties))



            address = []
            info = []

            for element in properties:
                
                first_prop_address = element.find("div", class_ = "location").text
                first_prop_info = element.find("div", class_ = "info").text
                address.append(first_prop_address)
                info.append(first_prop_info)

            prop_df = pd.DataFrame({"Address": address,
                                   "Info" : info})
            proplist = []
            proplist.append(prop_df["Address"])
            proplist


            time.sleep(20)

            url1 = "https://showmojo.com/8dd2eea08f/listings/"
            response1 = get(url1)

            html_soup1 = BeautifulSoup(response1.text, "html.parser")
            type(html_soup1)
            properties1 = html_soup1.find_all("div", class_ = "iframeListing")
            prop_link1 = html_soup1.find_all("a", href=[])
            print(len(properties))

            address1 = []
            info1 = []

            for element1 in properties1:


                first_prop_address1 = element1.find("div", class_ = "location").text
                first_prop_info1 = element1.find("div", class_ = "info").text
                address1.append(first_prop_address1)
                info1.append(first_prop_info1)

            for a in prop_link1:
                first_prop_link1 = a.find("a", href=True)
                print(first_prop_link1)

            prop_df1 = pd.DataFrame({"Address": address1,
                                   "Info" : info1})
            proplist1 = []
            proplist1.append(prop_df1["Address"])



            finalprop = prop_df.join(prop_df1, lsuffix='a', rsuffix='b')


            old_list = finalprop["Addressa"].unique()
            new_list = finalprop["Addressb"].unique()
            nan_list = []
            compare_list=[]
            no_list = []
            final_list = []

    
            for element in new_list:

                element = str(element)
                if element == "nan":
                    nan_list.append(element)
                if element != "nan":
                    compare_list.append(element)


            for element in compare_list:
                if element not in old_list:
                    final_list.append(element)                  
                else:
                    no_list.append("NO")
            test = [x[10:-10] for x in final_list]



            if len(final_list) > 0:
                msg = [x for x in test]
            else:
                msg = "No New Listings"

            print(msg)

            # 2-6-2019 - Testing API calls for emails
            emails = []
            for x in data['members']:
                emails.append(x['email_address'])
            # hashed code below is from when we were using csv files for email storage
            # file = "contacts.csv"
            # peoplereader = pd.read_csv(file)
            # people1 = pd.DataFrame(peoplereader)

            # email = people1["Email Address"]
            # emails = emails.dropna()
           

            if len(no_list) < len(new_list):

                for email in emails:
       
        
                    if msg[0] != "N":
                        html = "We just listed the property at " + msg[0] + "!" + """                        <html>
                          <head></head>
                              <body>
                                <p>Ready to schedule your showing? Click the <a href="https://www.applerealty.com/for-rent">showing scheduler!</a>.
                                </p>
                                <p>Already found a place? Click this <a href="https://AppleRealty.us15.list-manage.com/unsubscribe?u=ef0682884d57cb58c340e9190&id=76de8932e9">unsubsubscribe link.</a>.
                                </p>
                              </body>
                            </html>
                            """ 
                        email = email
                       

                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(from_email, password)

                        msg1 = MIMEMultipart('alternative')
                        msg1['From'] = from_email
                        msg1['To'] = email
                        msg1['Subject'] = "Apple Listings Update"


                        part1 = MIMEText(html, 'html')
                        msg1.attach(part1)
                        server.sendmail(from_email, email, msg1.as_string())
                        server.quit()

                        return;


print("Program Running...")
while True:
    try:
        Apple_Scraper()
    except:
        print("Error...Restarting....")
        time.sleep(60)



