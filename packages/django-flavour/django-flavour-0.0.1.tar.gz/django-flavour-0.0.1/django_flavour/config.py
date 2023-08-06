# -*- coding: utf-8 -*-
import importlib


def settings(config):
    pass
    # load all the other flavour enabled settings
    # read flavour.yml
    # get the addons
    addons = [
        "django_cloud_essentials"
    ]
    for addon in addons:
        a = importlib.import_module(addon)
        a.settings(config)

