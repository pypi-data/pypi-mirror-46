# ISSpy

## Introduction

This project began when I wanted to illuminate or flash my LED lightglobe when the International Space Station (ISS) was approaching. However, the only python library I could find was Open Notify and it was not accurate^1 when compared to NASA's Spot The Station. This is a wrapper that provides an interface for Spot The Station. 

^1 https://github.com/open-notify/Open-Notify-API/issues/10 

## Installation

There is no backwards capability with python2. Please use python3 if you want to use this library. 

> pip install isspy

## Usage

This library uses both Spot The Station & Open Notify. By default, it uses Spot the Station for pass location. However you can change this and use Open Notify if you desire.  

    country = "Australia"
    region = "Victoria"
    city = "Melbourne"

    passes = ISSpy(country, region, city)

    #Returns list of passes as a dictionary
    print(x.get_passes())

    #expected output
    [{'datetime': datetime.datetime(2019, 4, 20, 19, 14), 
      'duration': 1, 
      'elevation': 17, 
      'approach_elev': 11, 
      'approach_dir': 'N', 
      'departure_elev': 17,
      'departure_dir': 'NNE'}] 
## Future

Open-Notify also provides the current location of the ISS and the people aboard. I will incorporate this at a later date. 