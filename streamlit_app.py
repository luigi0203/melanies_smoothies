# Import python packages
import requests
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Get the current credentials
session = get_active_session()

# Write directly to the app
st.title("My Parents New Healthy Diner")
st.header("Breakfast Menu")
st.write('')
st.subheader("Omega 3 & Blueberry Oatmeal")
st.subheader("Kale, Spinach & Smoothie")
st.subheader("Hard-Boiled Free-Range Egg")

st.write(
    "Choose the fruits you want in your custom Smoothie! "
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:   
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
           
    #st.write(ingredients_list)
    
    my_insert_stmt = """ insert into smoothies.public.orders(INGREDIENTS, NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()        
        st.success('Your Smoothie is ordered!', icon="✅")
