import os
import requests
import json
import dill
import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.neighbors import NearestNeighbors
from DictEncoder import DictEncoder

from os.path import exists
from PIL import Image

class IGDBInteraction():
    def __init__(self):

        self.filePath = os.path.dirname(__file__)
        self.pkd_Game_path = os.path.join(self.filePath, 'pkd/game-API.pkd')

        self.playedGamesIdxList =  [0] * 3

        self.dispFeatures = ['id', 'name', 'themes', 'genres', 'total_rating']

        self.oauth2URL = 'https://id.twitch.tv/oauth2/token'
        self.gamesURL  = 'https://api.igdb.com/v4/games'

    def selectPlayedGame(self, gameStr, gameNum):

        # Search for Game Text
        gameIdx = self.searchGame(gameStr)

        # Return JSON for that game listing and save it in a dictionary for ref.
        self.playedGamesIdxList[gameNum-1] = gameIdx

    def searchGame(self, gameStr):
        dfSubSet = self.gameDF.loc[self.gameDF['name'] == gameStr]
        gameInd = dfSubSet.index[0]
        return gameInd

    def RecEng_FeatureFit(self):
        print('Running fit/transform for features in DataFrame')
        themes_pipe = Pipeline([('encoder', DictEncoder('themes')),
                                ('vectorizer', DictVectorizer())])

        genre_pipe = Pipeline([('encoder', DictEncoder('genres')),
                               ('vectorizer', DictVectorizer())])

        union = FeatureUnion([('themes', themes_pipe),
                              ('genre', genre_pipe)])

        self.features = union.fit_transform(self.gameDF)
        self.nn = NearestNeighbors(n_neighbors=10).fit(self.features)

    def makeRecommendations(self, features):
        dists, indices = self.nn.kneighbors(features)
        recDF = self.gameDF.iloc[indices[0]][self.dispFeatures].sort_values(by = ['total_rating'], ascending = False)
        return recDF

    def PlayedGamesDF(self):
        return self.gameDF.iloc[self.playedGamesIdxList][self.dispFeatures]