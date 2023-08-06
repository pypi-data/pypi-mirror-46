import sys
import gi

from datetime import datetime, timezone
from lifxlan import LifxLAN
from iss_notifer import ISSNotify
from gi.repository import Notify

gi.require_version('Notify', '0.7')



def utc_to_local(utc_dt):
        pass
        #return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=11)

def raiseNotify(time):
        Notify.init("ISS_Notify")
        print(time)
        time = time.strftime("%D %H:%M:%S")
        Hello = Notify.Notification.new("ISS Notifier", f"The ISS will be passing at this time {time}", "dialog-information")
        Hello.show()

def main():

        #lifx = lifxLAN(1)
        #devices = lifx.get_lights()
        
        ylat = -37              
        xlong = 144

        iss = ISSNotify(ylat, xlong)
        passes = iss.get_next_pass()

        for i in passes:
                
                nextrise = i['risetime']
                 
                # TO DO
                # Find a more elegant solution to change from utc to AEST  
                # 
                # Adds 11 hour time difference multiplied by 60 minutes *
                # multiplied again by 60 seconds onto unix time (in seconds)  

                nextrise = nextrise + 11 * 60 * 60 
                nextrise = datetime.fromtimestamp(nextrise)


                raiseNotify(nextrise)
if __name__ == "__main__":
        main()
        pass