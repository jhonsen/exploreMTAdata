import requests
import pandas as pd
import json

import csv

def main():
    #google API token
    GOOG_API_KEY="PUT_API_KEY_HERE"

    #read subway station geo codes from https://catalog.data.gov/dataset/subway-stations
    subways=pd.read_csv("./data/DOITT_SUBWAY_STATION_01_13SEPT2010.csv")
    subways['the_geom']=subways.the_geom.str[7:-1]
    coord_list=subways['the_geom']

    # find the address of subway stations using google place API and then write results to CSV
    with open('./data/subwayszip.csv', 'w', newline='') as f:
        writer=csv.writer(f, delimiter=',')
        writer.writerow(["name", "zipcode", "lat", "long"])
        for coord in coord_list:
            coords=coord.split(' ') # split coordinates to long and lat coordinates
            #construct google place API with geo coordinates
            URL="https://maps.googleapis.com/maps/api/place/textsearch/json?hasNextPage=true&location="+coords[1]+","+coords[0]+"&radius=10&types=subway_station&key="+GOOG_API_KEY

            r=requests.get(URL, headers={})
            #if request is success, then write out first result's name and address to csv
            if (r.status_code==200):
                jsonData=r.json()
                name=jsonData['results'][0]['name']
                address=jsonData['results'][0]['formatted_address']
                writer.writerow([name, address, coords[1], coords[0]])

main()
