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
    st.subheader(':oncoming_automobile: Dane wejściowe')

    road_classes = ["A", "S", "GPG"]
    road_classes_display = {'A': 'A', 'S': 'S', 'GPG': 'GP lub G'}
    road_class = st.selectbox('Klasa drogi', 
                              road_classes, 
                              format_func=lambda x: road_classes_display.get(x, str(x)))

    speed_limits = [80, 90, 100, 110, 120, 130, 140]
    speed_limit = st.selectbox('Ograniczenie prędkości [km/h]', 
                               speed_limits)

    area_types = [0, 1]
    area_types_display = {0: 'aglomeracji', 1: 'zamiejski'}
    area_type = st.selectbox('Obszar', 
                             area_types, 
                             format_func=lambda x: area_types_display.get(x, str(x)),
                             help="""
                                **Obszar aglomeracji** - obszar o wysokiej koncentracji zabudowy i zagospodarowania, zamieszkany przez duże skupiska ludności. 
                                W jej centralnej części znajduje się jeden lub więcej ośrodków centralnych z rozległą strefą podmiejską, 
                                natomiast wokół nich leżą mniejsze ośrodki (miasta, miejscowości satelitarne). 
                                Aglomeracje w Polsce: białostocka, bydgosko-toruńska, górnośląska, krakowska, łódzka, lubelska, poznańska, rybnicko–jastrzębska, szczecińska, trójmiejska, warszawska, wrocławska.\n
                                **Obszar zamiejski** - poza obszarem aglomeracji.
                            """
                )
    
    lanes_list = [2, 3]
    lanes = st.selectbox('Liczba pasów', 
                         lanes_list,
                         help='Liczba pasów dotyczy jednego, analizowanego kierunku ruchu')

    gradients = [0.02, 0.03, 0.04, 0.05]
    gradients_display = {0.02: 'do 2%', 0.03: '3%', 0.04: '4%', 0.05: '5% i więcej'}
    gradient = st.selectbox('Pochylenie podłużne', gradients, 
                            format_func=lambda x: gradients_display.get(x, str(x)))
    
    access_points = st.number_input('Gęstość wjazdów i wyjazdów [liczba/km]', 
                                    min_value=0.0, 
                                    max_value=2.5, 
                                    value=.0, 
                                    step=.1, 
                                    help="""
                                    **Drogi klasy A i S:** tzw. gęstość wjazdów i wyjazdów oblicza się jako liczbę 
                                    wjazdów i wyjazdów na odcinku o długości 10 km (5 km w jednym i 
                                    drugim kierunku licząc od środka analizowanego odcinka), podzielona 
                                    przez długość tego odcinka (w km).\n
                                    **Drogi klasy GP i G:** oblicza się gęstość punktów włączeń, jako sumę punktów 
                                    włączeń (skrzyżowania, wyjazdy publiczne, istotne włączenia) dla danego 
                                    kierunku ruchu na całej długości odcinka i dzieli przez długość odcinka (w km). 
                                    """
                                )
    
    
    volume_type = st.selectbox('Wejściowe natężenie ruchu', ['SDR [P/24h]', 'Natężenie miarodajne [P/h]'])
    if volume_type == 'SDR [P/24h]':
        adt = st.number_input('*Wprowadź wartość:*', 
                              min_value=0, 
                              max_value=300000, 
                              value=30000, 
                              help="""
                              Wprowadź wartość SDR **dla całego przekroju drogi**. Na podstawie 
                              SDR i profilu drogi (zmienność sezonowa), wyznaczane jest miarodajne godzinowe natężenie ruchu w analizowanym kierunku ruchu,
                              """
                            )
        if road_class == 'GPG':
            profiles = ['DGPG']
        else:
            profiles = ['DASM', 'DASS', 'DASD']
            profiles_display = {'DGPG': 'mała', 'DASM': 'mała', 'DASS': 'średnia', 'DASD': 'duża'}
            profile = st.selectbox('*Zmienność sezonowa ruchu*', 
                                   profiles, 
                                   format_func=lambda x: profiles_display.get(x, str(x)),
                                   
                                   help="""
                                   W uproszczeniu można przyjąć:\n
                                   - **drogi o gospodarczym charakterze ruchu:** mała zmienność sezonowa ruchu\n
                                   - **drogi o turystyczno-rekreacyjnym charakterze ruchu:** średnia zmienność sezonowa\n
                                   W celu określenia zmienności można posilić się wskaźnikiem wahan ruchu SDRL/SDRR, który jest stosunkiem 
                                   średniego dobowego ruchu w miesiącach letnich w miesiącach letnich (SDRL) do średniego rocznego dobowego ruchu (SDRR).
                                   Jeżeli SRDL/SDRR <= 1,2: mała zmienność sezonowa, dla wartości od 1,21 do 1,6: średnia zmienność sezonowa, dla wartości powyżej 1,6: 
                                   wysoka sezonowa zmienność ruchu.
                                   """
                                   )
    else:
        input_hourly_volume = st.number_input('*Wprowadź wartość:*', 
                                              min_value=0, 
                                              value=1000, 
                                              step=100, 
                                              max_value=10000,
                                              help="""
                                              Wprowadź wartość natężenia miarodajnego *Qm* dla danego kierunku ruchu.
                                              """
                                              )
        
        adt = int(2 * input_hourly_volume / 0.095)
        profile = 'DGPG'
    
    hv_share = st.number_input('Udział pojazdów ciężkich', min_value=0.0, max_value=1.0, value=0.0, step=0.01, 
                                    help="""
                                    Jako pojazdy ciężkie należy traktować: samochody ciężarowe, ciężarowe z przyczepą, ciągniki siodłowe, autobusy.
                                    """
                                    )



