""" addon system """
import os, os.path
import pkg_resources
from memphis import config, view, form
from memphis.config import directives

import ptah


ADDONS = []

@config.subscriber(config.SettingsInitialized)
def initAddons(ev):
    dir = os.path.join(os.getcwd(), 'addons')
    if not os.path.isdir(dir):
        return

    for item in os.listdir(dir):
        path = os.path.join(dir, item)

        for dist in pkg_resources.find_distributions(path, True):
            distmap = pkg_resources.get_entry_map(dist, 'memphis')
            if 'package' in distmap:
                ADDONS.append(dist)


class AddonModule(ptah.PtahModule):
    """ """

    title = 'Add-ons'
    ptah.manageModule('addons')


class AddonView(view.View):
    view.pyramidView(
        context = AddonModule,
        template = view.template('addon.pt'))

    def update(self):
        data = []

        for dist in ADDONS:
            data.append(dist)

        self.addons = data

        if 'form.button.install' in self.request.POST:
            for name in self.request.POST.getall('addon'):
                for dist in self.addons:
                    if dist.project_name == name:
                        dist.activate()
                        actions = directives.scan(name, set())
                        pkg_resources.working_set.add(dist)
                        for action in actions:
                            action()
