# -*- coding: utf-8 -*-
import os
import pathlib
import yaml


class Settings(object):
    _DEFAULT_SECTION = 'DEFAULT'

    BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

    TESTING = True
    SECRET_KEY = 'insecure-192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

    MEDIA_ROOT = BASE_DIR / 'media'
    UPLOAD_FOLDER = MEDIA_ROOT / 'uploads'

    def __init__(self):
        default_settings_file = self.BASE_DIR / 'etc' / 'config.yaml'

        settings_file = os.environ.get('TICKETS_SETTINGS_FILE', default_settings_file)
        if settings_file and os.path.exists(settings_file):
            self.configure(settings_file)

    def configure(self, config_file: str):
        with open(config_file, 'r', encoding='utf-8') as f:
            conf = yaml.load(f, Loader=yaml.SafeLoader)

        for section, part in conf.items():
            for key, value in part.items():
                if self._DEFAULT_SECTION == section:
                    key = key.upper()
                else:
                    key = f'{section}_{key}'.upper()

                setattr(self, key, value)


settings = Settings()
