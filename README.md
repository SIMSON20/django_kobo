# CARPE Surveys
CARPE survey website. Fetches data collected with Kobo Toolbox, runs various analysis and shows results on website.

# Config

## Docker

Install [Docker](https://docs.docker.com/install) and [Docker Compose](https://docs.docker.com/compose/install/)

## Social oAuth with ArcGIS Portal
Register your app with ArcGIS Portal. Enter `http://<url>:<port>/oauth/complete/portal/` as redirect URI.

You can add additional social auth providers (ie Google, Facebook, Twitter) as needed.
Follow the instruction here

https://python-social-auth.readthedocs.io/en/latest/configuration/django.html#orms

https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html

If you decide to not use Social Login, you can deactivate this option.
You will need to make the following changes to the django settings file at app/kobo_project/settings.py

`AUTHENTICATION_BACKENDS`: remove the entry `custom_auth.portal.PortalOAuth2'`

remove all of the following settings:
```
SOCIAL_AUTH_POSTGRES_JSONFIELD
SOCIAL_AUTH_LOGIN_REDIRECT_URL
SOCIAL_AUTH_LOGIN_ERROR_URL
SOCIAL_AUTH_URL_NAMESPACE
SOCIAL_AUTH_PORTAL_KEY
SOCIAL_AUTH_PORTAL_SECRET
```

in app/templates/registration/login.html remove the line
```
<hr>
<a href="{% url "social:begin" "portal" %}" class="btn btn-default carpe-login" style="width:100%;">{% trans "or sign in with CARPE" %}</a>
```

## SSL
Create a private and public SSL key for your server. If you run the application behind a reverse proxy, 
you can use a self-signed certificate. Just make sure your reverse proxy accepts it.
If you expose the app directly, your certificate must be signed by a trusted Authority and DNS entry must match your server URL. 
Name the public certificate `certificate.crt` and the private key `certificate.key` and place both files in the root directory (same folder as the Dockerfile).

## Environment settings
Rename `.env.example` to `.env` in app folder. Update the attributes as followed:


|Attribute|Description|
|---------|-----------|
|SECRET_KEY| Some random String. You will need this to debug your site in your webbrowser. If you don't know what to put her just generate a random UUID |
|DEBUG  |true/ false, should be false when run in production |
|SERVER_URL| The URL of your webserver, if you use a reverse proxy, use the URL of the proxy |
|SERVER_IP| The public IP of the server running the app |
|LOG_LEVEL| When running in production set to INFO or WARNING | 
|URI_PREFIX| URI underwhich the app will be accessible on your server. I if you want your app to be accessible at gis.forest-atlas.org/surveys, type in `surveys` |
|DB_NAME| The name of the database your want to use. It will be created inside your docker container. If you don't know what to put in here, just use `django` |
|DB_USER| The user of the above database. If you don't know what to put in here, just use `django` |
|DB_PASSWORD| The password for the above user. If you don't know what to put in here, just generate a random UUID |
|DB_HOST| The host name of your database server. By default it is created inside your docker container and must be `postgis`|
|DB_PORT| By default use `5432` |
|PORTAL_URL| The URL to your ArcGIS Portal used for Social oAuth |
|PORTAL_KEY | The ArcGIS portal key for your app |
|PORTAL_SECRET | The ArcGIS portal secret for your app |


# First Run

## Install and configure Django
Start your docker container like this
```
./django_kobo.sh init
```
follow the command prompt
- confirm the static file collection
- and enter the admin user for your site. This user will be your site superuser.

It might happen that your PostgreSQL cluster is not yet ready when you first launch the site. 
Django will through an error and won't be able to complete the installation. 
In that case, simply stop your docker container and run the `init` command again.  

## Link you app to Kobo Toolbox

- Open you site (usually localhost/prefix/ or mydomain.com/prefix)
- Login using the super user password
- In the user menu select `Admin`. This will take you to the django backoffice


Create a new connection using your kobo Toolbox user name and password

- Go to "Connections" in the KOBO menu section
- Add a new connection
    - Auth user: Your Kobo user name
    - Auth pass: Your Kobo Password 
    - Host assets: https://kf.kobotoolbox.org/assets/
    - Host api: https://kc.kobotoolbox.org/api/v1/
    
Afterwards select your connection, go to "Action", select "Sync data" and click "Go"

This should fill the BNS Forms, BNS Forms - Prices and NRGT Forms tables in the corresponding menu sections.
Open this tables, select the surevy you want to download, go to "Action", select "Sync data" and click "Go".
Afterwards you will be able to see your data on your website.

The app will priodically check, if new data are available on Kobo. It will then update the data on your server.
Any local changes will be overwritten by the data coming from Kobo. 

If you want to keep your local changes, you can unlink your data with the data on Kobo.

Go to "BNS Forms", "BNS Forms - Prices" or "NRGT Forms", select the survey you want to unlink. Deselect the option "Kobo managed" and click "save".


## Allow other users to view data
By default, other uses cannot see detailed data from any survey. 
To give a user access to a survey, go to Kobo users, click on the user you want to give access.
Afterwards, select a survey and move it to the right hand side. The user should now be able to see the data. 


