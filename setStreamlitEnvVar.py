import os

def setTwitchEnvVar():
    APIFile = os.path.dirname(__file__) + '\\APIKEY_TWITCH.txt'
    f = open(APIFile, 'r')
    client_ID = str(f.readline()).strip()
    client_SEC = str(f.readline()).strip()
    f.close()

    print('Setting Twitch Env Vars')
    os.environ['TWITCH_CLIENTID'] = str(client_ID)
    os.environ['TWITCH_CLIENTSEC'] = str(client_SEC)

if __name__ == '__main__':
    setTwitchEnvVar()