import aiohttp
from aiohttp import web
import os

GITHUB_CLIENT_ID = os.environ['CLIENT_ID']  # Github Client ID
GITHUB_CLIENT_SECRET = os.environ['CLIENT_SECRET']  # Github Client secret key
GITHUB_REDIRECT_URI = 'http://localhost:5000/callback'  # Github Handshake
GITHUB_AUTH_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_API_URL = 'https://api.github.com/user'  # Your Username
GITHUB_SEARCH_URL = 'https://api.github.com/search/repositories'  # All repos

async def index(request):  # Home Page With Buttons Navigate.
    return web.Response(
    text='<p><h2>How To Use Login: <a href="/login">http://localhost:5000/login</a> or Click <a href="/login">Login</a> For Login</h2></p>'
         '<h2>Get Token ID: <a href="/gettoken">http://localhost:5000/gettoken</a> or Click <a href="/gettoken">Get Token</a> For Token</h2>'
         '<p><h2>Starred Repositories: <a href="/starrepos">http://localhost:5000/starrepos</a> or Click <a href="/starrepos">Get Star Repositories</a> For Star repositories<h2></p>'
         '<p><h2>Search Repositories: <a href="/search">http://localhost:5000/search</a> or Click <a href="/search">To Search Repositories</a><h2></p>',
    content_type='text/html'
)

async def login(request):  # Hand Shake With Github
    endpoint = request.query.get('endpoint') # Use the GitHub auth state parameter for transferring data about the redirect endpoint URL.

    if not endpoint:
        endpoint = '/profile' # Default endpoint
    oauth_login_url = f'https://github.com/login/oauth/authorize?scope=repo&client_id={GITHUB_CLIENT_ID}&state={endpoint}' # Github Auth with Client ID and Token
    return web.HTTPFound(oauth_login_url) # Redirecting

async def callback(request: web.Request):  # Requesting authorization
    code = request.query.get('code')  # User code = user ID
    state = request.query.get('state', '') # Transferring token if no token default value ''

    async with aiohttp.ClientSession() as session: # Creating session
        async with session.post(GITHUB_TOKEN_URL,
                                params={'client_id': GITHUB_CLIENT_ID,
                                        'client_secret': GITHUB_CLIENT_SECRET,
                                        'code': code},
                                headers={'Accept': 'application/json'}) as response:
            data = await response.json()  # Gets User Data And saves it as LIST
    access_token = data['access_token'] # Getting Access token
    return web.HTTPFound(f'{state}?access_token={access_token}') # Returning Access token

async def userprofile(request:web.Request):  # Shows own profile
    access_token = request.query.get('access_token', None) # Getting token if empty return None
    headers = {'Authorization': f'Bearer {access_token}'} # Gives Access token

    if access_token is None:  # Checks if You're authenticated in.
        return web.HTTPFound('/login?endpoint=/profile')  # Redirect to Login Web

    async with aiohttp.ClientSession() as session:
        async with session.get(GITHUB_API_URL, headers=headers) as response: # Getting Api With Key(Access token)
            user_data = await response.json()  # Gets User Data saves in User_data

    if not user_data: # Check If found user data
        return web.Response(text='Something went wrong', content_type='text/html')

    return web.Response(# Returning data Getting Login name and User ID.
         text=f'<h1>Hello, {user_data["login"]}!</h1><p>ID: {user_data["id"]}</p>'
         f'<h2>Home Page: <a href="http://localhost:5000">http://localhost:5000</a> or Click <a href="http://localhost:5000">Home Page</a> For Home Page</h2>',
    content_type='text/html'  # Converts to HTML
    )

async def profile(access_token): # Returns all user data in JSON format
    headers = {'Authorization': f'Bearer {access_token}'} # Gets Auth with token
    async with aiohttp.ClientSession() as session:
        async with session.get(GITHUB_API_URL, headers=headers) as response:
            user_data = await response.json()  # Gets User Data

    if not user_data: # Check If found user data
        return web.Response(text='Something went wrong', content_type='text/html')

    return user_data # Return JSON user data

async def gettoken(request):  # Gets user Token
    access_token = request.query.get('access_token', None)

    if access_token is None:  # Checks if You're authenticated in.
        return web.HTTPFound('/login?endpoint=/gettoken')  # Redirect to Login Web

    return web.Response(text=f'<h2>Access Token: {access_token}</h2>', content_type='text/html')  # Returns Token And shows it in HTML

