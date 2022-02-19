# Sea Trader game
You are a trader in the sea. Your mission - try to get as many coins as you can in the trading season!

This is a homage for the famous Socher Hayam game by Matach - with new twists!


## Running game -
```bash
pip install -r requirements.txt
python3 main.py
```

## Running tests -
All tests are located at ```./tests``` folder.
```bash
python -m unittest discover -s tests
```

## Run as a docker container
The game requires interactive shell - make sure to include ```-it``` in the run command!
```bash
docker build -t sea_trader .
docker run -it sea_trader
```

## Log files + game setting
See file ```constants.py``` for logging files path + game settings
You can -
* Change cities list
* Add new products and change their settings
* Choose a file path for the logs file + game results save file
* Modify the ship properties


## You can find the original Socher HaYam game here -
https://www.old-games.org/games/socher1
