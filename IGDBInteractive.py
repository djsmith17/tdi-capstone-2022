import itertools
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.neighbors import NearestNeighbors
from DictEncoder import DictEncoder

class IGDBInteraction():
    ''' Class to handle interaction with IGDB data and make recommendations '''
    def __init__(self):

        self.playedGamesIdxList =  [0] * 3
        self.dispFeatures = ['id', 'name', 'themes', 'genres', 'total_rating']

        # Initialize empty dataframes to hold API data
        self.game_df = pd.DataFrame()
        self.theme_df = pd.DataFrame()
        self.genre_df = pd.DataFrame()

        # Initialize model attributes
        self.features = None
        self.nn = None

        # Initialize summary data attributes
        self.theme_count_df = {}
        self.genre_count_df = {}

    def selectPlayedGame(self, game_str, game_num):
        ''' Select a game that the user has played and store its index '''

        # Search for Game Text
        game_idx = self.search_game(game_str)
        # Return JSON for that game listing and save it in a dictionary for ref.
        self.playedGamesIdxList[game_num-1] = game_idx

    def search_game(self, game_str):
        ''' Search for a game in the game dataframe and return its index '''
        df_sub = self.game_df.loc[self.game_df['name'] == game_str]
        if not df_sub.empty:
            return df_sub.index[0]
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

        self.features = union.fit_transform(self.game_df)
        self.nn = NearestNeighbors(n_neighbors=10).fit(self.features)

    def makeRecommendations(self, features):
        dists, indices = self.nn.kneighbors(features)
        recDF = self.game_df.iloc[indices[0]][self.dispFeatures].sort_values(by = ['total_rating'], ascending = False)
        return recDF

    def PlayedGamesDF(self):
        return self.game_df.iloc[self.playedGamesIdxList][self.dispFeatures]

    def create_summary_info(self):
        """
        Generates summary information for themes and genres in the game dataset.

        This method processes the 'themes' and 'genres' columns in the game's DataFrame,
        extracting unique theme and genre IDs, converting them to their respective names,
        and counting the number of games associated with each theme and genre.
        The results are stored in two DataFrames: `self.theme_count_df` and `self.genre_count_df`,
        containing the names and counts of themes and genres, respectively.

        Returns:
            None
        """
        # Grab theme and genre data and drop the NA values
        theme_df = self.game_df['themes'].dropna()
        genre_df = self.game_df['genres'].dropna()

        # Find sets of theme/genre included in the database
        theme_set = set(itertools.chain.from_iterable(theme_df))
        genre_set = set(itertools.chain.from_iterable(genre_df))

        # Convert the category numbers to category names
        theme_names = [self.theme_df[self.theme_df['id']== x]['name'].to_string(index = False) for x in theme_set]
        genre_names = [self.genre_df[self.genre_df['id']== x]['name'].to_string(index = False) for x in genre_set]

        # Find theme counts and put it into a dataframe
        theme_counts = [sum([x in y for y in theme_df]) for x in theme_set]
        self.theme_count_df = pd.DataFrame({'Themes': theme_names, 'NumGames': theme_counts})

        # Find genre counts and put it into a dataframe
        genre_counts = [sum([x in y for y in genre_df]) for x in genre_set]
        self.genre_count_df = pd.DataFrame({'Genres': genre_names, 'NumGames': genre_counts})
