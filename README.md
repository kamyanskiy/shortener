### One time URL Shortener

This application provides one time URL shorterner functionality. The short URL can be used the only once. 
After short URL was used, this short URL will be destroyed without possibility to recover it.
  
This application is based on Tornado web framework with Redis server backend.

Running app is here http://kamyanskiy.fvds.ru/ - use it without any payments, 
it's 100% free for you ;-) 

1. Start application:
```commandline
$ docker-compose up --build -d 

```

2. Open in browser **http://localhost**

3. Enter URL in form to get short link. Press Submit button.


It also possible to make **GET** request: 
```commandline
GET http://localhost/?url=https://kamyanskiy.github.io/
``` 


P.S. Q: Why I tried to that when in the world are +100500 sample apps like that ? 
     A: I don't know :-) Probably because of bad bad weather today.
     
     
     