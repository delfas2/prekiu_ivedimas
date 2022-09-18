# from typing import Container
from ast import Index
import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine



@st.cache(allow_output_mutation=True)
def get_data():
    return []

database_username = 'user'
database_password = 'Password'
database_ip       = '192.168.1.112:8457'
database_name     = 'dwh'

st.header('Prekių įvedimas į duomenų bazę')


db_connection_str = 'mysql+pymysql://user:Password@192.168.1.112:8457/dwh'
db_connection = create_engine(db_connection_str)

df_prekes = pd.read_sql('SELECT `Prekės pavadinimas` FROM dwh.dim_prekes', con=db_connection)
df_parduotuves = pd.read_sql('SELECT Parduotuvė FROM dwh.dim_parduotuves', con=db_connection)



data = st.date_input('Pirkimo data:')

parde=st.radio('Nauja parduotuvė?',('Esanti', 'Nauja'))
if parde == "Nauja":
    parduotuve = st.text_input('Parduotuvė:')
else:
    parduotuve=st.selectbox('Parduotuvė:', df_parduotuves)

prek=st.radio('Nauja prekė?',('Esanti', 'Nauja'))
if prek == "Nauja":
    pavadinimas = st.text_input('Prekės pavadinimas:', '')
else:
    pavadinimas = st.selectbox('Prekės pavadinimas:', df_prekes)

kiekis = st.number_input('Kiekis:', step=0.01)
kaina = st.number_input('Kaina:', step=0.01)
nuolaida = st.number_input('Nuolaida:', step=0.01)
    

if st.button('Įrašyti'):
    df = pd.DataFrame({"Data": data, 
                    "Parduotuvė":parduotuve, 
                    "Prekės pavadinimas": pavadinimas, 
                    "Kiekis": kiekis, 
                    "Kaina": kaina, 
                    "Nuolaida": nuolaida}, index=[0])
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.format(database_username, database_password, database_ip, database_name))
    df.to_sql(con=database_connection, name='fact_pirkimai', if_exists='append', index=False)
    if parde == "Nauja":
        df=pd.DataFrame({"Parduotuvė":parduotuve}, index=[0])
        df.to_sql(con=database_connection, name='dim_parduotuves', if_exists='append', index=False)
    if prek == "Nauja":
        df=pd.DataFrame({"Prekės pavadinimas":pavadinimas}, index=[0])
        df.to_sql(con=database_connection, name='dim_prekes', if_exists='append', index=False)