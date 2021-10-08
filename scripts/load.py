import psycopg2
import pandas as pd



def _load():
    conn = psycopg2.connect("user='postgres' dbname='vaccination_inequality_proj'")
    curr = conn.cursor()
    


_load()

                

    