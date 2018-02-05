#Import of necessary libararies

from tkinter import *
from pandastable import Table, TableModel
import requests
from bs4 import BeautifulSoup
import pandas as pd
from geopy.geocoders import Nominatim
geolocator = Nominatim()

#Function to input text

def printtext():
    global e
    string = e.get() 
    return string 

#Selectcity function
"""
first select the location according to input value
then by using geopy module convert into latttude and longitude and feed into website requeste
e.g.
create dictionary of varible as 'key':'value'

Extract seven_day with beautiful soup module with find attribute

Collect the data as Tonight, Periods, Short_descs, temp, descs and transform into dataframe as weather

Return Dataframe with condition of night only
"""
def selectcity():
    location = geolocator.geocode(printtext)
    latitude = location[1][0]
    longitude = location[1][1]
    payload = {'lat': latitude , 'lon': longitude}
    page = requests.get("http://forecast.weather.gov/MapClick.php?lat=latitude&lon=longitude",  params=payload)
    soup = BeautifulSoup(page.content, 'html.parser')
    seven_day = soup.find(id="seven-day-forecast")
    forecast_items = seven_day.find_all(class_="tombstone-container")
    tonight = forecast_items[0]
    period_tags = seven_day.select(".tombstone-container .period-name")
    periods = [pt.get_text() for pt in period_tags]
    short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
    temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
    descs = [d["title"] for d in seven_day.select(".tombstone-container img")]
    weather = pd.DataFrame({
        "period": periods, 
        "short_desc": short_descs, 
        "temp": temps, 
        "desc":descs
        })
    temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
    weather["temp_num"] = temp_nums.astype('int')
    is_night = weather["temp"].str.contains("Low")
    weather["is_night"] = is_night
    global Low_night
    Low_night = pd.DataFrame(weather[is_night])
    return Low_night


root = Tk()
#Message to display
msg = Message(root, text='Enter the address or zipcode or city name to see weather table')
msg.config(font=('times',14))
root.title('Name')

e = Entry(root)
e.pack()
e.focus_set()

class TestApp(Frame):
        """Basic test frame for the table"""        
        def __init__(self, parent=None):
            self.parent = parent
            Frame.__init__(self)
            self.main = self.master
            self.main.geometry('600x400+200+100')
            self.main.title('Table app')
            f = Frame(self.main)
            f.pack(fill=BOTH,expand=1)
            self.table = pt = Table(f, dataframe=selectcity("Austin"),
                showtoolbar=True, showstatusbar=True)
            pt.show()
            return



#Pack the message with tkinter
msg.pack()

b = Button(root,text='okay',command=printtext)
b.pack(side='bottom')
        
app = TestApp()
#launch the app
app.mainloop()