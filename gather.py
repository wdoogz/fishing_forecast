import requests
import json
import os
import datetime

def zip_to_geo(zipcode):
    exit_code = None
    locofile = "/tmp/geocodes/{}.json".format(zipcode)

    if os.path.exists(locofile):
        json_out = json.loads(open(locofile, "r").read())
        print(json_out)
    else:
        try:
            os.makedirs("/tmp/geocodes")
        except Exception as e:
            pass

        URL = "https://www.zipcodeapi.com/rest/YFel5D52qU9IQnlCK8obG7QmiEd3HF32jbj49eNu8vCOYR6ZfA3bRYa1SFxnvFpx/info.json/{}/degrees".format(zipcode)
        
        geo_co = requests.get(URL).json()
        
        city = geo_co["city"]
        lat = geo_co['lat']
        lng = geo_co['lng']

        dictionary = { 'city': city, 'lat': lat, 'lng': lng }
        jsontest = json.dumps(dictionary)

        with open(locofile, "w+") as f:
            f.write(jsontest)
            json_out = f.read()
            print(json_out)

    return json_out

def get_forecast(geoloco):
    todaydate = datetime.datetime.now()
    date = todaydate.strftime("%Y%m%d")
    URL = "https://api.solunar.org/solunar/{},{},{},-4".format(str(geoloco["lat"]), str(geoloco["lng"]), date)
    solunar_req = requests.get(URL).json()
    hourly_rating = solunar_req["hourlyRating"]
    print(json.dumps(hourly_rating, indent=4))

    for k in hourly_rating:
        rating = hourly_rating[k]
        if int(k) < 24:
            if int(rating) > 20:
                print(k, "Is a good day to time to fish!")
            else:
                print(k, "BAD Don't fish")


get_forecast(zip_to_geo(17856))
