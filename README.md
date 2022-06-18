# lgtv-remote

## To run:

Set IP of tv in .env file:
```
TV_IP=192.168.1.100
```

Set any flask environment variables:
```
FLASK_APP=lgtv-remote
FLASK_ENV=development
FLASK_RUN_PORT=5005
```

Run the following commands:

```
python3 -m venv [virtual_environment_dir]
source [virtual_environment_dir]/bin/activate
pip install -r requirements.txt
```

Then navigate to the [ip]:5000, accept the confirmation on the screen, and you're on your way!
