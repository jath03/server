from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets as FFC
import httplib2
import json
import pathlib
import webbrower
flow = FFC('/home/jack/.creds/client_secrets.json', scope='https://www.googleapis.com/auth/userinfo.email', redirect_uri='http://localhost:6789/callback')



def main():
  auth_uri = flow.step1_get_authorize_url()
  
  http = httplib2.Http()
  http = credentials.authorize(http)

  # The apiclient.discovery.build() function returns an instance of an API service
  # object can be used to make API calls. The object is constructed with
  # methods specific to the calendar API. The arguments provided are:
  #   name of the API ('calendar')
  #   version of the API you are using ('v3')
  #   authorized httplib2.Http() object that can be used for API calls
  service = build('oauth2', 'v2', http=http)
  try:
    profile = service.userinfo().v2().me().get().execute()
    '''print("""<!DOCTYPE html>

<html>
	<head>
		<link type="text/css" rel="stylesheet" href="style.css">
		<title>Jack.com</title>
	</head>
	<body>
		<div id="header">
			<h1>Jack's Website</h1>
		</div>
		<div id="nav">
                        <h4>Hello, {name}</h4>
			<ul>
				<li><a href="sites.html">My favorite sites</a></li>
				<li><a href="secret-fake.html">Secret site</a></li>
				<li><a href="fun.html">I'm bored</a></li>
			</ul>
		</div>
		<div id="section1">
			<h2>{name}'s profile</h2>
			<img src="{pic}" width=320 height=240 />
                        <p>Name: {name}</p>
			<p>Email: {email}</p>
		</div>
	</body>
</html>
""".format(name=profile['name'], pic=profile['picture'], email=profile['email']))'''
  except AccessTokenRefreshError:
    # The AccessTokenRefreshError exception is raised if the credentials
    # have been revoked by the user or they have expired.
    print ('The credentials have been revoked or expired, please re-run'
           'the application to re-authorize')

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    subprocess.run(['sudo rm /home/jack/.creds/credentials.dat'])
