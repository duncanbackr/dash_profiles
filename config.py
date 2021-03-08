import os

import environ

BASE_DIR = cwd = os.getcwd()
env_file = os.path.join(BASE_DIR, ".env")
SETTINGS_NAME = "creator-profiles"

if not os.path.isfile('.env'):
    import google.auth
    from google.cloud import secretmanager_v1 as sm

    _, project = google.auth.default()

    if project:
        client = sm.SecretManagerServiceClient()
        name = f"projects/{project}/secrets/{SETTINGS_NAME}/versions/latest"
        payload = client. \
            access_secret_version(name=name). \
            payload. \
            data.decode("UTF-8")

        with open(env_file, "w") as f:
            f.write(payload)

env = environ.Env()
env.read_env(env_file)


class Config:
    FLASK_APP = env.str('FLASK_APP')
    SECRET_KEY = env.str('SECRET_KEY')
    TESTING = env.bool('TESTING')
    BACKREST_URL = env.str('BACKREST_URL')
    LOCAL = env.bool('LOCAL')
    CREDENTIALS_PATH = env.str('CREDENTIALS_PATH')


# class Auth:
#     VALID_PASSWORD = env.str('VALID_PASSWORD')
#     VALID_USERNAME = env.str('VALID_USERNAME')
