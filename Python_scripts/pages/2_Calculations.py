import streamlit as st
from backend import BasicSection
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# page config
st.set_page_config(
    page_title="Polish highway capacity method",
    page_icon=":oncoming_automobile:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# sidebar
with st.sidebar:
    st.subheader(':oncoming_automobile: Input data')

    road_classes = ["A", "S", "GPG"]
    road_classes_display = {'A': 'Motorway', 'S': 'Express road', 'GPG': 'Main road'}
    road_class = st.selectbox(':small_blue_diamond: Road class', road_classes, format_func=lambda x: road_classes_display.get(x, str(x)))

    speed_limits = [80, 90, 100, 110, 120, 130, 140]
    speed_limit = st.selectbox(':small_blue_diamond: Speed limit', speed_limits)

    area_types = [0, 1]
    area_types_display = {0: 'agglomeration', 1: 'rural'}
    area_type = st.selectbox(':small_blue_diamond: Area type', area_types, format_func=lambda x: area_types_display.get(x, str(x)))
    
    lanes_list = [2, 3]
    lanes = st.selectbox(':small_blue_diamond: No. of lanes', lanes_list)

    gradients = [0.02, 0.03, 0.04, 0.05]
    gradients_display = {0.02: 'up to 2%', 0.03: '3%', 0.04: '4%', 0.05: '5% and more'}
    gradient = st.selectbox(':small_blue_diamond: Longitudinal gradient', gradients, format_func=lambda x: gradients_display.get(x, str(x)))

    access_points = st.number_input(':small_blue_diamond: No of access points', min_value=0, max_value=30, value=0, step=1, 
                                    help='Some help')
    section_length = st.number_input(':small_blue_diamond: Section length', min_value=0, max_value=50, value=10, step=1, 
                                    help='Input annual traffic volume at road cross-section')
    
    volume_type = st.selectbox(':small_blue_diamond: Input volume', ['ADT', 'hourly volume'])
    if volume_type == 'ADT':
        adt = st.slider(':small_blue_diamond: ADT', min_value=0, max_value=300000, value=30000, step=1000, 
                            help='Input annual traffic volume at road cross-section', label_visibility='hidden')
        if road_class == 'GPG':
            profiles = ['DGPG']
        else:
            profiles = ['DASM', 'DASS', 'DASD']
            profiles_display = {'DGPG': 'Low', 'DASM': 'Low', 'DASS': 'Medium', 'DASD': 'High'}
            profile = st.selectbox(':small_blue_diamond: Seasonal traffic variations', profiles, format_func=lambda x: profiles_display.get(x, str(x)))
    else:
        input_hourly_volume = st.slider('Hourly traffic', min_value=0, value=1000, step=100, max_value=10000, label_visibility='hidden')
        adt = int(2 * input_hourly_volume / 0.095)
        profile = 'DGPG'
    
    hv_share = st.number_input(':small_blue_diamond: HV share', min_value=0.0, max_value=1.0, value=0.0, step=0.01, 
                                    help='Some help')




col = st.columns((1.5, 6.5, 1.5), gap='medium')

bs = BasicSection(road_class=road_class, access_points=access_points, speed_limit=speed_limit, area_type=area_type, adt=adt, hv_share=hv_share, profile=profile, lanes=lanes, gradient=gradient, section_length=section_length)

if volume_type != 'ADT':
    adt_from_volume = bs.calculate_adt_from_volume(input_hourly_volume)
    bs = BasicSection(road_class=road_class, access_points=access_points, speed_limit=speed_limit, area_type=area_type, adt=adt_from_volume, hv_share=hv_share, profile=profile, lanes=lanes, gradient=gradient, section_length=section_length)

df = bs.van_aerde_calculations()
df = df[df['density'] <= 26.5]

with col[0]:
    if volume_type == 'ADT':
        hourly_volume = bs.calculate_hourly_volume()
    else:
        hourly_volume = input_hourly_volume
    if bs.calculate_avg_speed() != None:
        avg_speed = round(bs.calculate_avg_speed(), 1)
    ffs_speed = bs.calculate_ffs()
    hourly_flow = bs.calculate_flow()
    base_capacity = bs.estimate_base_capacity()
    real_capacity = round(base_capacity * lanes * bs.calculate_k15() / bs.calculate_ew())
    
    st.markdown('###### Traffic metrics')

    st.metric(label='Traffic volume [veh/h]',
              value=hourly_volume)
    
    st.metric(label='Cross-section capacity [veh/h]',
              value=real_capacity)
    
    st.metric(label='Capacity utilization', 
              value=f"{round(100*hourly_flow/base_capacity, 1)}%")
    

    st.divider()

    st.markdown('###### Calculated flows')

    st.metric(label='Traffic flow [pc/h/lane]', 
              value=f"{hourly_flow}")

    st.metric(label='Base capacity [pc/h/lane]',
              value=base_capacity)
    
with col[2]: 
    st.markdown('###### Traffic conditions')
    
    if bs.calculate_avg_speed() != None:
        
        st.metric(label='Free-flow speed [km/h]', 
                    value=f"{ffs_speed}")
        
        st.metric(label='Avg speed [km/h]', 
                    value=f"{avg_speed}",
                    delta=f"{round(100*(avg_speed - ffs_speed)/ffs_speed,1)}% to FFS")
            
        st.metric(label='Density [pc/km/lane]', 
                    value=f"{round(hourly_flow/avg_speed, 1)}")

    st.metric(label='Level of Service',
              value=f"{bs.assess_los()}", border=True)

with col[1]:
    if bs.calculate_avg_speed() is not None and hourly_flow/base_capacity <= 1:
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

        ### table with critical densities
        st.markdown('###### Critical traffic flow [pc/h/lane]')
    
        df_crit_flow = pd.DataFrame(
            {
            "PSR A": [round(bs.calculate_metrics_at_density(6.5)[1])],
            "PSR B": [round(bs.calculate_metrics_at_density(11)[1])],
            "PSR C": [round(bs.calculate_metrics_at_density(16)[1])],
            "PSR D": [round(bs.calculate_metrics_at_density(21)[1])],
            "PSR E": [round(bs.calculate_metrics_at_density(26.5)[1])],
            }
        )
        st.dataframe(df_crit_flow, hide_index=True)
    else:
        st.markdown('<b style="color:red;">Predicted hourly flow exceeds capacity.</b>', unsafe_allow_html=True)

        with st.expander("See explanation"):
            st.write('''
            If flow exceeds capacity **congested traffic conditions** appears. 
            The state of congested traffic (figure below) occurs after a breakdown in traffic flow, 
            i.e. after a significant drop in traffic speed caused by local traffic congestion. 
            This is characterised by densed traffic on the road and fluctuating speed - 
            vehicles are forced to brake again and again until they come to a standstill and then restart and accelerate. 
            The intensity of the congested traffic can fluctuate from low to high. 
            This condition often occurs due to accidents or other traffic incidents, 
            narrowing of the cross-section or other reasons that reduce capacity (so-called local capacity restriction).
            ''')
            st.image("files\\congested_traffic.png")
    