import streamlit as st
import altair as alt
import plotly.graph_objects as go
from pathlib import Path

# page config
st.set_page_config(
    page_title="Polish highway capacity method",
    page_icon=":oncoming_automobile:",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

col = st.columns((3, 7), gap='medium')


with col[1]:
    pass

    st.markdown('#### Ocena warunków ruchu na odcinkach międzywęzłowych dróg dwujezdniowych')
    
    with st.expander("O metodzie"):
        st.markdown("""
            Metoda jest rezultatem projektu badawczego „Nowoczesne metody obliczania przepustowości i oceny warunków 
            ruchu dla dróg poza aglomeracjami miejskimi, w tym dla dróg szybkiego ruchu”, 
            realizowanego w ramach programu „Rozwój Innowacji Drogowych” w latach 2016-2019. 
            Metodę oceny dla odcinków międzywęzłowych opracowano na podstawie badań empirycznych realizowanych w latach 2016-2017 
            na odcinkach autostrad, dróg ekspresowych i dwujezdniowych dróg klasy GP i G. 
        """)
    
    with st.expander("Podstawowe pojęcia"):
        st.markdown("""
                    | Pojęcie ***symbol*** **[jednostka]** | Definicja 
                    | :------- | :---------
                    | **Gęstość rzeczywista** *k* [P/km] | liczba rzeczywistych pojazdów znajdujących się na odcinku drogi o długości 1 km |
                    | **Gęstość obliczeniowa** *k0* [E/h/pas] | średnia liczba pojazdów znajdujących się na odcinku pasa ruchu o długości 1 km, przeliczona na pojazdy umowne [E] |
                    
                    """)


# Gęstość wjazdów i wyjazdów g_wz to przypadająca na kilometr łączna liczba wjazdów i wyjazdów na odcinku drogi w danym kierunku ruchu. 
# Krytyczne obliczeniowe natężenie ruchu  Q_oki [E/h/pas] jest to największe godzinowe natężenie ruchu, wyrażone w pojazdach umownych na pas, przy którym może utrzymać się poziom swobody ruchu i. Po przekroczeniu natężenia krytycznego, warunki ruchu pogarszają się do PSR (i+1).
# Lokalne Ograniczenie Przepustowości LOP (ang. bottleneck) definiuje się jako miejsce zatłoczenia na drodze, w którym dopływający potok pojazdów jest większy niż przepustowość przekroju drogi w jednostce czasu, przez co tworzy się kolejka (nazwa stosowana potocznie „korek drogowy”). 
# Miarodajne godzinowe natężenie ruchu Q_m   [P/h] jest to pomierzone lub prognozowane, najmniejsze z największych 50 natężeń godzinowych w roku. Dla dróg dwujezdniowych natężenia podaje się osobno dla każdego kierunku.

# Natężenie ruchu Q [P/h] jest liczbą pojazdów rzeczywistych, które przejeżdżają przez dany przekrój poprzeczny w ustalonej jednostce czasu, najczęściej godzinie.
# Natężenie ruchu obliczeniowe Q_o [E/h/pas] lub [E/h] jest to natężenie ruchu w szczytowych 15-tu minutach w godzinie, wyrażone w pojazdach umownych na godzinę. Natężenie to reprezentuje obciążenie drogi w standardowy sposób z uwzględnieniem struktury rodzajowej ruchu, zmienności godzinowej oraz wpływu pochyleń podłużnych.
# Niezawodność to zdolność odcinka lub elementu drogi do spełnienia stawianych mu wymagań w określonym czasie i w określonych warunkach użytkowania. Z punktu widzenia użytkownika drogi, istotne jest czy i jak często dochodzi do zatłoczenia na drodze, które powoduje nadmierne wydłużenie czasu podróży. Miarami niezawodności mogą być: wydłużenie czasu podróży, częstość lub prawdopodobieństwo wystąpienia zatłoczenia.
# Odcinek międzywęzłowy dróg klasy A, S, GP to odcinek będący poza obszarem oddziaływania węzłów, na którym ruch nie jest zakłócony manewrami włączania, wyłączania, przeplatania.
# Odcinek przeplatania dróg klasy A, S i GP jest obszarem na węźle, na którym przecinają się potoki pojazdów: wjeżdżających i wyjeżdżających oraz poruszających się na wprost jezdnią główną. 
# Odcinek wjazdu, wyjazdu są to miejsca włączenia lub wyłączenia drogi łącznikowej do jezdni głównej, na którym krzyżują się dwa potoki ruchu
# Pojazd lekki jest to pojazd o dopuszczalnej masie całkowitej do 3,5 t. Do pojazdów lekkich zalicza się samochody osobowe i pojazdy dostawcze o masie do 3,5 t.
# Pojazd ciężki jest to pojazd o dopuszczalnej masie całkowitej powyżej 3,5 t. Do pojazdów ciężkich zalicza się pojazdy ciężarowe bez przyczep i z przyczepami/naczepami, autobusy oraz ciągniki rolnicze.
# Poziom swobody ruchu (PSR) to klasa warunków ruchu związana ze sprawnością i płynnością ruchu, uwzględniająca odczucia kierowców. Zakres zmienności warunków ruchu podzielono na 6 poziomów oznaczonych literami od A do F, przy czym PSR A odpowiada najlepszym, a PSR F najgorszym warunkom ruchu.
# Prędkość optymalna potoku pojazdów V_op (km/h) jest to prędkość przejazdu pojazdów przez odcinek drogi przy natężeniu ruchu równym przepustowości drogi.
# Prędkość w ruchu swobodnym V_sw (km/h) jest uśrednioną w określonym przedziale czasu prędkością przejazdu samochodów osobowych przez analizowany odcinek drogi w warunkach ruchu swobodnego, czyli przy braku utrudnień wynikających z obecności innych użytkowników drogi.
# Prędkość potoku ruchu V (km/h) jest to prędkość przejazdu pojazdów przez analizowany odcinek drogi, uśredniona w określonym przedziale czasowym. 
# Przepustowość obliczeniowa (bazowa) drogi C_o [E/h/pas] lub [E/h] to największa liczba pojazdów w przeliczeniu na pojazdy umowne, które mogą przejechać przez przekrój pasa drogi w jednym kierunku w ciągu godziny, w dobrych (bazowych) warunkach drogowo-ruchowych.
# Przepustowość drogi C  [P/h] - największa liczba pojazdów rzeczywistych, które mogą przejechać przez dany przekrój drogi w jednym kierunku w ciągu godziny w określonych warunkach drogowo-ruchowych oraz przy dobrych warunkach atmosferycznych.
# Stopień obciążenia drogi X jest stosunkiem natężenia ruchu do przepustowości drogi.
# Średni dobowy ruch roczny SDRR [P/dobę] jest to średni dobowy ruch pojazdów w roku, wyrażony liczbą pojazdów przejeżdżających przez dany przekrój drogi przez kolejne 24 godziny.
# Udział pojazdów ciężkich u_c jest stosunkiem natężenia pojazdów ciężkich do całkowitego natężenia ruchu w danym przekroju w ustalonej jednostce czasu, najczęściej godzinie. 
# Warunki drogowo-ruchowe to zespół czynników mogących wpływać na przepustowość lub płynność ruchu pojazdów, obejmujący między innymi: liczbę i szerokości pasów ruchu, pochylenia podłużne i konfigurację pasów ruchu oraz strukturę rodzajową pojazdów uczestniczących w ruchu.

                    # """)


    st.markdown("""
        The data was collected by **permanent traffic counting station** working continuously based on dual inductance loops detectors.
        The station, for each detected vehicle at the lane, registers time of passage, spot speed, class and its length.
    """)
    st.markdown("""
        The data was **aggregated to 10-min and hourly intervals** and supplemented with relevant information from external sources. The database comprises:
        - *traffic data*: mean speed, volume, calculated density, mean headways, by lane and vehicle class,
        - *time-related data*: date, time, day of week, and time of day (dawn, day, night, dusk),
        - *weather conditions*: air temperature, precipitation type and intensity, humidity, wind speed, and road surface condition.
    """)
    st.markdown("""
        *All visuals and tables refer to southbound traffic direction. 
        All variables are aggregated over carriageway cross-section, without dividing into lanes.*
    """)


with col[0]:
    
    st.markdown("""
                **Procedura oceny warunków ruchu**
                """)
    
    st.image("files//r4_online.png", width=400)
    