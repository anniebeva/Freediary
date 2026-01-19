import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


TRAINING_TYPE_FIELDS = {
    'pool': ['pool_size'],
    'gym': ['duration', 'kcal', 'avg_heartrate', 'max_heartrate'],
    'depth': ['location', 'temperature', 'wetsuit', 'weights_free']
}


EXERCISE_TYPE_FIELDS = {
    'pool': ['distance', 'reps', 'interval'],
    'gym': ['weight', 'sets', 'reps', 'rest_time'],
    'depth': ['depth', 'dive_time', 'rest_time']
}