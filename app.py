### Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

### Config
st.set_page_config(
    page_title="Streamlit Tutorial",
    page_icon="🏎️",
    layout="wide",
)


def page_1():
    ### Title
    st.title("Streamlit Tutorial")

    ### Markdown
    st.markdown("""## Streamlit Tutorial
                
    `ceci est du code`         
                """)

    ### Load Data
    @st.cache
    def load_data():
        data = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/e-commerce_data.csv")
        data.currency = data.currency.apply(lambda x: float(x.replace('$', '')))
        data.Date = data.Date.apply(lambda x: ''.join(x.split(',')[-2:]))
        
        return data

    df = load_data()


    ### Show Data with checkbox
    if st.checkbox("Show Data"):
        st.write(df)


    ## Simple bar chart
    data_curency = df.set_index("country")["currency"]
    st.bar_chart(data_curency)



    ### chart with plotly
    fig = px.histogram(df.sort_values("country"), x="country", y="currency", barmode="group")
    st.plotly_chart(fig, use_container_width=True)


    ### Set columns

    col1, col2 = st.columns(2)

    ### Column 1
    with col1:  
        st.write("## Column 1")
        country = st.selectbox("Select", df.country.unique())

        country_sales = df[df["country"]==country]
        fig = px.histogram(country_sales, x="Date", y="currency")
        fig.update_layout(bargap=0.2)
        st.plotly_chart(fig, use_container_width=True)


    ### Column 2
    with col2:  
        st.write("## Column 2")

        with st.form("form1"):
            st.write("## Form")

            country = st.selectbox('Select your Country', df.country.unique())

            min, max = st.slider("Select a range", 0, 100, (25, 75))



            buton = st.form_submit_button("Submit")

            if buton:
                st.write("Form submitted")
                mean_ = df[(df.country == country) & (df.currency >min) & (df.currency <max)].currency.mean()

                st.write(f"Mean of sales for {country} is {mean_}")


### Sidebar

st.sidebar.title("Sidebar")

st.sidebar.markdown("""## Sidebar""")


def page_2():
    picture = st.camera_input("Take a picture")

    if picture:
        st.image(picture)


import os
def page_3():

    path = "./Miyazaki/"
    movies = os.listdir(path)
    movie = st.selectbox("Select a movie", movies)

    video_file = open(path+movie, 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)



dict_page = {
    "Page 1": page_1,
    "Page 2": page_2,
    "Page 3": page_3,
}

page = st.sidebar.selectbox('Select your page', ["Page 1", "Page 2", "Page 3"])



dict_page[page]()


### footer