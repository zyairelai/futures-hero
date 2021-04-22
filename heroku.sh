rm -rf __pycache__/
rm -rf screenshots/
rm -rf BTCUSDT/
rm -rf ETHUSDT/
rm -rf BNBUSDT/
rm -rf BCHUSDT/
rm README.md
rm test.py
rm check.py

heroku git:remote -a futures-hero
git push heroku master
heroku ps:scale worker=1
