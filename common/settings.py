# -*- coding: utf-8 -*-
import configparser
import os
import pathlib


class Settings(object):
    _DEFAULT_SECTION = 'DEFAULT'

    BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

    TESTING = True
    SECRET_KEY = 'insecure-192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

    MEDIA_ROOT = BASE_DIR / 'media'
    UPLOAD_FOLDER = MEDIA_ROOT / 'uploads'

    def __init__(self):
        settings_file = os.environ.get('TICKETS_SETTINGS_FILE')
        if settings_file:
            self.configure(settings_file)

    def configure(self, config_file: str):
        parser = configparser.ConfigParser()
        parser.read(config_file)

        for section in parser.sections():
            for key, value in parser.items(section):
                if self._DEFAULT_SECTION == section:
                    key = key.upper()
                else:
                    key = f'{section}_{key}'.upper()

                setattr(self, key, value)


settings = Settings()