col = st.columns((2, 6, 2), gap='medium')

bs = BasicSection(road_class=road_class, access_points=access_points, speed_limit=speed_limit, area_type=area_type, adt=adt, hv_share=hv_share, profile=profile, lanes=lanes, gradient=gradient)

if volume_type != 'SDR [P/24h]':
    adt_from_volume = bs.calculate_adt_from_volume(input_hourly_volume)
    bs = BasicSection(road_class=road_class, access_points=access_points, speed_limit=speed_limit, area_type=area_type, adt=adt_from_volume, hv_share=hv_share, profile=profile, lanes=lanes, gradient=gradient)

df = bs.van_aerde_calculations()
df = df[df['density'] <= 26.5]

with col[0]:
    if volume_type == 'SDR [P/24h]':
        hourly_volume = bs.calculate_hourly_volume()
    else:
        hourly_volume = input_hourly_volume
    if bs.calculate_avg_speed() != None:
        avg_speed = round(bs.calculate_avg_speed(), 1)
    ffs_speed = bs.calculate_ffs()
    hourly_flow = bs.calculate_flow()
    base_capacity = bs.estimate_base_capacity()
    real_capacity = round(base_capacity * lanes * bs.calculate_k15() / bs.calculate_ew())
    
    st.markdown('###### Parametry ruchu (w przekroju)')

    st.metric(label='Natężenie ruchu Qm [P/h]',
              value=hourly_volume)
    
    st.metric(label='Przepustowość C [P/h]',
              value=real_capacity)
    
    st.metric(label='Stopień wykorzystania X', 
              value=f"{round(100*hourly_flow/base_capacity, 1)}%")
    

    st.divider()

    st.markdown('###### Wartości obliczeniowe (na 1 pas ruchu)')

    st.metric(label='Natężenie ruchu Q0 [E/h/pas]', 
              value=f"{hourly_flow}",
              )

    st.metric(label='Przepustowość C0 [E/h/pas]',
              value=base_capacity)
    
