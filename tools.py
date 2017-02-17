#!/usr/bin/python3.5
import pickle, time

def log(data, filepath, timestamp=True):
    if timestamp == True:
        with open(filepath, 'ab') as f:
            pickle.dump(str(time.asctime()) + ' ---  ' + str(data), f) 
    else:
        with open(filepath, 'ab') as f:
            pickle.dump(str(data), f)
def cookies(cookie=None, method='read'):
    if method == 'read':
        with open('/home/jack/projects/local/server/files/cookies.dat', 'rb') as f:
            return pickle.load(f)
    elif method == 'write':
        with open('/home/jack/projects/local/server/files/cookies.dat', 'wb') as f:
            return pickle.dump(cookie, f)
    else:
        raise ValueError('method must be either \"read\" or \"write\"')
