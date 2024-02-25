import streamlit as st
import pandas as pd
import configparser
from sqlalchemy import create_engine, Select
import sqlalchemy as sqa
from pages.Model import *
import time
from sqlalchemy.orm import sessionmaker
import random
from datetime import datetime


st.set_page_config(
    page_title="Adopcja Psa",
    page_icon="dog",
    layout="wide"
)

if "selected_id" not in st.session_state:
    st.session_state["selected_id"] = 0



#odczyt konfiguracji
config = configparser.ConfigParser()
config.read('.streamlit\secrets.toml')

server = config['MSSQL']['server']
port = config['MSSQL']['port']
database = config ['MSSQL']['database']
username = config ['MSSQL']['username']
password = config ['MSSQL']['password']


connection_string = f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
engine = sqa.create_engine(connection_string)


#Utwórz sesję

Session = sessionmaker(bind=engine)
session= Session()

def dataframe_with_selections(df):
        df_with_selections = df.copy()
        df_with_selections.insert(0, 'Zaznacz', False)

        edited_df = st.data_editor(
            df_with_selections,
            hide_index=True,
            column_config={"Zaznacz": st.column_config.CheckboxColumn(required=True)},
            disabled=df.columns,
            use_container_width=True,
            num_rows='fixed'
            
        )
        
        edited_df.set_index('id', inplace=True)

        selected_rows = edited_df[edited_df.Zaznacz]
        return selected_rows.drop('Zaznacz', axis=1)



stmt = sqa.select(Zwierze)
# stmt #zakomentować aby nie wyświetlać głupiego selecta na stronie
df = pd.read_sql(stmt, session.bind)

selection = dataframe_with_selections(df)

if selection.size > 0:
    with st.expander(":writing_hand: Modyfikuj rekord", expanded=True):
          
            u_id = int(selection.index[0])
            
            col1, col2 = st.columns(2)
            u_imie = col1.text_input(label='Imię',value = selection["imie"].iloc[0])
            u_masa = col2.text_input(label='Masa', value = selection["masa"].iloc[0])
            u_plec = col1.text_input(label='Płeć', value = selection["plec"].iloc[0])
            u_typRasy = col2.text_input(label='Typ Rasy', value = selection["typRasy"].iloc[0])
            u_opis = col1.text_input(label='Opis', value = selection["opis"].iloc[0])
            u_statusZwierzecia = col2.text_input(label='Status', value = selection["statusZwierzecia"].iloc[0])
            u_dataPrzyjecia = col1.date_input(label='Data przyjęcia', value = selection["dataPrzyjecia"].iloc[0])
            u_dataWydania = col2.date_input(label='Data wydania')
            u_numerChip = col1.text_input(label='Numer CHIP', value = selection["numerChip"].iloc[0])
            u_wiek = col2.text_input(label='Wiek', value = selection["wiek"].iloc[0])
            u_boks = col1.text_input(label='Boks', value = selection["boks"].iloc[0])

            zmien = col1.button(label="Zmień", key="zmien", type='secondary', disabled=False)
            usun = col1.button(label="Usuń", key="usun", type='primary')
            
            if zmien:
                  with st.spinner('Zapisywanie...'):
                        zwierze = session.query(Zwierze).filter_by(id=u_id).one()
                        if zwierze:
                            zwierze.imie = u_imie
                            zwierze.masa = u_masa
                            zwierze.plec = u_plec
                            zwierze.typRasy = u_typRasy
                            zwierze.opis = u_opis
                            zwierze.statusZwierzecia = u_statusZwierzecia 
                            zwierze.dataPrzyjecia = u_dataPrzyjecia.strftime('%Y-%m-%d')
                            if u_dataWydania == None:
                                    zwierze.dataWydania = u_dataWydania
                            else:
                                    zwierze.dataWydania = u_dataWydania.strftime('%Y-%m-%d')

                            zwierze.numerChip = u_numerChip
                            zwierze.wiek = u_wiek
                            zwierze.boks = u_boks
                        session.commit()
                  st.success('Zmienione')
                  st.rerun()

            if usun:
                  zwierze = session.query(Zwierze).filter_by(id=u_id).one()
                  session.delete(zwierze)
                  session.commit()
                  st.success('Usunięty')
                  time.sleep(2)
                  st.rerun()
else:
      with st.expander(":heavy_plus_sign: Dodaj nowe zwierzę", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            i_imie = col1.text_input(label='Imię', placeholder= 'np.: Reszka')
            i_masa = col2.text_input(label='Masa', value = '20')
            i_plec = col3.text_input(label='Płeć', value = 'Samica')
            i_typRasy = col4.text_input(label='Typ Rasy', value = 'mieszaniec')
            i_opis = col1.text_input(label='Opis', value = 'to jest testowy opis')
            i_statusZwierzecia = col2.text_input(label='Status', value = 'Do adopcji')
            i_dataPrzyjecia = col3.date_input(label='Data przyjęcia', value = datetime.now())
            i_numerChip = col4.text_input(label='Numer CHIP', value = random.randrange(100000, 1000000))
            i_wiek = col1.text_input(label='Wiek', value = '5')
            i_boks = col2.text_input(label='Boks', value = 'B14')

            if i_masa == '' or i_plec == '' or i_typRasy =='' or i_statusZwierzecia =='' or i_dataPrzyjecia =='':
                  disable_btn = True
            else:
                  disable_btn = False

            zapisz = st.button(label='Zapisz', type='primary', disabled=disable_btn)
                  
            if zapisz:
                  with st.spinner('Zapisywanie...'):
                        nowe_zwierze = Zwierze(imie  = i_imie,
                              masa = i_masa,
                              plec = i_plec,
                              typRasy = i_typRasy,
                              opis = i_opis,
                              statusZwierzecia = i_statusZwierzecia,
                              dataPrzyjecia =i_dataPrzyjecia.strftime('%Y-%m-%d'),
                              numerChip = i_numerChip,
                              wiek = i_wiek,
                              boks = i_boks
                                          )
                        
                  try:
                        session.add(nowe_zwierze)
                  except:
                        session.rollback()
                        raise
                  else:
                        session.commit()
                  st.success('Zapisane')
                  st.rerun()










      #       	[id] [int] IDENTITY(1,1) NOT NULL,
	# [imie] [varchar](25) NULL,
	# [masa] [real] NOT NULL,
	# [plec] [varchar](10) NOT NULL,
	# [typRasy] [varchar](25) NOT NULL,
	# [opis] [varchar](250) NULL,
	# [statusZwierzecia] [varchar](25) NOT NULL,
	# [dataPrzyjecia] [date] NOT NULL,
	# [dataWydania] [date] NULL,
	# [numerChip] [char](20) NULL,
	# [wiek] [varchar](20) NULL,
	# [boks] [varchar](20) NULL,