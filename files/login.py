from apiclient.discovery import build
from oauth2client import tools
from oauth2client.contrib.keyring_storage import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets as FFC
import httplib2
import json
import pathlib
import subprocess
import pickle
import os
import io
import tools

def main(d):
  cookies = tools.cookies(method='read')
  w = json.loads(str(os.environ['GOOGLE-CLIENT-SECRETS']).replace('\'', '\"'))
  with open('/tmp/client_secrets.json', 'w') as f:
    json.dump(w, f)
  try:
    st = Storage('server', cookies['user'])
  except:
    st = None
  if cookies is None or st is None or st.get() is None:
    try:
      flow = FFC('/tmp/client_secrets.json', scope=('https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'), redirect_uri='http://jath03.herokuapp.com/{}'.format(str(d['params']['redirect'])))
    except (KeyError, TypeError) as err:
      flow = FFC('/tmp/client_secrets.json', scope=('https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'), redirect_uri='http://jath03.herokuapp.com')
    yield flow
    auth_uri = flow.step1_get_authorize_url()
  else:
    try:
      auth_uri = 'http://jath03.herokuapp.com/' + str(d['params']['redirect'])
    except:
      auth_uri = 'http://jath03.heorkuapp.com/'

  print('''<!DOCTYPE html>
<html>
	<head>
		<script>
                    "use strict";
                    function sleep(ms) {{
                        return new Promise(resolve => setTimeout(resolve, ms));
                    }}
                    async function foo() {{
                        sleep(5000);
                        window.location = "{}";
                    }}
                    foo();
                </script>
	</head>
	<body>
	</body>
</html>'''.format(auth_uri))
