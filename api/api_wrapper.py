import os
import requests
import dill

class ApiWrapper:
    '''
    This class handles the API environment and calls required to 
    drive the analytics present in the data app
    '''
    def __init__(self):

        # Set/get environment variables for Twitch API
        self._set_env_var()

        self.filePath = os.path.dirname(__file__)
        self.pkdFilePath = os.path.join(self.filePath, 'pkd')

        if not os.path.exists(self.pkdFilePath):
            os.mkdir(self.pkdFilePath)

        self.pkd_Game_path = os.path.join(self.pkdFilePath, 'game-API.pkd')
        self.pkd_Theme_path = os.path.join(self.pkdFilePath, 'theme-API.pkd')
        self.pkd_Genre_path = os.path.join(self.pkdFilePath, 'genre-API.pkd')

        self.oauth2URL = 'https://id.twitch.tv/oauth2/token'
        self.gamesURL  = 'https://api.igdb.com/v4/games'
        self.themeURL  = 'https://api.igdb.com/v4/themes'
        self.genreURL  = 'https://api.igdb.com/v4/genres'

        # Retrieve the Access Token
        self._request_access_token()

        # Initialize empty dictionaries to hold API data
        self.games_dict = []
        self.theme_dict = []
        self.genre_dict = []

    def _set_env_var(self):
        '''
        Sets the values of the Twitch API environment variables.

        Arguments:
            None

        Returns:
            None
        '''

        # Check for existence of client ID and SECRET in environment variables
        client_id = os.environ.get('TWITCH_CLIENTID', 'Not Found')
        client_sc = os.environ.get('TWITCH_CLIENTSEC', 'Not Found')

        if (client_id == 'Not Found') | (client_sc == 'Not Found'):
            # Call up API secrets from txt file if not already found
            print('Environment Variables not found ')

            api_file = os.path.dirname(__file__) + '/APIKEY_TWITCH.txt'
            f = open(api_file, 'r', encoding='utf-8')
            client_id = str(f.readline()).strip()
            client_sc = str(f.readline()).strip()
            f.close()

            print('Setting API Environment Variables')
            os.environ['TWITCH_CLIENTID']  = str(client_id)
            os.environ['TWITCH_CLIENTSEC'] = str(client_sc)
        else:
            print('Environment Variables found')

        self._client_id = client_id
        self._client_sc = client_sc
        print('Environment Variables Set\n')

    def _request_access_token(self):
        '''
        Requests an access token from the Twitch API.
        '''
        print('Requesting Access Token')
        params = {'client_id': self._client_id,
                  'client_secret': self._client_sc,
                  'grant_type': 'client_credentials'}

        response = requests.post(self.oauth2URL, params=params, timeout=10)
        self._access_token = response.json()['access_token']
        self._bearer_access_token = f"Bearer {self._access_token}"
        print('Access Token Received\n')

    def load_game_data(self):
        """
        Loads game data into the instance variable `games_dict`.

        If a pickled file containing game data exists at `self.pkd_Game_path`, it loads
        the data from the file. Otherwise, it downloads the game data from the API specified
        by `self.gamesURL`, saves it as a pickle file, and then loads it into `self.games_dict`.

        Side Effects:
            - Sets `self.games_dict` to the loaded or downloaded game data.
            - May create or overwrite the pickle file at `self.pkd_Game_path`.

        """
        games_dict = []
        if os.path.exists(self.pkd_Game_path):
            games_dict = self.load_pickled_file(self.pkd_Game_path)
        else:
            games_dict = self.download_api_data(self.gamesURL)
            self.save_pickled_file(self.pkd_Game_path, games_dict)

        self.games_dict = games_dict

    def load_game_adj_data(self):
        """
        Loads theme and genre data for games, either from pickled files or by downloading from the
        API.

        This method checks if pickled files containing theme and genre data exist. If they do,
        it loads the data from these files. If not, it downloads the data from the specified
        API URLs and saves them as pickled files for future use. The loaded data is then assigned
        to the instance variables `self.theme_dict` and `self.genre_dict`.

        Attributes:
            self.pkd_Theme_path (str): Path to the pickled theme data file.
            self.pkd_Genre_path (str): Path to the pickled genre data file.
            self.themeURL (str): URL to download theme data from the API.
            self.genreURL (str): URL to download genre data from the API.
            self.theme_dict (list): Loaded theme data.
            self.genre_dict (list): Loaded genre data.
        """
        theme_dict = []
        genre_dict = []
        if os.path.exists(self.pkd_Theme_path):
            theme_dict = self.load_pickled_file(self.pkd_Theme_path)
        else:
            theme_dict = self.download_api_data(self.themeURL)
            self.save_pickled_file(self.pkd_Theme_path, theme_dict)

        if os.path.exists(self.pkd_Genre_path):
            genre_dict = self.load_pickled_file(self.pkd_Genre_path)
        else:
            genre_dict = self.download_api_data(self.genreURL)
            self.save_pickled_file(self.pkd_Genre_path, genre_dict)

        self.theme_dict = theme_dict
        self.genre_dict = genre_dict

    def load_pickled_file(self, pickle_dir):
        """
        Loads and returns a Python object from a pickled file using dill.

        Args:
            pickle_dir (str): The file path to the pickled file.

        Returns:
            object: The Python object loaded from the pickled file.

        Prints:
            Status messages indicating the start and completion of the loading process.
        """
        print('Loading Pickled Data')
        with open(pickle_dir, 'rb') as f:
            dict_out = dill.load(f)
        print('Finished Loading Data')
        return dict_out

    def save_pickled_file(self, pickle_dir, game_dict):
        """
        Serializes and saves the provided game dictionary to a file using dill.

        Args:
            pickle_dir (str): The file path where the pickled data will be saved.
            game_dict (dict): The dictionary containing game data to be pickled.

        Returns:
            None

        Side Effects:
            Writes a pickled file to the specified location.
            Prints a message indicating the pickling process has started.
        """
        print('Pickling Data')
        with open(pickle_dir, 'wb') as f:
            dill.dump(game_dict, f)

    def download_api_data(self, url):
        """
        Downloads data from the specified API endpoint in batches.

        Args:
            url (str): The API endpoint URL to send requests to.

        Returns:
            list: A list containing all entries retrieved from the API.

        Notes:
            - Uses pagination with a fixed batch size (limit) of 500.
            - Continues fetching data until the number of entries in the last batch
              is less than the batch size.
            - Requires valid 'Client-ID' and 'Authorization' headers set in the instance.
            - Prints progress messages to the console.
        """
        print('Download Started')
        headers = {'Client-ID': self._client_id,
                   'Authorization': self._bearer_access_token}

        game_collect = []
        set_offset = 0
        set_limit = 500
        stop = False
        while not stop:
            body = f'fields *; limit {set_limit}; offset {set_offset};'
            thisbatch = requests.post(url,
                                      headers=headers,
                                      data=body,
                                      timeout=10).json()
            game_collect.extend(thisbatch)
            set_offset += set_limit
            if len(thisbatch) < set_limit:
                stop = True
        print('Download Finished')
        print(f'Downloaded {len(game_collect)} entries')
        return game_collect
