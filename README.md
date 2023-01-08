# AZ-Lyrics Scrapper

First step is to fill the database with artists
Then you need to fill that artist's 
items(albums and songs) again 5 elements for each.  

ATM, the filling method is dumb,
meaning if the artist is already in the database
calling fill endpoint will repopulate with
the same artists.

ATM, fills database with 5 artists names 
per letter.

ATM, no more than 2 songs lyrics per album 
are filled bc of timeout error.

------

# ToDo
[ ] User Login   
[ ] Smart fill   
[ ] Timeout error when getting lyrics   
[ ] Credits(for users to fill db, get songs, etc)  
[ ] Analytics   
[ ] Visualization   
[ ] Search for specific artist/song   
[ ] Something with Dataclass or Schemas, cant remember  
[ ] Check generators on Scrapper Service   
[ ] Check loggings message an location   
[ ] Fill lyrics might be async or thread?   
[ ] Check try and except locations  
[ ] Bulk update for Song table
[ ] Refactor fill lyrics   
[ ] Create tables at project init.
