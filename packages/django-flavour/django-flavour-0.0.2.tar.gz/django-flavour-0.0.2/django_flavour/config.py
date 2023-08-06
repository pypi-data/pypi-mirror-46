# -*- coding: utf-8 -*-
import importlib
import libflavour
from strictyaml import load
from pathlib import Path

def settings(config):
    pass
    # load all the other flavour enabled settings
    # read flavour.yml
    # get the addons
    addons = ["django_cloud_essentials"]

    with Path("flavour.yml").open("r") as yaml:
        yaml_data = load(yaml.read(), libflavour.schema.schema_addon)

    print(yaml_data)


    for addon in yaml_data["addons"]:
        try:
            a = importlib.import_module(addon["settings"]["packagename"])
            a.settings(config)
        except Exception as e:
            print(e)
