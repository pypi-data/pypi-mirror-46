# -*- coding: utf-8 -*-
import os

def settings(config):
    from getenv import env
    config["BASE_DIR"] = env("BASE_DIR", required=True)
    config["DATA_ROOT"] = env(
        "DATA_ROOT", os.path.join(config["BASE_DIR"], "data")
    )
    config["SECRET_KEY"] = env("SECRET_KEY", "this-is-not-very-random")
    config['ALLOWED_HOSTS'] = env('ALLOWED_HOSTS', ['localhost', '0.0.0.0', '*'])
    config["SITE_ID"] = env("SITE_ID", 1)
