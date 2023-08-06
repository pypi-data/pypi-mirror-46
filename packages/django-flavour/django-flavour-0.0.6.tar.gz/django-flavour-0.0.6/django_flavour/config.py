# -*- coding: utf-8 -*-


def settings(config):
    import importlib
    import libflavour
    from strictyaml import load
    from pathlib import Path

    with Path("flavour.yml").open("r") as yaml:
        yaml_data = load(yaml.read(), libflavour.schema.schema_project)

    for addon in yaml_data["addons"]:
        try:
            if "django-flavour" in addon:
                continue 
            a = importlib.import_module(str(yaml_data["addons"][addon]["settings"]["packagename"]))
            a.settings(config)
        except Exception as e:
            print(e)
