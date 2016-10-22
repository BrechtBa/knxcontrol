# Server

Create a virtual environment to hold the python dependencies
```
virtualenv -p python3 env
```

Activate the virtual environment with:
```
source env/bin/activate
```

Install python dependencies:
```
pip install ephem
pip install passlib
pip install PyJWT
pip install websocket-client
```

## Unit tests
To run unit tests cd to the tests folder and run
```
python all.py
```