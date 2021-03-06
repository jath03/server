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
import tools

def main():
    # Create a Storage object. This object holds the credentials that your
    # application needs to authorize access to the user's data. The name of the
    # credentials file is provided. If the file does not exist, it is
    # created. This object can only hold credentials for a single user, so
    # as-written, this script can only handle a single user.
    c = tools.cookies(method='read')
    try:
        with open('/home/jack/projects/local/server/files/session.dat', 'r+b') as file:            
            d = pickle.load(file)
    except EOFError:
        d = None
    try:
        st = Storage('server', c['user'])
        if st.get() is not None:
            credentials = st.get()
    except TypeError:
        try:
            with open('/home/jack/projects/local/server/files/flow.dat', 'r+b') as f:
                flow = pickle.load(f)
                credentials = flow.step2_exchange(d['params']['code'])
        except (EOFError, TypeError):
            print('''\
<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
        <h3>You are not authenticated, Redirecting...</h3>
        <script>window.location="http://jath03.herokuapp.com/login"</script>
    </body>
</html>''') 
    try:
        # The get() function returns the credentials for the Storage object. If no
        # credentials were found, None is returned.
        # If no credentials are found or the credentials are invalid due to
        # expiration, new credentials need to be obtained from the authorization
        # server. The oauth2client.tools.run_flow() function attempts to open an
        # authorization server page in your default web browser. The server
        # asks the user to grant your application access to the user's data.
        # If the user grants access, the run_flow() function returns new credentials.
        # The new credentials are also stored in the supplied Storage object,
        # which updates the credentials.dat file.
        # Create an httplib2.Http object to handle our HTTP requests, and authorize it
        # using the credentials.authorize() function.
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
            with open('/home/jack/projects/local/.spy/data/gUsers.dat', 'ab') as f:
                pickle.dump(profile, f)
            if not c['user']:
                with open('/home/jack/projects/local/server/files/hds.dat', 'wb') as f:
                    pickle.dump('Set-Cookie: user={u}; Max-Age=2592000\r\n'.format(u=profile['id']), f)
            if profile['id'] != '101157566449352653116':
                print('''<!DOCTYPE html>
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
				<li><a href="fun.html">I'm bored</a></li>
			</ul>
		</div>
		<div id="section1">
			<h2>{name}'s profile</h2>
			<img src="{pic}" width=320 height=240 />
                        <p>Name: {name}</p>
			<p>Email: {email}</p>
			<p>Id: {id}</p>
		</div>
	</body>
</html>'''.format(name=profile['name'], pic=profile['picture'], email=profile['email'], id=profile['id']))
            else:
                print('''<!DOCTYPE html>

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
                                <li><a href="fun.html">I'm bored</a></li>
				<li><a href="http://jath03.herokuapp.com/projects">My projects</a></li>
                        </ul>
                </div>
                <div id="section1">
                        <h2>{name}'s profile</h2>
			<img src="{pic}" width=320 height=240 />
                        <p>Name: {name}</p>
                        <p>Email: {email}</p>
                        <p>Id: {id}</p>
                </div>
        </body>
</html>'''.format(name=profile['name'], pic=profile['picture'], email=profile['email'], id=profile['id'],
                  code=params['code']))
        except AccessTokenRefreshError:
            # The AccessTokenRefreshError exception is raised if the credentials
            # have been revoked by the user or they have expired.
            raise
    except Exception as error:
        print("""<!DOCTYPE html>
<html>
	<head>
	</head>
	<body>
		<h2>Error: {error}</h2>
		<p>Redirecting...</p>
		<script>window.location = "http://jath03.herokuapp.com/login";</script>
	</body>
</html>""".format(error=error))


if __name__ == '__main__':
    main()
