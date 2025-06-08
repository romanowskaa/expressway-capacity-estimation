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
    next_critical_flow = bs.calculate_metrics_at_density(bs.extract_los_density())[1]
    next_critical_volume = round(next_critical_flow * lanes * bs.calculate_k15() / bs.calculate_ew())
    
    st.markdown('###### Traffic metrics')

    st.metric(label='Traffic volume [veh/h]',
              value=bs.calculate_hourly_volume())
    
    st.metric(label='Cross-section capacity [veh/h]',
              value=real_capacity)
    
    st.metric(label='Capacity utilization', 
              value=f"{round(100*hourly_flow/base_capacity, 1)}%")
    
    st.metric(label='Volume to next LOS [veh/h]',
              value=f"{round(next_critical_volume - bs.calculate_hourly_volume())}")
    
    st.divider()

    st.markdown('###### Calculated flows')

    st.metric(label='Traffic flow [pc/h/lane]', 
              value=f"{hourly_flow}")

    st.metric(label='Base capacity [pc/h/lane]',
              value=base_capacity)
    
with col[2]: 
    st.markdown('###### Traffic conditions')
    
    st.metric(label='Avg speed [km/h]', 
              value=f"{avg_speed}",
              delta=f"{round(100*(avg_speed - ffs_speed)/ffs_speed,1)}% to FFS")
    
    st.metric(label='Density [pc/km/lane]', 
              value=f"{round(hourly_flow/avg_speed, 1)}")
    
    st.metric(label='Level of Service',
              value=f"{bs.assess_los()}", border=True)

with col[1]:

    
    df_trafficx = df['volume']
    df_trafficy = df['speed']

    scat_plot = px.line(df, x=df_trafficx, y=df_trafficy)

    scat_plot.update_layout(title='Flow-speed relationship', 
                                    yaxis=dict(title='Avg speed [km/h]', range=[0, 150]),
                                    xaxis=dict(title='Traffic flow [pc/h/lane]', range=[0, 2500]))
    
    scat_plot.update_layout()

    scat_plot.add_trace(go.Scattergl(x=[hourly_flow], y=[avg_speed], mode='markers', 
                                   marker=dict(size=12, color='white', symbol='circle', line=dict(width=2,
                                        color='DarkSlateGrey')),
                                   showlegend=False,
                                   )
                        )
    
    # line plot at densities corresponding to LOS boundaries
    scat_plot.add_trace(go.Scatter(x=[0, bs.calculate_metrics_at_density(6.5)[1]], 
                                   y=[0, bs.calculate_metrics_at_density(6.5)[0]], 
                                   mode='markers+lines', 
                                   opacity=0.5, name='costam',
                                   showlegend=False, 
                                   line=dict(color='royalblue', width=1, dash='dot')))
    scat_plot.add_trace(go.Scatter(x=[0, bs.calculate_metrics_at_density(11)[1]], 
                                   y=[0, bs.calculate_metrics_at_density(11)[0]], 
                                   mode='markers+lines', 
                                   opacity=0.5, name='costam',
                                   showlegend=False, 
                                   line=dict(color='royalblue', width=1, dash='dot')))
    scat_plot.add_trace(go.Scatter(x=[0, bs.calculate_metrics_at_density(16)[1]], 
                                   y=[0, bs.calculate_metrics_at_density(16)[0]], 
                                   mode='markers+lines', 
                                   opacity=0.5, name='costam',
                                   showlegend=False, 
                                   line=dict(color='royalblue', width=1, dash='dot')))
    scat_plot.add_trace(go.Scatter(x=[0, bs.calculate_metrics_at_density(21)[1]], 
                                   y=[0, bs.calculate_metrics_at_density(21)[0]], 
                                   mode='markers+lines', 
                                   opacity=0.5, name='costam',
                                   showlegend=False, 
                                   line=dict(color='royalblue', width=1, dash='dot')))
    scat_plot.add_trace(go.Scatter(x=[0, bs.calculate_metrics_at_density(26.5)[1]], 
                                   y=[0, bs.calculate_metrics_at_density(26.5)[0]], 
                                   mode='markers+lines', 
                                   opacity=0.5, name='costam',
                                   showlegend=False, 
                                   line=dict(color='royalblue', width=1, dash='dot')))
    
    scat_plot.add_annotation(
        x=hourly_flow, y=avg_speed,
        text=f"Predicted traffic state",
        showarrow=True,
        arrowhead=2)

    scat_plot.add_annotation(
        x=bs.calculate_metrics_at_density(6.5)[1] - 350, y=bs.calculate_metrics_at_density(6.5)[0] - 10,
        text=f"LOS A",
        align='left',
        showarrow=False)
    scat_plot.add_annotation(
        x=bs.calculate_metrics_at_density(11)[1] - 350, y=bs.calculate_metrics_at_density(11)[0] - 10,
        text=f"LOS B",
        align='left',
        showarrow=False)
    scat_plot.add_annotation(
        x=bs.calculate_metrics_at_density(16)[1] - 350, y=bs.calculate_metrics_at_density(16)[0] - 10,
        text=f"LOS C",
        align='left',
        showarrow=False)
    scat_plot.add_annotation(
        x=bs.calculate_metrics_at_density(21)[1] - 350, y=bs.calculate_metrics_at_density(21)[0] - 5,
        text=f"LOS D",
        align='left',
        showarrow=False)
    scat_plot.add_annotation(
        x=bs.calculate_metrics_at_density(26.5)[1] - 200, y=bs.calculate_metrics_at_density(26.5)[0],
        text=f"LOS E",
        align='left',
        showarrow=False)
    scat_plot.add_annotation(
        x=bs.calculate_metrics_at_density(26.5)[1] - 200, y=bs.calculate_metrics_at_density(26.5)[0] - 20,
        text=f"LOS F",
        align='left',
        showarrow=False)
    st.plotly_chart(scat_plot)