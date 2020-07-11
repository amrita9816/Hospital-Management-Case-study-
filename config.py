import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xe5K\xf5t\x15\xba\x9a,s\x999\xd4\x14\xd4\x80\x0f'
