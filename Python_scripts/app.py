import streamlit as st
from backend import BasicSection as bs
import plotly.express as px

# page config
st.set_page_config(
    page_title="Polish highway capacity method",
    page_icon=":oncoming_automobile:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# sidebar
with st.sidebar:
    st.subheader(':oncoming_automobile: Select options:')

    road_classes = ['A', 'S', 'GPG']
    road_class = st.selectbox('Road class', road_classes)
    speed_limits = [80, 90, 100, 110, 120, 130, 140]
    speed_limit = st.selectbox('Speed limit', speed_limits)
    access_points = st.number_input('No of access points', min_value=0, max_value=30, value=0, step=1, 
                                    help='Some help')
    area_types = ['rural', 'agglomeration']
    area_type = st.selectbox('Area type', area_types)
    adt = st.number_input('ADT', min_value=0, max_value=300000, value=30000, step=1000, 
                                    help='Some help')
    hv_share = st.number_input('HV share', min_value=0.0, max_value=1.0, value=0.0, step=0.01, 
                                    help='Some help')
    lanes_list = [2, 3]
    lanes = st.selectbox('No. of lanes', lanes_list)

bs = bs(road_class='A', access_points=access_points, speed_limit=speed_limit, area_type=1, adt=adt, hv_share=hv_share, profile='DASM', lanes=lanes, gradient=0.02, section_length=10)
df = bs.van_aerde_calculations()



df_trafficx = df['volume']
df_trafficy = df['speed']

scat_plot = px.scatter(df, x=df_trafficx, y=df_trafficy)
scat_plot.update_layout(title='Relationship between traffic parameters and weather', 
                                yaxis=dict(title='', range=[0, 150]), 
                                xaxis=dict(title='', range=[0, 2500]))
st.plotly_chart(scat_plot)