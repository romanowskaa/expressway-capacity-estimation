# Streamlit app for calculating road capacity and assessing traffic conditions
@author: romanowskaa
## The scope
The [app](https://mop-dz.streamlit.app/) calculates road traffic parameters and assesses traffic conditions on basic sections of dual-carriageway roads with uninterrupted traffic (motorways, expressways and the sections of dual-carriageway highways). The calculations are based on the Polish highway capacity method (2019), developed based on empirical reasearch conducted in Poland in 2016-2017. The method is described in the [article](https://www.researchgate.net/publication/347890137_Development_of_the_new_Polish_method_for_capacity_analysis_of_motorways_and_expressways) and was developed by the team of researchers from the Technical Universitites of Cracow, Gdansk and Warsaw. The calculations requires the user to give number of input parameters, e.g. road class, number of lanes, the share of heavy vehicles, etc.

## Python scripts

### backend.py
The file contains the class of methods to calculate road and traffic parameters, and, at the end, assess the level of traffic conditions.

### Start.py
The app homepage. The user is required to give password to use the app.

### pages/1_Ocena warunkow ruchu.py
In the page, on the sidebar, the user is required to give input parameters. The results of caluclations are displayed on the right, in the form of (1) metrics with main traffic parameters, (2) visual with speed-flow relationship for the given road section with actual traffic state, (3) table with critical flows (traffic flows for the given levels-of-service).

### pages/2_O metodzie.py
In the page, the method and calculation steps are described.

