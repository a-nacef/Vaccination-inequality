import requests
import os
import psycopg2
import pandas as pd
import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Countries = ['World', 'Asia', 'Africa', 'Europe', 
             'France', 'Italy', 'Spain', 'Germany', 'United Kingdom', 'Russia', 'Scotland', 'Norway', 'Belgium',
             'United States', 'Canada', 'Mexico', 'Brazil', 
             'Zimbabwe', 'South Africa', 'Morocco', 'Algeria', 'Tunisia',
             'Taiwan', 'Hong Kong', 'India', 'Thailand', 'Sri Lanka', 'Japan', 'South Korea', 'Vietnam', 'Indonesia', 'Australia',
             'Qatar', 'Bahrain', 'Israel', 'Turkey',
             'Low income', 'High income', 'Upper middle income', 'Lower middle income' 
            ]

values = ['location', 'date', 'total_vaccinations', 'people_vaccinated', 'daily_vaccinations_per_million']


def _extract():
    try:
        v_data = requests.get("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv")
    except requests.exceptions.ConnectionError:
        print("err")
    except requests.exceptions.RequestException:
        print("err") 
    with open(path+'/vax-dbrd/staging/v-data_raw.csv', 'wb') as f:
        f.write(v_data.content)

def _transform():
    df = pd.read_csv(path+'/vax-dbrd/staging/v-data_raw.csv')
    prn_df = df[['location', 'date', 'total_vaccinations', 'people_vaccinated', 'daily_vaccinations_per_million']]
    final_df = prn_df.pivot_table(values, index=['location','date']).loc[Countries]
    final_df.fillna(0, inplace=True)
    final_df.to_csv(path+'/vax-dbrd/staging/v-data_transformed.csv')

def _load():
    conn = psycopg2.connect("user='postgres' dbname='vaccination_inequality_proj'")
    curr = conn.cursor()
    print(os.environ['VPATH']+'/vax-dbrd/staging/v-data_transformed.csv')
    try:
        curr.execute("""DELETE FROM dimvax_staging WHERE location is not null """)
        curr.execute(f"""COPY dimvax_staging(location, day, daily_per_mil, daily_total, total)
                        FROM '{os.environ['VPATH']+'/vax-dbrd/staging/v-data_transformed.csv'}'
                        DELIMITER ','
                        CSV HEADER; 
                        """)
        conn.commit() 
        curr.execute("""
            INSERT INTO dimvax(location, day, daily_per_mil, daily_total, total) 
                (SELECT * FROM dimvax_staging)
                 ON CONFLICT ON CONSTRAINT dimvax_uq DO UPDATE SET
                 daily_total = EXCLUDED.daily_total,
                 total = EXCLUDED.total,
                 daily_per_mil = EXCLUDED.daily_per_million
        """)
    
    except psycopg2.Error as e:
        print(e.args)
    conn.commit()
    conn.close()

