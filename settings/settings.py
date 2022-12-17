from os import path
from pathlib import Path
from environ import Env

ROOT_FOLDER = Path(__file__).parent.parent

env = Env(DEBUG=(bool, False),)
Env.read_env(path.join(ROOT_FOLDER, 'env/.env'))

# Must have environment variables
WEATHER_DATA_URL = env('WEATHER_DATA_URL')
WEATHER_LOCATION_ID = env('WEATHER_LOCATION_ID')
WEATHER_LOCATION_NAME = env('WEATHER_LOCATION_NAME')
GAS_PER_HOUR_FILE = env('GAS_PER_HOUR_FILE')
ELECTRICITY_PER_QUARTER_FILE = env('ELECTRICITY_PER_QUARTER_FILE')
GAS_PER_DAY_FILE = env('GAS_PER_DAY_FILE')

# Optional overwrites
HISTORIC_DATA_FOLDER = env('historic_data', default=path.join(ROOT_FOLDER, 'historic_data'))