async def search(request):  # Search ALL repos
    access_token = request.query.get('access_token', None) # Getting token if empty return None

    if access_token is None:  # Checks if You're authenticated in.
        return web.HTTPFound('/login?endpoint=/search')  # Redirect to Login Web

    headers = {'Authorization': f'Bearer {access_token}'} # header key
    async with aiohttp.ClientSession() as session:
        user_data = await profile(access_token) # Getting JSON data with token access
        url = f'https://api.github.com/users/{user_data['login']}/repos'  # User API that contains login
        async with session.get(url, headers=headers) as data_response:
            repo = await data_response.json()  # Saving in repo all after 'login' data

    if not user_data: # Check If found user data
        return web.Response(text='Something went wrong', content_type='text/html')

    repo_list = []  # Creating an empty list
    repo_amount = len(repo)  # Calculating how many repos
    for repo_data in repo:  # Sorting Repos by filters
        if not repo_data['topics']:  # if repo 'topics' is empty export this
            repo_info = {
                'name': repo_data['name'],
                'description': repo_data['description'],
                'html_url': repo_data['html_url'],
                'fork': repo_data['fork'],
                'license': repo_data['license'],
                'stargazers_count': repo_data['stargazers_count']
            }
        else:  # else print with topics
            repo_info = {
                'name': repo_data['name'],
                'description': repo_data['description'],
                'topics': ', '.join(repo_data['topics']),
                'html_url': repo_data['html_url'],
                'fork': repo_data['fork'],
                'license': repo_data['license'],
                'stargazers_count': repo_data['stargazers_count']
            }
        repo_list.append(repo_info)  # Modify skin repo list

    html_content = f'<h2>Repository Amount: {repo_amount}</h2>'  # Convert response_data to HTML content

    for repo_info in repo_list:  # Convert to HTML all from Repo_list
        html_content += f'''
        <div>
            <strong>Name:</strong> {repo_info['name']}<br>
            <strong>Description:</strong> {repo_info['description']}<br>
            {'<strong>Topics:</strong> ' + repo_info['topics'] + '<br>' if 'topics' in repo_info else ''}
            <strong>URL:</strong> <a href='{repo_info['html_url']}'>{repo_info['html_url']}</a><br>
            <strong>Fork:</strong> {repo_info['fork']}<br>
            <strong>License:</strong> {repo_info['license']}<br>
            <strong>Stargazers Count:</strong> {repo_info['stargazers_count']}<br><br>
        </div>
        '''

    return web.Response(text=html_content, content_type='text/html')  # Return as HTML

async def starrepos(request):  # Show Starred Repos
    access_token = request.query.get('access_token', None) # Getting token if empty return None

    if access_token is None:# Check if access token != None
        return web.HTTPFound('/login?endpoint=/starrepos')  # Redirect to Login Web

    user_data = await profile(access_token) # Gets Userdata JSON

    if not user_data: # Check If found user data
        return web.Response(text='Something went wrong', content_type='text/html')

    user_name = user_data['login'] # Finding from JSON format Login name
    url = f'https://api.github.com/users/{user_name}/starred'  # Shows all starred repos

    async with aiohttp.ClientSession() as session:
        repo_list = []  # Empty List
        headers = {'Authorization': f'Bearer {access_token}'}

        async def fetch_page(url):  # Get Url data
            async with session.get(url, headers=headers) as data_response:
                return await data_response.json()  # Return json Data

        starred_repos = await fetch_page(url)  # Fetch the first page
        repo_list.extend(starred_repos)  # Extends repo list

        # Check for additional pages
        while 'Link' in session._default_headers and 'rel="next"' in session._default_headers['Link']:
            next_page_url = session._default_headers['Link'].split(';')[0][1:-1]
            next_page_repos = await fetch_page(next_page_url)
            repo_list.extend(next_page_repos)

        repo_amount = len(repo_list)  # Get Repos amount

        html_content = f'<h2>Starred Repositories Amount: {repo_amount}</h2>'  # Convert response_data to HTML content

        for repo_info in repo_list: # Looping list for printing in HTML
            if not repo_info['topics']: # remove {}
                repo_info['topics'] = 'N/A' # replace with N/A

            if repo_info['private']: # if Repo is private skip printing data
                continue # skip this loop

            html_content += f'''
            <div>
                <strong>Name:</strong> {repo_info['name']}<br>
                <strong>Description:</strong> {repo_info['description']}<br>
                <strong>Topics:</strong> {repo_info['topics']}<br>
                <strong>URL:</strong> <a href='{repo_info['html_url']}'>{repo_info['html_url']}</a><br>
                <strong>Private:</strong> {repo_info['private']}<br>
                <strong>Fork:</strong> {repo_info['fork']}<br>
                <strong>License:</strong> {repo_info['license']}<br>
                <strong>Stargazers Count:</strong> {repo_info['stargazers_count']}<br><br>
            </div>
            '''

        return web.Response(text=html_content, content_type='text/html') # Return HTML format

# Commands to navigate and Endpoints.
app = web.Application()
app.router.add_get('/', index)
app.router.add_get('/login', login)
app.router.add_get('/callback', callback)
app.router.add_get('/profile', userprofile)
app.router.add_get('/gettoken', gettoken)
app.router.add_get('/search', search)
app.router.add_get('/starrepos', starrepos)

if __name__ == '__main__':
    print('Server is starting...')
    web.run_app(app, port=5000) # Run local host at port :5000
