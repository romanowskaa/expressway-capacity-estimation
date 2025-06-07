import streamlit as st
from backend import BasicSection
import plotly.express as px
import plotly.graph_objects as go

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

col = st.columns((1.5, 6.5, 1.5), gap='medium')

bs = BasicSection(road_class='A', access_points=access_points, speed_limit=speed_limit, area_type=1, adt=adt, hv_share=hv_share, profile='DASM', lanes=lanes, gradient=0.02, section_length=10)
df = bs.van_aerde_calculations()
df = df[df['density'] <= 26.5]

with col[0]:
    avg_speed = round(bs.calculate_avg_speed(), 1)
    ffs_speed = bs.calculate_ffs()
    hourly_flow = bs.calculate_flow()
    base_capacity = bs.estimate_base_capacity()
    real_capacity = round(base_capacity * lanes * bs.calculate_k15() / bs.calculate_ew())
    
    st.markdown('###### Traffic metrics')

    st.metric(label='Traffic volume [veh/h]',
              value=bs.calculate_hourly_volume())
    
    st.metric(label='Cross-section capacity [veh/h]',
              value=real_capacity)
    
    st.metric(label='Capacity utilization', 
              value=f"{round(100*hourly_flow/base_capacity, 1)}%")
    
    st.divider()

    st.metric(label='Traffic flow [pc/h/lane]', 
              value=f"{hourly_flow}")

    st.metric(label='Base capacity [pc/h/lane]',
              value=base_capacity)
    
with col[2]: 
    st.markdown('###### Traffic conditions')
    
    st.metric(label='Avg speed [km/h]', 
              value=f"{avg_speed}",
              delta=f"{round(100*(avg_speed - ffs_speed)/ffs_speed,1)}% to FFS")
    
    st.metric(label='Level of Service',
              value=f"{bs.assess_los()}", border=True)

with col[1]:

    
    df_trafficx = df['volume']
    df_trafficy = df['speed']

    scat_plot = px.scatter(df, x=df_trafficx, y=df_trafficy)

    scat_plot.update_layout(title='Flow-speed relationship', 
                                    yaxis=dict(title='', range=[0, 150]),
                                    xaxis=dict(title='', range=[0, 2500]))
    
    scat_plot.update_layout()

    scat_plot.add_trace(go.Scattergl(x=[hourly_flow], y=[avg_speed], mode='markers', 
                                   marker=dict(size=20, color='red', symbol='circle'),
                                   showlegend=False,

                                   )
                        )

    # scat_plot.update_layout(hovermode="x")

    st.plotly_chart(scat_plot)