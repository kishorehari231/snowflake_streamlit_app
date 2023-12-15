import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My parents Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)

my_fruit_list = my_fruit_list.set_index('Fruit') 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruitvice_data(fruit_choice):
      fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+fruit_choice) 
      fruityvice_normalized = pd.json_normalize(fruityvice_response.json()) 
      return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
  
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','')
  if not fruit_choice:
      streamlit.error('Kindly select a fruit to get information')
  else:
    back_from_function=get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
streamlit.header("The friut load list contains")
streamlit.dataframe(my_data_row) 

add_my_fruit = streamlit.text_input('What fruit you would like to add?','')
streamlit.write('Thanks for entering ', add_my_fruit)

my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")
