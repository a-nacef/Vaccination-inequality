import requests
import os



def _extract():
    try:
        v_data = requests.get("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv")
    except requests.exceptions.ConnectionError:
        print("err")
    except requests.exceptions.RequestException:
        print("err") 
    print(v_data.content)
    with open('v_data.csv', 'wb') as f:
        f.write(v_data.content)


_extract()