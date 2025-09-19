import streamlit as st
import pandas as pd
from IGDBInteractive import IGDBInteraction
from api.api_wrapper import ApiWrapper

if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.GameDB = pd.DataFrame()
    st.session_state.themeCountD = {}
    st.session_state.genreCountD = {}

    st.session_state.Gm1Title = 'Game 1'
    st.session_state.Gm2Title = 'Game 2'
    st.session_state.Gm3Title = 'Game 3'
    st.session_state.RecDF = pd.DataFrame()

st.header('Video Game Recommendation Engine\nAuthor: Dante J. Smith, PhD')

@st.cache_data
def startUpScripts():

    # Set up API wrapper
    apim = ApiWrapper()

    # Request Access Token
    apim.requestAccessToken()

    # Load Game Data
    apim.loadGameData()
    apim.loadGameAdjData()

    # Make Games Recommendation Engine (GRE)
    GRE = IGDBInteraction()

    # Create games dataframe
    GRE.gameDF = pd.DataFrame(apim.gamesDict)
    GRE.themeDF = pd.DataFrame(apim.themeDict)
    GRE.genreDF = pd.DataFrame(apim.genreDict)

    # Fit the Games DataFrame to a KNN
    GRE.RecEng_FeatureFit()
    GRE.CreateSummaryInfo()

    return GRE

GRE = startUpScripts()
st.session_state.GameDB = GRE.gameDF
st.session_state.themeCountD = GRE.themeCountD
st.session_state.genreCountD = GRE.genreCountD

def displayGameInfo(title):
    st.markdown(f'#### {title}')

# Previously played Games Input BOX
st.markdown('''### Select Games that you have enjoyed playing!\n #### Hit enter after each selection''')
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Game #1")
    st.session_state.Gm1Title = st.text_input(label = 'Game1_input',
                                              key = 'Game1_input',
                                              label_visibility = 'hidden')
    GRE.selectPlayedGame(st.session_state.Gm1Title, 1)
    displayGameInfo(st.session_state.Gm1Title)
with col2:
    st.header("Game #2")
    st.session_state.Gm2Title = st.text_input(label = 'Game2_input',
                                              key = 'Game2_input',
                                              label_visibility = 'hidden')
    GRE.selectPlayedGame(st.session_state.Gm2Title, 2)
    displayGameInfo(st.session_state.Gm2Title)
with col3:
    st.header("Game #3")
    st.session_state.Gm3Title = st.text_input(label = 'Game3_input',
                                              key = 'Game3_input',
                                              label_visibility = 'hidden')
    GRE.selectPlayedGame(st.session_state.Gm3Title, 3)
    displayGameInfo(st.session_state.Gm3Title)

ComboFeatures = GRE.playedGamesIdxList[0]

if st.button('Generate Results'):
    st.session_state.recDF = GRE.makeRecommendations(GRE.features[ComboFeatures])
    st.dataframe(st.session_state.recDF)
