import streamlit as st
from PIL import  Image
# Custom imports 
from multipage import MultiPage
import numpy as np
# from pages import reussite_general, reussite_numero_chance # import your pages here
import reussite_general,  reussite_timeslice, reussite_n_dernieres, gap_metrics, simulation
# Create an instance of the app 
app = MultiPage()

# Title of the main page

display = Image.open('fdj.jpg')
# display = np.array(display)
# st.image(display, width = 100)
col1, col2 = st.columns(2)
col2.image(display, width = 150)
col1.title("Super Statistiques Française des Jeux")

# Add all your applications (pages) here
app.add_page("Réussite totale", reussite_general.app)
app.add_page("Réussite par periode", reussite_timeslice.app)
app.add_page("Réussite sur les N derniers tirages", reussite_n_dernieres.app)
app.add_page("Écart", gap_metrics.app)
app.add_page("Simuler ma combinaison", simulation.app)

# The main app
app.run()