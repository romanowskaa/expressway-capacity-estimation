import streamlit as st

st.set_page_config(
    page_title="Przepustowość i warunki ruchu",
    page_icon=":oncoming_automobile:",
)

st.write("# Witamy w programie! :motorway:")

st.markdown(
    """
    Program służy do obliczeń przepustowości i oceny warunków ruchu na odcinkach międzywęzłowych autostrad, dróg ekspresowych i dwujezdniowych dróg klasy GP i G, na podstawie polskiej metody MOP-DZ, opracowanej w ramach projektu
    badawczego „Nowoczesne metody obliczania przepustowości i oceny warunków ruchu dla dróg poza aglomeracjami miejskimi, w tym dla dróg szybkiego ruchu”. Projekt był realizowany w latach 2016-2017
    przez konsorcjum Politechniki Krakowskiej, Politechniki Gdańskiej i Politechniki Warszawskiej w ramach Wspólnej Inicjatywy GDDKiA i NCBiR "Rozwój Innowacji Drogowych" (RID). 

"""
)

st.markdown("""
            :red[**Przed rozpoczęciem korzystania z programu należy zapoznać się z instrukcją zawierającą szczegółowy opis metody dla odcinków międzywęzłowych.**] 
            Program realizuje obliczenia zgodnie z metodą szczegółową opisaną w rozdziałach 3 i 4.
                    """)
st.link_button("Instrukcja oceny warunków ruchu - DODAĆ LINK", url="")