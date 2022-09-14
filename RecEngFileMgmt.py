import os
import requests
import dill

class RecEngFileMgmt():
    def __init__(self, client_ID, client_SEC):
        self.client_ID = client_ID
        self.client_SEC = client_SEC

        self.filePath = os.path.dirname(__file__)
        self.pkdFilePath = os.path.join(self.filePath, 'pkd')

        if not os.path.exists(self.pkdFilePath):
            os.mkdir(self.pkdFilePath)

        self.pkd_Game_path = os.path.join(self.pkdFilePath, 'game-API.pkd')

        self.playedGamesIdxList =  [0] * 3

        self.dispFeatures = ['id', 'name', 'themes', 'genres', 'total_rating']

        self.oauth2URL = 'https://id.twitch.tv/oauth2/token'
        self.gamesURL  = 'https://api.igdb.com/v4/games'

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
            gamesDict = self.downloadAPIData()
            self.savePickleFile(self.pkd_Game_path, gamesDict)
        return gamesDict

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

    def downloadAPIData(self):
        print('Download Started')
        headers = {'Client-ID': self.client_ID, 'Authorization': self.bearerAT}

        gameCollect = []
        set_offset = 0
        set_limit = 500
        stop = False
        while not stop:
            BODY = f'fields *; limit {set_limit}; offset {set_offset}; where parent_game = null;'
            thisbatch = requests.post(self.gamesURL, 
                                    headers = headers, 
                                    data = BODY).json()
            gameCollect.extend(thisbatch)
            set_offset += set_limit
            if len(thisbatch) < set_limit:
                stop = True
        print('Download Finished')
        print(f'Downloaded {len(gameCollect)} entries')
        return gameCollect