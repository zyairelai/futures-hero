heroku git:remote -a futures-hero
git add .
git commit -m "heroku"
git push heroku master
heroku ps:scale worker=1
