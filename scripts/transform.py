import os
import pandas as pd


Countries = ['World', 'Asia', 'Africa', 'Europe', 
             'France', 'Italy', 'Spain', 'Germany', 'United Kingdom', 'Russia', 'Scotland', 'Norway', 'Belgium',
             'United States', 'Canada', 'Mexico', 'Brazil', 
             'Zimbabwe', 'South Africa', 'Morocco', 'Algeria', 'Tunisia',
             'Taiwan', 'Hong Kong', 'India', 'Thailand', 'Sri Lanka', 'Japan', 'South Korea', 'Vietnam', 'Indonesia', 'Australia',
             'Qatar', 'Bahrain', 'Israel', 'Turkey',
             'Low income', 'High income', 'Upper middle income', 'Lower middle income' 
            ]



def _transform():
    df = pd.read_csv('v_data.csv')
    