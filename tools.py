#!/usr/bin/python3.5
import pickle, time, sys
from io import StringIO

def log(data, filepath, timestamp=True):
    if timestamp == True:
        with open(filepath, 'ab') as f:
            pickle.dump(str(time.asctime()) + ' ---  ' + str(data), f) 
    else:
        with open(filepath, 'ab') as f:
            pickle.dump(str(data), f)
def cookies(cookie=None, method='read'):
    if method == 'read':
        with open('/app/files/cookies.dat', 'rb') as f:
            return pickle.load(f)
    elif method == 'write':
        with open('/app/files/cookies.dat', 'wb') as f:
            return pickle.dump(cookie, f)
    else:
        raise ValueError('method must be either \"read\" or \"write\"')

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
