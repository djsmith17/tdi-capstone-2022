import os
import streamlit as st
import pandas as pd
from IGDBInteractive import IGDBInteraction
from RecEngFileMgmt import RecEngFileMgmt

if 'FiMg' not in st.session_state:
    st.session_state.FiMg = 0

st.header('Video Game Recommendation Engine\nAuthor: Dante J. Smith, PhD')

@st.experimental_memo
def startUpScripts():

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
    
    return FiMg

st.session_state.FiMg = startUpScripts()

# Make Games Recommendation Engine (GRE)
GRE = IGDBInteraction()
# Create games dataframe
GRE.gameDF = pd.DataFrame(st.session_state.FiMg.gamesDict)
# Fit the Games DataFrame to a KNN 
GRE.RecEng_FeatureFit()

# Previously played Games Input BOX
# Please provide the names of three games that you have enjoyed recently!

GRE.selectPlayedGame('The Elder Scrolls III: Morrowind', 1)
GRE.selectPlayedGame('Pillars of Eternity', 2)
GRE.selectPlayedGame("Baldur's Gate", 3)

# Remind ourselves what these features look like: 
st.dataframe(GRE.PlayedGamesDF())

if st.button('Generate Results'):
    st.dataframe(GRE.makeRecommendations(GRE.features[198244]))