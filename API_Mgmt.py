import os
import requests
import dill

class API_Mgmt():
    # This class handles the API environment and calls required to 
    # drive the analytics present in the data app
    def __init__(self):

        client_ID  = os.environ.get('TWITCH_CLIENTID', 'Not Found')
        client_SEC = os.environ.get('TWITCH_CLIENTSEC', 'Not Found')

        if (client_ID == 'Not Found') | (client_SEC == 'Not Found'):
            # Call up API secrets from txt file if not already found
            print('Environment Variables not found ')
            client_ID, client_SEC = self.setEnvVar()
        else:
            print('Environment Variables found')

        self.client_ID = client_ID
        self.client_SEC = client_SEC

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

    def setEnvVar(self):
        APIFile = os.path.dirname(__file__) + '/APIKEY_TWITCH.txt'
        f = open(APIFile, 'r')
        client_ID = str(f.readline()).strip()
        client_SEC = str(f.readline()).strip()
        f.close()

        print('Setting API Environment Variables\n')
        os.environ['TWITCH_CLIENTID']  = str(client_ID)
        os.environ['TWITCH_CLIENTSEC'] = str(client_SEC)

        return client_ID, client_SEC

    def requestAccessToken(self):
        params = {'client_id': self.client_ID, 'client_secret': self.client_SEC, 'grant_type': 'client_credentials'}
        response = requests.post(self.oauth2URL, params = params)
        self.AT = response.json()['access_token']
        self.bearerAT = 'Bearer ' + self.AT

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