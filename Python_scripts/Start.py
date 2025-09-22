import streamlit as st

st.set_page_config(
    page_title="Polish highway capacity method",
    page_icon=":oncoming_automobile:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.write("# Witamy w programie! :motorway:")

st.markdown(
    """
    Program służy do obliczeń przepustowości i oceny warunków ruchu na **odcinkach międzywęzłowych autostrad, dróg ekspresowych i dwujezdniowych dróg klasy GP i G**, na podstawie polskiej metody MOP-DZ, 
    opracowanej w ramach projektu badawczego „Nowoczesne metody obliczania przepustowości i oceny warunków ruchu dla dróg poza aglomeracjami miejskimi, w tym dla dróg szybkiego ruchu”.
    Projekt był realizowany w latach 2016-2017 przez konsorcjum Politechniki Krakowskiej, Politechniki Gdańskiej i Politechniki Warszawskiej w ramach Wspólnej Inicjatywy GDDKiA i NCBiR "Rozwój Innowacji Drogowych" (RID). 

"""
)




if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.markdown("### :arrow_left: Podaj hasło, aby korzystać z programu ")

with st.sidebar:
    if not st.session_state.logged_in:
        st.markdown("### Podaj hasło, aby korzystać z programu :arrow_heading_down:")
        password = st.text_input("🔑 Podaj hasło:", type="password")
        if password == st.secrets["APP_PASSWORD"]:
            st.session_state.logged_in = True
            st.success("✅ Dostęp przyznany – możesz teraz korzystać z aplikacji")
        elif password:
            st.error("❌ Nieprawidłowe hasło")

if not st.session_state.logged_in:
    st.stop()


st.markdown("""
            ##### :red[:warning: **Przed rozpoczęciem korzystania z programu należy zapoznać się z instrukcją zawierającą szczegółowy opis metody dla odcinków międzywęzłowych.**] 
            Program realizuje obliczenia zgodnie z metodą szczegółową opisaną w rozdziałach 3 i 4.
            """)
st.link_button("Instrukcja oceny warunków ruchu - DODAĆ LINK", url="")

