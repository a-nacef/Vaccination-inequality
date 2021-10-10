import os
import pandas as pd
import sys

#store this as config at some point
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

def _transform():
    df = pd.read_csv(path+'/staging/v-data_raw.csv')
    df2 = pd.read_csv(path+'/staging/gdp-data_raw.csv')
    prn_df = df[['location', 'date', 'total_vaccinations', 'people_vaccinated', 'daily_vaccinations_per_million']]
    final_df = prn_df.pivot_table(values, index=['location','date']).loc[Countries]
    final_df.fillna(0, inplace=True)
    final_df.to_csv(path+'/staging/v-data_transformed.csv')
    gdpdf = pd.merge(final_df.reset_index()['location'], df2[df2['Year']>=2019], how='inner', left_on = 'location', right_on = 'Entity').drop(columns=['Entity']).drop_duplicates().reset_index(drop=True)
    gdpdf.to_csv(path+'/staging/gdp-data.csv')
    
    

_transform()