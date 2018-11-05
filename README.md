# CARPE Surveys
CARPE survey website. Fetches data collected with Kobo Toolbox, runs various analysis and shows results on website.

# Config

Install [Docker](https://docs.docker.com/install) and [Docker Compose](https://docs.docker.com/compose/install/)

Register your app with ArcGIS Portal. Enter `http://<url>:<port>/oauth/complete/portal/` as redirect URI.

Create file `.env` in app folder. Add the following lines

```bash
SECRET_KEY=<your django key>
DEBUG=<True|Flase>
DB_NAME=<pg db name>
DB_USER=<pg user>
DB_PASSWORD=<pg password>
DB_HOST=<pg host>
DB_PORT=<pg port>
PORTAL_URL=<portal url>
CARPE_KEY=<arcgis portal app key>
CARPE_SECRET=<arcgis portal app secret>
```

# First Run

```./django_kobo.sh init```

follow the command promt
- confirm the static file collection
- and enter the admin user for your site

Afterwards logon to localhost/admin
create a new connection using your kobo Toolbox user name and password
enter 
host assets: https://kf.kobotoolbox.org/assets/
host api: https://kc.kobotoolbox.org/api/v1/


