import os
import streamlit as st
import pandas as pd
from IGDBInteractive import IGDBInteraction
from RecEngFileMgmt import RecEngFileMgmt
import gc

# if 'FiMg' not in st.session_state:
#     st.session_state.FiMg = 0

if 'Gm1Title' not in st.session_state:
    st.session_state.Gm1Title = 'Game 1'

if 'Gm2Title' not in st.session_state:
    st.session_state.Gm2Title = 'Game 2'

if 'Gm3Title' not in st.session_state:
    st.session_state.Gm3Title = 'Game 3'

st.header('Video Game Recommendation Engine\nAuthor: Dante J. Smith, PhD')

@st.experimental_memo
def startUpScripts():

    # Set Secrets
    from setStreamlitEnvVar import setTwitchEnvVar
    setTwitchEnvVar()

    # Pull out Env Var
    client_ID  = os.environ.get('TWITCH_CLIENTID', 'NA')
    client_SEC = os.environ.get('TWITCH_CLIENTSEC', 'NA')

    if (client_ID == 'NA') | (client_SEC == 'NA'):
        print('Could not find secret env variables')

    # Set up script for file managements
    FiMg = RecEngFileMgmt(client_ID, client_SEC)
    
    # Request Access Token
    FiMg.requestAccessToken()
    
    # Load Game Data 
    FiMg.gamesDict = FiMg.loadGameData()
    
    # Make Games Recommendation Engine (GRE)
    GRE = IGDBInteraction()
    # Create games dataframe
    GRE.gameDF = pd.DataFrame(FiMg.gamesDict)
    # Fit the Games DataFrame to a KNN 
    GRE.RecEng_FeatureFit()

    return GRE

# @st.experimental_memo
# def setGamesObj(gamesDict):


GRE = startUpScripts()
# GRE = setGamesObj(FiMg.gamesDict)

# # Make Games Recommendation Engine (GRE)
# GRE = IGDBInteraction()
# # Create games dataframe
# GRE.gameDF = pd.DataFrame(FiMg.gamesDict)
# # Fit the Games DataFrame to a KNN 
# GRE.RecEng_FeatureFit()

# Previously played Games Input BOX
# Please provide the names of three games that you have enjoyed recently!

col1, col2, col3 = st.columns(3)

with col1:
    st.header("Game #1")
    st.session_state.Gm1Title = st.text_input('', key = 'Game1')
    GRE.selectPlayedGame(st.session_state.Gm1Title, 1)
with col2:
    st.header("Game #2")
    st.session_state.Gm2Title = st.text_input('', key = 'Game2')
    GRE.selectPlayedGame(st.session_state.Gm2Title, 2)
with col3:
    st.header("Game #3")
    st.session_state.Gm3Title = st.text_input('', key = 'Game3')
    GRE.selectPlayedGame(st.session_state.Gm3Title, 3)

# Remind ourselves what these features look like: 
# st.dataframe(GRE.PlayedGamesDF())

ComboFeatures = GRE.playedGamesIdxList[0]

if st.button('Generate Results'):
    st.dataframe(GRE.makeRecommendations(GRE.features[ComboFeatures]))