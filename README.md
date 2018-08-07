[![Build Status](https://travis-ci.com/crunis/mastermind_api.svg?branch=master)](https://travis-ci.com/crunis/mastermind_api)
# Mastermind API server

Server that handles mastermind games

## RUNNING THE APP

### RUN THE APP USING DOCKER-COMPOSE

If you have Docker and docker-compose installed, just run:

```
docker-compose up
```

Default configuration has the server listening on port 8080

This will pull and run 3 containers:

- **crunis/mastermind**: container with the mastermind api server. Please take a look at the provided Dockerfile to see how this image is built
- **library/redis**: official redis container image. The mastermind API server stores game information in redis
- **library/nginx**: official nginx container image. I'm using nginx as a proper gw to our app. It connects to the app using FastCGI.



### RUN THE APP FROM THE COMMANDLINE

Don't forget to install all necessary packages:

```
sudo pip install -r requirements.txt
```

If you execute the app directly you will have to indicate where your Redis server is:

```
REDIS_HOST=200.32.15.23 REDIS_PORT=6363 python server.py
```

Remember your can quickly launch a local redis server using docker:

```
docker run -p 6379:6379 redis
REDIS_HOST=127.0.0.1 python server.py
```

Default configuration has the server listening on port 8080

## API ENDPOINTS

### CREATE NEW GAME
This endpoint creates a new game, returning the corresponding game_id.

The API endpoint is:
```
/games [POST]
```

This will return a JSON with the **game_id** of the created game, for example:
```
$ curl -X POST  http://localhost:8080/games
{"game_id": "1533678277959254"}
```

### QUERY A GUESS 
This endpoint allows to make a guess, and returns the number of blacks and whites obtained.

The API endpoint is:
```
/games/<game_id>/guess [POST]
params:
  guess: string - guess of the code, is a 4-digit string build with the digits 1-6, for example: "1134"
```
Returns a JSON with the number of black ('b' key) and whites ('w' key). For example:
```
$ curl -d'{"guess":"5522"}' -H "Content-Type: application/json" -X POST  http://localhost:8080/games/1533678277959254/guess
{"b": 2, "w": 1}
```

### GET THE HISTORIC OF GUESSES AND RESPONSES
This endpoint returns the full historic of guesses with their responses for a game

The API endpoint is:
```
/games/<game_id>/historic [GET]
```

For example:
```
$ curl http://localhost:8080/games/1533678277959254/historic
{"alphabet": "123456", "length": 4, "historic": [{"ts": 1533676261.8311884, "guess": "1111", "b": 0, "w": 0}, {"ts": 1533676270.8240309, "guess": "2222", "b": 1, "w": 0}, {"ts": 1533676277.741756, "guess": "2233", "b": 0, "w": 1}, {"ts": 1533676298.455014, "guess": "3344", "b": 0, "w": 0}, {"ts": 1533676322.3685536, "guess": "2255", "b": 1, "w": 2}, {"ts": 1533676362.1079507, "guess": "5522", "b": 2, "w": 1}, {"ts": 1533676397.294603, "guess": "2552", "b": 3, "w": 0}, {"ts": 1533676442.2439208, "guess": "6552", "b": 4, "w": 0}]}
```

**alphabet** provides the valid digits for the code and **length** the length of the code. Currently this is always "123456" and 4 digits, but most of the code is ready to support other alphabets and lengths.
**historic** key contains an array with all the guesses, for each entry, it contains **ts** (timestamp of the guess), the **guess** made, **b**, number of blacks, and **w**, number of whites obtained with that guess.