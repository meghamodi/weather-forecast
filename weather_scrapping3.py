try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv
from datetime import date, timedelta
import pandas as pd


# Function for encoding the list using utf-8
# def to_utf8(lst):
#     return [str(elem).encode('utf-8') for elem in lst]
# def to_utf8(lst):
#     try:
#         if type(lst) ==unicode:
#             return lst.encode('utf-8',ignore)
#     except:
#         return str(lst)

# Assign values
data_weather = pd.read_csv("/Users/meghamodi/Documents/Districtwise_India.csv",sep="\t")
df = data_weather[data_weather['Lat'].notna()]
df.Lat = df.Lat.astype(str)
df.Long = df.Long.astype(str)
for index, row in df.iterrows():
    district = row['District']
    days=5
    lat= row['Lat']
    lon= row['Long']
# district = 'Kolar'
# days=5
# lat='13.137'
# lon='78.134'
# #lat='12.9791'
#lon='77.5913'



    details=[]
    for i in range(days):
    	d = date.today() - timedelta(i)
    	quote_page="https://darksky.net/details/"+lat+','+lon+'/'+str(d)+"/us12/en"
    	#quote_page="https://darksky.net/details/13.137,78.134/2008-5-1/us12/en"

    	page = urlopen(quote_page)

    	soup = BeautifulSoup(page, "html.parser")

    	precipitation_box= soup.find(attrs={"class": "precipProbability"}).find(attrs={"class":"num swip"})
    	rain_box= soup.find(attrs={"class": "precipAccum swap"}).find(attrs={"class":"num swip"})
    	temp_box = soup.find(attrs={"class": "temperature"}).find(attrs={"class":"num"})
    	wind_box = soup.find(attrs={"class": "wind"}).find(attrs={"class":"num swip"})
    	pressure_box = soup.find(attrs={"class": "pressure"}).find(attrs={"class":"num swip"})
    	humidity_box = soup.find(attrs={"class": "humidity"}).find(attrs={"class":"num swip"})
    	dew_point_box = soup.find(attrs={"class": "dew_point"}).find(attrs={"class":"num"})


    	high_point_box = soup.find(attrs={"class":"highLowTemp swip"}).find(attrs={"class": "highTemp swip"}).find(attrs={"class": "temp"})
    	low_point_box = soup.find(attrs={"class":"highLowTemp swip"}).find(attrs={"class": "lowTemp swap"}).find(attrs={"class": "temp"})


    	mylist= [str(d),pressure_box.text,dew_point_box.text,humidity_box.text,temp_box.text,high_point_box.text.strip('/')[:2],low_point_box.text.strip('/')[:2],wind_box.text,precipitation_box.text,rain_box.text]

    	for i,val in enumerate(mylist):
    		if val=='???' or val=='-':
    			mylist[i]= 'No Data'

    	details.append(mylist)
    	print(mylist)


    a = u"\u00b0"

    header = ['Date','Pressure(mb)',"Dew Point("+a+')','Humidity(%)', 'Temperature('+a+')','Max Temp('+a+')','Min Temp('+a+')','Wind(mph)', 'Precipitation(%)', "Rain(in)"]

    filename = district+'.csv'


    with open(filename, 'w') as myfile:
        wr = csv.writer(myfile, lineterminator='\n')
        wr.writerow(header)
        wr.writerows(details)
