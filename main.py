import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from datetime import date, timedelta
from streamlit_extras.metric_cards import style_metric_cards


# Page layerout 
st.set_page_config(page_title="Analytics",page_icon="", layout="wide")

#Streamlite theme = none
theme_plotly = None

#Side bar logo
st.sidebar.image("Photos/1-6.png")

# Title 
st.title("Online Dashboard:Developed by Machary")

#load Css style 
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load dataset
df=pd.read_csv("sales.csv")


#date filter

start_date = st.sidebar.date_input("start Date", date.today()-timedelta(days=365*2))
end_date = st.sidebar.date_input(label="End Date ")

#compare date
df2 = df[(df['OrderDate'] >= str(start_date)) & (df['OrderDate'] <= str(end_date))]

# sidebar switcher
st.sidebar.header("Please filter")
city=st.sidebar.multiselect(
    "Select City",
    options=df2["City"].unique(),
    default=df2["City"].unique(),
  )

Category = st.sidebar.multiselect(
    "Select Category",
    options= df2["Product"].unique(),
    default= df2["Product"].unique(),
 ) 

region = st.sidebar.multiselect(
    "Select Region",
    options=df2["Region"].unique(),
    default=df2["Region"].unique(),
 )
df_selection=df2.query(
    "City==@city & Product==@Category & Region ==@region"
 )

 #metrics
st.subheader("Key Performance")
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Total Items", value=df_selection.Product.count(), delta="Number of Item in Stock")
col2.metric(label="Sum of Product Total Price USD:", value=f"{df_selection.TotalPrice.sum():,.0f}",delta=df_selection.TotalPrice.median())
col3.metric(label="Maximum Price USD:", value=f"{df_selection.TotalPrice.max():,.0f}", delta="High Price")
col3.metric(label="Minimum Price USD:", value=f"{df_selection.TotalPrice.min():,.0f}", delta="Low Price")
style_metric_cards(background_color="#FF588E", border_left_color="#FF4B4B", border_color="#1f66bd",box_shadow="#FFF398")

coll1,coll2=st.columns(2)
coll1.info("Business Metrics between["+str(start_date)+"] and ["+str(end_date)+"]")

#bar Chart
with st.container():  # Use st.container() or another layout function if coll1 is not defined
    st.subheader("Product by Quantity")
    source = pd.DataFrame({
        "Quantity ($)": df_selection["Quantity"],
        "Product": df_selection["Product"]
    })

    bar_chart = alt.Chart(source).mark_bar().encode(
        x="sum(Quantity ($)):Q",
        y=alt.Y("Product:N", sort="-x")
    )
    st.altair_chart(bar_chart, use_container_width=True, theme= theme_plotly,)  # Corrected the theme assignment



#Progress Bar
def Progressbar():
    st.markdown("""
<style>
.stProgress > div > div > div {
    background-image: linear-gradient(to right, #4CAF50, #8BC34A);
}
</style>
""", unsafe_allow_html=True)

    target=50000
    current=df_selection["TotalPrice"].sum()
    percent=round((current/target*100))
    mybar=st.progress(0)
    if percent> 100:
        st.subheader("Target done !")
    else:
        st.write("you have", percent, "%","of", (format(target, 'd')), "USD")
        mybar.progress(percent, text="Target percentage")

with coll1:
    st.subheader("Target Percentage")
    Progressbar()

#bar chart
 
with coll2:
    st.subheader("Product OrderDate by Quantity")
    data = {
        'Category' : df_selection['OrderDate'],
        'Value': df_selection['Quantity']
    }
df=pd.DataFrame(data)
st.bar_chart(df.set_index('Category')['Value'], use_container_width=600, height=600,)

 








