# django_kobo
Kobo Aggregator

# Config

Install Docker and Docker Compose
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

# Run

```./django_kobo.sh```

