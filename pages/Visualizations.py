import streamlit as st

st.set_page_config(page_title="Visualizations")

st.header('Video Game Recommendation Engine\nAuthor: Dante J. Smith, PhD')
st.markdown('### Visualizations of the Games included in the IGDB')

st.markdown(f'The IGDB contains entries for over **{len(st.session_state.GameDB)} video games!!**')

st.header('Game Themes')
st.bar_chart(data=st.session_state.themeCountD ,  x='Themes', width = 500, height = 500)

st.header('Game Genres')
st.bar_chart(data=st.session_state.genreCountD,  x='Genres', width = 500, height = 500)