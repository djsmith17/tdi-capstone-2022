import streamlit as st
import itertools

st.set_page_config(page_title="Visualizations")

st.header('Video Game Recommendation Engine\nAuthor: Dante J. Smith, PhD')
st.markdown('### Visualizations of the Games included in the IGDB')

gameDF = st.session_state.GameDB
themeDF = st.session_state.themeDB
genreDF = st.session_state.genreDB

st.markdown(f'The IGDB contains entries for over **{len(gameDF)} video games!!**')

themeData = gameDF['themes']
genreData = gameDF['genres']
themeDataReal = themeData.dropna()
genreDataReal = genreData.dropna()

themeSet = set(itertools.chain.from_iterable(themeData.dropna()))
genreSet = set(itertools.chain.from_iterable(genreData.dropna()))

themeNames = [themeDF[themeDF['id']== x]['name'].to_string(index = False) for x in themeSet]
genreNames = [genreDF[genreDF['id']== x]['name'].to_string(index = False) for x in genreSet]

st.header('Game Themes')
Counts = [sum([x in y for y in themeDataReal]) for x in themeSet]
d = {'Themes': themeNames, 'NumGames': Counts}
st.bar_chart(data=d,  x='Themes', width = 500, height = 500)

st.header('Game Genres')
Counts = [sum([x in y for y in genreDataReal]) for x in genreSet]
d = {'Genres': genreNames, 'NumGames': Counts}
st.bar_chart(data=d,  x='Genres', width = 500, height = 500)