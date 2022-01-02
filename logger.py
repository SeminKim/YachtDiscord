from config import ENABLE_LOGGING


def put_log(text):
    if ENABLE_LOGGING:
        with open(f'data/log.txt', 'a') as f:
            f.write(text)
    return
