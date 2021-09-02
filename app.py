import streamlit as st
from PIL import  Image
# Custom imports 
from multipage import MultiPage
import numpy as np
# from pages import reussite_general, reussite_numero_chance # import your pages here
import reussite_general, reussite_numero_chance, reussite_timeslice, reussite_n_dernieres, gap_metrics, demo
# Create an instance of the app 
app = MultiPage()

# Title of the main page

display = Image.open('fdj.jpg')
# display = np.array(display)
# st.image(display, width = 100)
col1, col2 = st.beta_columns(2)
col2.image(display, width = 150)
col1.title("Super Statistiques Française des Jeux")

# Add all your applications (pages) here
app.add_page("Reussite totale", reussite_general.app)
app.add_page("Reussite par periode", reussite_timeslice.app)
app.add_page("Reussite sur les N derniers tirages", reussite_n_dernieres.app)
app.add_page("Ecart", gap_metrics.app)
app.add_page("Simuler ma combinaison", demo.app)

# The main app
app.run()