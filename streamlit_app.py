import streamlit as st
from snowflake.snowpark.functions import col

streamlit.title("Customize Your Smoothie!")
streamlit.write(
    """Choose the fruits you want in your custom smoothie!
""")

name_on_order = st.text_input("Name on Smoothie:")
streamlit.write("The name on your smoothie will be", name_on_order)

cnx = streamlit.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True) 

ingredients_options = st.multiselect(
    "Choose upto 5 options:",
    my_dataframe ,
    max_selections = 5
)



if ingredients_options:
    ingredients_string = ''

    for fruit_chosen in ingredients_options:
        ingredients_string += fruit_chosen + ' '
        #ingredients_string = ", ".join(ingredients_options)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    streamlit.write(my_insert_stmt)

    submit_order = streamlit.button('Submit Order')
    
    if submit_order:
        session.sql(my_insert_stmt).collect()
        #st.success('Your Smoothie is ordered!', icon="✅")
        streamlit.success('Your Smoothie is ordered,' + name_on_order +"!" )


