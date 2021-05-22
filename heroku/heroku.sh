heroku git:remote -a futures-hero
git push heroku master
heroku ps:scale worker=1
