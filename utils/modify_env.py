import dotenv

def modify_env(key, value):
    dotenv_file = dotenv.find_dotenv()

    dotenv.set_key(dotenv_file, key, value)