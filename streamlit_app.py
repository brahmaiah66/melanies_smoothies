# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write(
    """ Choose the fruits you want in your custom Smoothie!.
    """
)

# Contactoption = st.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone"),
# )

# st.write("Your referred Contact:", Contactoption)


# Fruitoption = st.selectbox(
#     "Whats your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("Your favorite fruit:", Fruitoption)

# title = st.text_input("Movie title", "Life of Brian")
# st.write("The current movie title is", title)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be :", name_on_order)

cnx = st.connection("snowflake")
#session = get_active_session()
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe,max_selections=5
)
if ingredients_list:
    # st.write(ingredients_list) 
    # st.text(ingredients_list)

    ingredients_String = ''

    for fruit_chosen in ingredients_list:
        ingredients_String += fruit_chosen + ' '

    # st.write(ingredients_String)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_String + """','"""+name_on_order+"""')"""

    # st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button('Submit Order')

    # if ingredients_String:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order} !", icon="✅")
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        #st.text(fruityvice_response.json())    
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)