with col[2]: 
    st.markdown('###### Warunki ruchu')
    
    if bs.calculate_avg_speed() != None:
        
        st.metric(label='Prędkość swobodna Vsw [km/h]', 
                    value=f"{ffs_speed}")
        
        st.metric(label='Średnia prędkość V [km/h]', 
                    value=f"{avg_speed}",
                    delta=f"{round(100*(avg_speed - ffs_speed)/ffs_speed,1)}% od swobodnej")
            
        st.metric(label='Gęstość k0 [E/km/pas]', 
                    value=f"{round(hourly_flow/avg_speed, 1)}")

    st.metric(label='PSR',
              value=f"{bs.assess_los()}", 
              border=True,
              help="Poziom Swobody Ruchu")

with col[1]:
    if bs.calculate_avg_speed() is not None and hourly_flow/base_capacity <= 1:
        df_trafficx = df['volume']
        df_trafficy = df['speed']

        scat_plot = px.line(df, x=df_trafficx, y=df_trafficy)

        scat_plot.update_layout(title='Zależność prędkości od natężenia ruchu', 
                                            yaxis=dict(title='Średnia prędkość [km/h]', range=[0, 150]),
                                            xaxis=dict(title='Natężenie obliczeniowe ruchu [E/h/pas]', range=[0, 2500]))
            
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
                text=f"Przewidywany stan ruchu",
                showarrow=True,
                arrowhead=2)

        scat_plot.add_annotation(
                x=bs.calculate_metrics_at_density(6.5)[1] - 350, y=bs.calculate_metrics_at_density(6.5)[0] - 10,
                text=f"PSR A",
                align='left',
                showarrow=False)
        scat_plot.add_annotation(
                x=bs.calculate_metrics_at_density(11)[1] - 350, y=bs.calculate_metrics_at_density(11)[0] - 10,
                text=f"PSR B",
                align='left',
                showarrow=False)
        scat_plot.add_annotation(
                x=bs.calculate_metrics_at_density(16)[1] - 350, y=bs.calculate_metrics_at_density(16)[0] - 10,
                text=f"PSR C",
                align='left',
                showarrow=False)
        scat_plot.add_annotation(
                x=bs.calculate_metrics_at_density(21)[1] - 350, y=bs.calculate_metrics_at_density(21)[0] - 5,
                text=f"PSR D",
                align='left',
                showarrow=False)
        scat_plot.add_annotation(
                x=bs.calculate_metrics_at_density(26.5)[1] - 200, y=bs.calculate_metrics_at_density(26.5)[0],
                text=f"PSR E",
                align='left',
                showarrow=False)
        scat_plot.add_annotation(
                x=bs.calculate_metrics_at_density(26.5)[1] - 200, y=bs.calculate_metrics_at_density(26.5)[0] - 20,
                text=f"PSR F",
                align='left',
                showarrow=False)
        st.plotly_chart(scat_plot)

        ### table with critical densities
        st.markdown('###### Tablica natężeń krytycznych dla analizowanego odcinka [E/h/pas]')
    
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
        st.markdown('<b style="color:red;">Przekroczona przepustowość przekroju.</b>', unsafe_allow_html=True)

        with st.expander("Zobacz wyjaśnienie"):
            st.write('''
                    **Na drodze występuje stan ruchu wymuszonego, PSR F.**\n
                     
                     Stan ruchu wymuszonego występuje po załamaniu się płynności ruchu, czyli po znacznym spadku prędkości ruchu 
                     spowodowanym lokalnym zagęszczeniem ruchu. Cechą charakterystyczną jest zatłoczenie na drodze 
                     oraz zmienna prędkość - pojazdy raz po raz zmuszone są do hamowania aż do zatrzymania oraz ponownego ruszania i przyspieszania. 
                     Natężenie ruchu wymuszonego może oscylować od małego do dużego. Stan taki występuje często z powodu wypadków lub innych zdarzeń drogowych, 
                     zawężenia przekroju lub innych przyczyn obniżających przepustowość (tzw. lokalne ograniczenie przepustowości).
            ''')
            st.image("files\\congested_traffic.png")
    