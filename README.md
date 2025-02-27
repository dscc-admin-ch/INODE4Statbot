# Statbot UI

This package contains the front- and back-end code for the Statbot UI.

## Running the Server

To run, first create a `.env` with the following variables:

	MODEL_NAME=[ModelName]
	MODEL_PATH="model_path"
	INFERENCE_SERVER_URL=[Onyxia service address]

Along with the database parameters:

	DB_HOST=
	DB_PORT=
	DB_SCHEMA=
	DB_PASS=
	DB_USERNAME=
	DB_DATABASE=

Then run `docker compose up` to build and start the server.

### Importing/Exporting User Data

Once the server is running, the logs, whitelist and user data will be stored in `./userdata`. To import existing data from a previous instance, place it in `./userdata` before startup. If no existing user data has been provided, create an `admin` account and password using the login screen after startup.

### Managing Access

The user whitelist and password reset functions can be accessed in a browser via the administrator control panel at `http://[URL]/admin`. Alternatively, the databases in `./userdata` can be modified directly.


## Statbot helm

For now, on onyxia just clone this repo, adapt the `values.yaml` and run: 

`helm install statbot ./statbot-helm/`

For now, ui is mapped to port 2000 (forced).
The current `nginx.default.conf` is using this config:

```
server {
        listen 2000 default_server;
        listen [::]:2000 default_server;

        root /usr/share/nginx/html;
        index index.html;

		location /
		{
			try_files $uri $uri/ /index.html =404;
		}

        location /api
		{
			proxy_pass http://api:5000/api;
			proxy_read_timeout 3600;
		}
}
```