# import audio player
import os
from time import sleep

# import user config
from config import LOG, OS_TYPE


def play_audio(path):
    if OS_TYPE == 'mac':
        os.system("afplay " + path)
    elif OS_TYPE == 'linux': 
        os.system("mpg123 " + path)
    else:
        raise Exception('Invalid os')


class Player:

    def __init__(self, uids):
        self.uids = uids
        self.index = 0
        self.run = False
        

    def start(self):

        while True:

            # delay 
            sleep(0.1)

            # if index is greater than uids, stop
            if self.index >= len(self.uids): break

            # grab the next uid
            uid = self.uids[self.index]

            # convert to path
            path = os.path.join(os.getcwd(), f'tmp/{uid}.wav')

            # if file does not exist, continue
            if not os.path.exists(path): continue
                
            # log
            if LOG: print(f'INFO: Playing {path}')
                
            # play audio
            play_audio(path)

            # delete
            os.remove(path)

            # increment index
            self.index += 1

        if LOG: print('INFO: Player exited successfully')
