import requests
import os

#store this as config at some point
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _extract():
    try:
        v_data = requests.get("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv")
    except requests.exceptions.ConnectionError:
        print("err")
    except requests.exceptions.RequestException:
        print("err") 
    with open(path+'/staging/v-data_raw.csv', 'wb') as f:
        f.write(v_data.content)


_extract()