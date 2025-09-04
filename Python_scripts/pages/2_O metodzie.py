import streamlit as st

# page config
st.set_page_config(
    page_title="Polish highway capacity method",
    page_icon=":oncoming_automobile:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# błąd dostępu, jeśli nie wprowadzono hasła
if not st.session_state.get("logged_in", False):
    st.error("🚫 Brak dostępu. Wróć na stronę główną i zaloguj się.")
    st.stop()

col = st.columns((3, 7), gap='medium')


with col[1]:
    pass

    st.markdown('#### Ocena warunków ruchu na odcinkach międzywęzłowych dróg dwujezdniowych')
    
    with st.expander("O metodzie"):
        st.markdown("""
            Metoda jest rezultatem projektu badawczego „Nowoczesne metody obliczania przepustowości i oceny warunków 
            ruchu dla dróg poza aglomeracjami miejskimi, w tym dla dróg szybkiego ruchu”, 
            realizowanego w ramach programu „Rozwój Innowacji Drogowych” w latach 2016-2019 przez konsorcjum Politechniki Krakowskiej, Politechniki Gdańskiej i Politechniki Warszawskiej. 
            Metodę oceny dla odcinków międzywęzłowych opracowano na podstawie badań empirycznych realizowanych w latach 2016-2017 
            na odcinkach autostrad, dróg ekspresowych i dwujezdniowych dróg klasy GP i G w Polsce. 
        """)
    
    with st.expander("Podstawowe pojęcia"):
        st.markdown("""
                    | Pojęcie ***symbol*** **[jednostka]** | Definicja 
                    | :------- | :---------
                    | **Gęstość rzeczywista** *k* [P/km] | Liczba rzeczywistych pojazdów znajdujących się na odcinku drogi o długości 1 km. |
                    | **Gęstość obliczeniowa** *k$_{0}$* [E/h/pas] | Średnia liczba pojazdów znajdujących się na odcinku pasa ruchu o długości 1 km, przeliczona na pojazdy umowne [E]. |
                    | **Natężenie ruchu** *Q* [P/h] | Liczba pojazdów rzeczywistych, które przejeżdżają przez dany przekrój poprzeczny w ustalonej jednostce czasu, najczęściej godzinie. |
                    | **Miarodajne godzinowe natężenie ruchu** *Q$_{m}$ [P/h] | Pomierzone lub prognozowane, najmniejsze z największych 50 natężeń godzinowych w roku. Dla dróg dwujezdniowych natężenia podaje się osobno dla każdego kierunku. |
                    | **Natężenie ruchu obliczeniowe** *Q$_{0}$* [E/h/pas] | Natężenie ruchu w szczytowych 15-tu minutach w godzinie, wyrażone w pojazdach umownych na godzinę. Natężenie to reprezentuje obciążenie drogi w standardowy sposób z uwzględnieniem struktury rodzajowej ruchu, zmienności godzinowej oraz wpływu pochyleń podłużnych. |
                    | **Krytyczne obliczeniowe natężenie ruchu** *Q$_{0ki}$* [E/h/pas] | Największe godzinowe natężenie ruchu, wyrażone w pojazdach umownych na pas, przy którym może utrzymać się poziom swobody ruchu *i*. Po przekroczeniu natężenia krytycznego, warunki ruchu pogarszają się do PSR *(i+1)* |
                    | **Poziom swobody ruchu** *PSR* | Jest to klasa warunków ruchu związana ze sprawnością i płynnością ruchu, uwzględniająca odczucia kierowców. Zakres zmienności warunków ruchu podzielono na 6 poziomów oznaczonych literami od A do F, przy czym PSR A odpowiada najlepszym, a PSR F najgorszym warunkom ruchu. |
                    | **Prędkość w ruchu swobodnym** *V$_{sw}$* [km/h] | Uśredniona w określonym przedziale czasu prędkość przejazdu samochodów osobowych przez analizowany odcinek drogi w warunkach ruchu swobodnego, czyli przy braku utrudnień wynikających z obecności innych użytkowników drogi.
                    | **Prędkość potoku ruchu** *V* [km/h] | Prędkość przejazdu pojazdów przez analizowany odcinek drogi, uśredniona w określonym przedziale czasowym. 
                    | **Prędkość optymalna** *V$_{op}$* [km/h] | Prędkość przejazdu pojazdów przez odcinek drogi przy natężeniu ruchu równym przepustowości drogi.
                    | **Przepustowość** *C*  [P/h] | Największa liczba pojazdów rzeczywistych, które mogą przejechać przez dany przekrój drogi w jednym kierunku w ciągu godziny w określonych warunkach drogowo-ruchowych oraz przy dobrych warunkach atmosferycznych.
                    | **Przepustowość obliczeniowa (bazowa)** *C$_{0}$* [E/h/pas] | Największa liczba pojazdów w przeliczeniu na pojazdy umowne, które mogą przejechać przez przekrój pasa drogi w jednym kierunku w ciągu godziny, w dobrych (bazowych) warunkach drogowo-ruchowych.
                    | **Stopień obciążenia drogi** *X* | Jest stosunkiem natężenia ruchu do przepustowości drogi.
                    | **Średni dobowy ruch roczny** *SDRR* [P/dobę] | Jest to średni dobowy ruch pojazdów w roku, wyrażony liczbą pojazdów przejeżdżających przez dany przekrój drogi przez kolejne 24 godziny.
                    | **Udział pojazdów ciężkich** *u$_{c}$* | Jest stosunkiem natężenia pojazdów ciężkich do całkowitego natężenia ruchu w danym przekroju w ustalonej jednostce czasu, najczęściej godzinie. Pojazd ciężki jest to pojazd o dopuszczalnej masie całkowitej powyżej 3,5 t. Do pojazdów ciężkich zalicza się pojazdy ciężarowe bez przyczep i z przyczepami/naczepami, autobusy oraz ciągniki rolnicze.
                    | **Warunki drogowo-ruchowe** | Zespół czynników mogących wpływać na przepustowość lub płynność ruchu pojazdów, obejmujący między innymi: liczbę i szerokości pasów ruchu, pochylenia podłużne i konfigurację pasów ruchu oraz strukturę rodzajową pojazdów uczestniczących w ruchu.
        """)

    with st.expander("Zakres metody"):
        st.markdown("""
                Metoda ma zastosowanie do oceny warunków ruchu na **odcinkach międzywęzłowych** autostrad, dróg ekspresowych i dwujezdniowych dróg klasy GP (droga główna o ruchu przyspieszonym) i G (droga główna).  
                
                **Odcinki międzywęzłowe** to odcinki będące poza obszarem oddziaływania węzłów, tj. niezakłócone manewrami włączania, wyłączania i przeplatania. Obszar oddziaływania węzła przyjmuje się jako (patrz rysunek poniżej):  
                - obszar wjazdu: 450 m, mierzony od końca łuku kołowego na łącznicy, w kierunku ruchu,  
                - obszar wyjazdu: 450 m, mierzony od końca łuku kołowego na łącznicy, w kierunku przeciwnym do kierunku ruchu,  
                - obszar przeplatania: 150 m, mierzone od końca łuku kołowego na łącznicach, w obu kierunkach.  
        """)
        st.image("files\droga.png", width=600)

        st.markdown("""
                    Odcinki międzywęzłowe należy podzielić na odcinki jednorodne pod względem warunków drogowo-ruchowych. W szczególności, wymagana jest jednorodność geometryczna (liczba pasów ruchu, szerokość pasów ruchu oraz pasa awaryjnego, pochylenia podłużne), 
                    a także jednorodność metod zarządzania ruchem (prędkość dopuszczalna, zakaz wyprzedzania przez samochody ciężarowe, itd.).
                    """)

    with st.expander("Przygotowanie danych"):
        st.markdown("""
                Przed przystąpieniem do obliczeń należy zebrać informacje dotyczące:  
                - klasy drogi (A, S, GP lub G),  
                - liczby pasów ruchu w jednym kierunku (2 lub 3),  
                - lokalizacji drogi (obszar aglomeracyjny lub zamiejski),  
                - pochylenia podłużnego odcinka (w %),  
                - dostępności do drogi (gęstość wjazdów i wyjazdów),  
                - ograniczenia prędkości dopuszczalnej,  
                - rzeczywistych lub prognozowanych natężeń ruchu (SDR lub miarodajne godzinowe natężenie ruchu),  
                - udziału pojazdów ciężkich.
        """)

    with st.expander("Procedura obliczeń w aplikacji"):
        st.markdown("""
                    **Krok 1: Zebranie i wprowadzenie danych wejściowych**  
                        Dane wejściowe wprowadza się poprzez wybór opcji z listy rozwijanej lub wprowadzenie wartości liczbowej.  
                        
                    W przypadku natężenia ruchu, możliwe jest wprowadzenie:  
                    - średniego dobowego ruchu rocznego SDR (rzeczywistego lub prognozowanego, w zależności od rodzaju analizy) - w takim przypadku należy wskazać jaka jest zmienność sezonowa ruchu, z której wynika udział godziny miarodajnej w SDR.
                    - miarodajnego godzinowego natężenia ruchu 
                        - w przypadku, gdy dysponuje się danymi z pomiarów dla drogi istniejącej, należy wyznaczyć natężenie miarodajne zgodnie z instrukcją (rozdział 3.5.3)
                    
                    
                    **Krok 2: Wyznaczenie prędkości w ruchu swobodnym**  
                    Aplikacja oblicza prędkość ruchu swobodnym na podstawie parametrów: klasa drogi, prędkość dopuszczalna i gęstość wjazdów i wyjazdów. Wzory zdefiniowane są w rozdziale 4.2 instrukcji.

                    **Krok 3: Wyznaczenie obliczeniowego natężenia ruchu**  
                    Miarodajne godzinowe natężenie ruchu (wprowadzone bezpośrednio do programu lub obliczone przez program na podstawie SDR i zmienności sezonowej)
                    jest przeliczane na natężenie obliczeniowe, tj. wyrażone w pojazdach obliczeniowych na 1 pas ruchu. Program wylicza natężenie obliczeniowe na podstawie parametrów: natężenie miarodajne, liczba pasów ruchu, udział pojazdów ciężkich i pochylenie podłużne. 
                    Sposób obliczeń jest przedstawiony w rozdziale 3.6 instrukcji.
                    
                    **Krok 4: Określenie przepustowości bazowej i stopnia wykorzystania przepustowości**  
                    Parametrem, na podstawie którego wyznaczana jest przepustowość bazowa drogi jest prędkość w ruchu swobodnym. Tablica poniżej prezentuje przepustowości obliczeniowe dróg danej klasy w zależności od obliczonej w kroku 2 prędkości w ruchu swobodnym.
                    Przepustowości są podane dla prędkości z krokiem 5 km/h. W programie, w przypadku wartości pośrednich *V$_{sw}$*, wartości przepustowości są interpolowane. Z tabeli można odczytać ponadto prędkość optymalną, a więc prędkość występującą przy natężeniu ruchu równym przepustowości.

                    """)
        st.image("files//przepustowosc.png", width=700)

        st.markdown("""
                    Następnie, program wylicza stopień wykorzystania przepustowości X jako stosunek natężenia ruchu do przepustowości. Jeżeli X przekracza 1 oznacza to, że natężenie ruchu przekracza przepustowość drogi, występuje Poziom Swobody Ruchu PSR F,
                    a procedura nie jest dalej kontynuowana.
                    """)

        st.markdown("""
                    **Krok 5: Obliczenie średniej prędkości**  
                    Średnia prędkość ruchu obliczana jest w programie na podstawie skalibrowanego modelu Van Aerde, którego parametry zostały przyjęte w metodzie na podstawie badań ruchu.

                    **Krok 6: Wyznaczenie gęstości obliczeniowej**  
                    Gęstość obliczeniowa jest stosunkiem obliczeniowego natężenia ruchu (wyznaczonego w kroku 3) do średniej prędkości (wyznaczonej w kroku 5).

                    **Krok 7: Określenie PSR**   
                    Na podstawie gęstości wyznaczonej w kroku 6, określany jest Poziom Swobody Ruchu PSR. Tablica poniżej przedstawia wartości graniczne gęstości dla poszczególnych PSR.
                    """)

        st.image("files//psr.png", width=300)

        st.markdown("""
                    Program wyznacza ponadto natężenia krytyczne dla analizowanego odcinka, tj. graniczne obliczeniowe natężenia ruchu dla poszczególnych PSR.
                    """)

    with st.expander("Instrukcja oceny warunków ruchu (...)"):
        st.markdown("""
                    Instrukcja oceny warunków ruchu na drogach dwujezdniowych, na podstawie której realizowane są obliczenia w programie, dostępna jest w linku poniżej.
                    """)
        st.link_button("Instrukcja oceny warunków ruchu - DODAĆ LINK", url="")
        

with col[0]:
    
    st.markdown("""
                **Procedura oceny warunków ruchu**
                """)
    
    st.image("files//r4_online.png", width=400)
    