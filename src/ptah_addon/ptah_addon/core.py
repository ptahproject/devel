""" addon system """
import os, os.path
import pkg_resources
from ptah  import config
from ptah.config import directives

import ptah


ADDONS = {}

@config.subscriber(config.SettingsInitialized)
def initAddons(ev):
    dir = os.path.join(os.getcwd(), 'addons')
    if not os.path.isdir(dir):
        return

    for dist in pkg_resources.working_set:
        distmap = pkg_resources.get_entry_map(dist, 'ptah')
        if 'addon' in distmap:
            ADDONS[dist.project_name] = dist

    for item in os.listdir(dir):
        path = os.path.join(dir, item)

        for dist in pkg_resources.find_distributions(path, True):
            distmap = pkg_resources.get_entry_map(dist, 'ptah')
            if 'package' in distmap:
                ADDONS[dist.project_name] = dist
