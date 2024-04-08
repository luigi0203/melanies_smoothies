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

#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:   
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen+  'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
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
