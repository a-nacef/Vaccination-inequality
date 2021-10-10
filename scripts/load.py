import psycopg2
import pandas as pd
import os



def _load():
    conn = psycopg2.connect("user='postgres' dbname='vaccination_inequality_proj'")
    curr = conn.cursor()
    print(os.environ['VPATH']+'staging/v-data_transformed.csv')
    try:
   #     curr.execute(f"""COPY dimvax(location, day, daily_total, total, daily_per_million)
                        #FROM '{os.environ['VPATH']+'staging/v-data_transformed.csv'}'
                        #DELIMITER ','
                        #CSV HEADER; 
                        #""") 
     curr.execute(f"""COPY dimgdp(name, year, gdppc)
                        FROM '{os.environ['VPATH']+'staging/gdp-data.csv'}'
                        DELIMITER ','
                        CSV HEADER; 
                        """) 

    except psycopg2.Error as e:
        print(e.args)
    conn.commit()
    conn.close()


_load()

                

    