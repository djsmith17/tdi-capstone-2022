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

    def loadGameData(self):
        gamesDict = []
        if os.path.exists(self.pkd_Game_path):
            gamesDict = self.loadPickledFile(self.pkd_Game_path)
        else:
            gamesDict = self.downloadAPIData(self.gamesURL)
            self.savePickleFile(self.pkd_Game_path, gamesDict)

        self.gamesDict = gamesDict

    def loadGameAdjData(self):
        themeDict = []
        genreDict = []
        if os.path.exists(self.pkd_Theme_path):
            themeDict = self.loadPickledFile(self.pkd_Theme_path)
        else:
            themeDict = self.downloadAPIData(self.themeURL)
            self.savePickleFile(self.pkd_Theme_path, themeDict)

        if os.path.exists(self.pkd_Genre_path):
            genreDict = self.loadPickledFile(self.pkd_Genre_path)
        else:
            genreDict = self.downloadAPIData(self.genreURL)
            self.savePickleFile(self.pkd_Genre_path, genreDict)

        self.themeDict = themeDict
        self.genreDict = genreDict

    def loadPickledFile(self, dir):
        print('Loading Pickled Data')
        with open(dir, 'rb') as f:
            dictOut = dill.load(f)
        print('Finished Loading Data')
        return dictOut

    def savePickleFile(self, dir, GameDict):
        print('Pickling Data')
        with open(dir, 'wb') as f:
            dill.dump(GameDict, f)

    def downloadAPIData(self, URL):
        print('Download Started')
        headers = {'Client-ID': self.client_ID, 'Authorization': self.bearerAT}

        gameCollect = []
        set_offset = 0
        set_limit = 500
        stop = False
        while not stop:
            BODY = f'fields *; limit {set_limit}; offset {set_offset};'
            thisbatch = requests.post(URL, 
                                    headers = headers, 
                                    data = BODY).json()
            gameCollect.extend(thisbatch)
            set_offset += set_limit
            if len(thisbatch) < set_limit:
                stop = True
        print('Download Finished')
        print(f'Downloaded {len(gameCollect)} entries')
        return gameCollect
