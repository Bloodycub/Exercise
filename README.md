# How to Use

## Starting point
- Open CMD in the Location of Gittask.py Folder

## Crate New OAuth App
- [Create New Oauth App](https://github.com/settings/applications/new)
- Fill in the following information:
  - Name your Application.
  - Home URL: http://127.0.0.1:5000
  - Optional Application description.
  - Authorization callback URL: http://127.0.0.1:5000/callback

- Generate a new client secret after creating the OAuth app.
- Retrieve the Client ID and Client Secret from Developer Settings.
- Save the Client ID and Client Secret in a secure location.
- [Get Client ID, Client Secret](https://github.com/settings/developers) Keys

## Input In CMD
### For Windows
```bash
set CLIENT_ID=(YOUR CLIENT ID)
set CLIENT_SECRET=(YOUR CLIENT SECRETKEY)
python Gittask.py
```
## Example
```bash
set CLIENT_ID=112cba423423423423423
set CLIENT_SECRET=f36ab06708324234234234234
python Gittask.py
```
- After the Server starts up, Navigate to the Homepage
- http://localhost:5000/ or http://localhost:5000/login

### [Navigate to Homepage](http://localhost:5000/)
## Navigation

- Navigate by buttons or via URL
- NOTE: Navigation only succeeds after login

## Endpoints:
```bash
127.0.0.1:5000 # Index
127.0.0.1:5000/login # Login in Github
127.0.0.1:5000/profile # Show own profile
127.0.0.1:5000/gettoken # Show Access token
127.0.0.1:5000/search # Show all repos
127.0.0.1:5000/starrepos # Show Stared repos
```

## Pips
```
pip install -r requirements.txt
```

## Docker Build Process
Open Docker desktop. To download docker, [Docker dowenload](https://www.docker.com/products/docker-desktop/)
  - Make Sure Docker is Running

```bash
cd /path/to/your/
docker build -t {your_image_name} .

- Example: docker build -t gittask .
```

- now take a sip of coffee for 10sec

## Docker Running
```bash
docker run -e CLIENT_ID=(your_client_id) -e CLIENT_SECRET=(your_client_secret) -p 5000:5000 {your_image_name}
```
- After pressing 'Enter,' the server is now running. Please note that there should be no text after pressing 'Enter.'

- Example: docker run -e CLIENT_ID=112cbaf2342348 -e CLIENT_SECRET=f36ab0670823522345 -p 5000:5000 gittask
