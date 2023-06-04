from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.neighbors import NearestNeighbors
from DictEncoder import DictEncoder
import itertools

class IGDBInteraction():
    def __init__(self):

        self.playedGamesIdxList =  [0] * 3
        self.dispFeatures = ['id', 'name', 'themes', 'genres', 'total_rating']

    def selectPlayedGame(self, gameStr, gameNum):

        # Search for Game Text
        gameIdx = self.searchGame(gameStr)
        # Return JSON for that game listing and save it in a dictionary for ref.
        self.playedGamesIdxList[gameNum-1] = gameIdx

    def searchGame(self, gameStr):
        dfSubSet = self.gameDF.loc[self.gameDF['name'] == gameStr]
        if not dfSubSet.empty:
            return dfSubSet.index[0]
        else:
            return 1

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

    def CreateSummaryInfo(self):
        # Start creating some summary data for the visualizations. 
        # First let's find how many games of each theme/genre there are
        
        # Grab theme and genre data and drop the NA values
        themeData = self.gameDF['themes'].dropna()
        genreData = self.gameDF['genres'].dropna()

        # Find sets of theme/genre included in the database
        themeSet = set(itertools.chain.from_iterable(themeData))
        genreSet = set(itertools.chain.from_iterable(genreData))

        # Convert the category numbers to category names
        themeNames = [self.themeDF[self.themeDF['id']== x]['name'].to_string(index = False) for x in themeSet]
        genreNames = [self.genreDF[self.genreDF['id']== x]['name'].to_string(index = False) for x in genreSet]

        # Find theme counts and put it into a dataframe
        Counts = [sum([x in y for y in themeData]) for x in themeSet]
        self.themeCountD = {'Themes': themeNames, 'NumGames': Counts}

        # Find genre counts and put it into a dataframe
        Counts = [sum([x in y for y in genreData]) for x in genreSet]
        self.genreCountD = {'Genres': genreNames, 'NumGames': Counts}