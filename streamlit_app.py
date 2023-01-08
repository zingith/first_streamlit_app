
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

streamlit.header('Breakfast Menu')
streamlit.text(' 🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avocado Toast')



streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def fruityvice_date(fr_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fr_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select fruit")
  else:
    streamlit.write('The user entered ', fruit_choice)
    res_fr=fruityvice_date(fruit_choice)
    streamlit.dataframe(res_fr)
except URLError as e:
  streamlit.error()
  
streamlit.header("Fruit list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    
    return my_cur.fetchall()
if streamlit.button('Get fruit list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone()
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.header("Data:")
  streamlit.dataframe(my_data_rows)
  
  
def insert_fruit_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute ("insert into pc_rivery_db.public.fruit_load_list values ('"+new_fruit+"')")
    return 'Inserted'+new_fruit

add_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('The user entered ', add_fruit)
if streamlit.button('Add fruit'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  ad_fr=insert_fruit_snowflake(add_fruit)
  my_cnx.close()
  streamlit.text(ad_fr)
