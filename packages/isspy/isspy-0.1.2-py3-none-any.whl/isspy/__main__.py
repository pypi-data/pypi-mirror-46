#!/usr/bin/python3

# libraries for open notify
import requests
import urllib3
import json
import http


#libraries for spot the station
import re
import feedparser
import time
from subprocess import check_output
import sys
import datetime

class ISSpy():
    """
    This class returns the next passes of the ISS.

    Changed default to the official Spot the Station RSS feed. 
    Open Notify seems to be incorrect.
    See https://github.com/open-notify/Open-Notify-API/issues/10

    https://spotthestation.nasa.gov/sightings/xml_files/Australia_Victoria_Melbourne.xml

    """


    def __init__(self, country="Australia", region="Victoria", city="Melbourne", ylat=-37, xlong=144):

        self.ylat = ylat
        self.xlong = xlong

        self.country=country
        self.region=region
        self.city=city

        self.http = urllib3.PoolManager()

    def get_passes(self):
        """
        Returns passes from Spot The Station (as a list) 
        """
        passes = []

        # Make URL an f-string and put in Country, region, city)
        url = f"https://spotthestation.nasa.gov/sightings/xml_files/{self.country}_{self.region}_{self.city}.xml"
        #url = "https://spotthestation.nasa.gov/sightings/xml_files/Australia_Victoria_Melbourne.xml"

        #print(url)
        feed = feedparser.parse(url)
        for post in feed.entries:
            
            #reg
            words = re.compile('\w+').findall(post.summary)
            
            # List is usually 29 words per passover.
            # 31 words if duration of ISS is below 1 minute.
            # Therefore it ignores all cases below 1 minute.
            # Potential work around, include offset in process passes. 
            if len(words) == 29:
                passes.append(self.process_passes(words))
        
        return passes

    def process_passes(self, pass_info, offset=0):
        """
        This processes the list of words and inserts them into a dictionary.
        """
        
        dic = {}
        if pass_info[0] != "Date":
            raise ValueError("The following solution is outdated and thus this library broken. OH NOES! ")

        # Get DateTime
        # converts list to string
        date_pass = ' '.join(str(e) for e in pass_info[1:10])

        #Strips br and Time from string
        date_pass = date_pass.replace("br Time ", "")
        dic["datetime"] = datetime.datetime.strptime(date_pass, "%A %b %d %Y %I %M %p")

        dic["duration"] = int(pass_info[12])
        dic["elevation"] = int(pass_info[17])
        dic["approach_elev"] = int(pass_info[20]) 
        dic["approach_dir"] = pass_info[22]
        dic["departure_elev"] = int(pass_info[25])
        dic["departure_dir"] = pass_info[27]

        #print(dic)
        return dic
    
    def get_location(self):
        """
        TO DO
        """
        addr = "http://api.open-notify.org/iss-now.json"
        
        r = self.http.request('get', addr)

        obj = json.loads(r.data.decode('utf-8'))

    def get_next_pass_ON(self):
        """
        TO DO
        """
        addr = f"http://api.open-notify.org/iss-pass.json?lat={self.ylat}&lon={self.xlong}"

        r = self.http.request('get', addr)

        obj = json.loads(r.data.decode('utf-8'))

        passes = obj['response']
        return passes


if __name__ == "__main__":

    country = "Australia"
    region = "New_South_Wales"
    city = "Sydney"

    xlat = -37
    ylong = 144
    x = ISSpy(country,region,city)
    #x.get_next_pass()
    print(x.get_passes())
                
