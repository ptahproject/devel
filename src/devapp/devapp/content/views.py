from zope import interface
from ptah import view, form, config
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

import ptah
from ptah import auth_service, cms


#listing_template = view.template("devapp:templates/listing.pt")


@view_config(
    context=ptah.cms.Container,
    wrapper=ptah.wrap_layout(),
    renderer='devapp:templates/listing.pt')
class ContainerListing(view.View):

    def update(self):
        context = self.context
        request = self.request
        registry = request.registry

        self.deleteContent = ptah.check_permission(
            cms.DeleteContent, context)

        # cms(uri).read()
        # cms(uri).create(type)
        # cms(uri).delete()
        # cms(uri).update(**kwargs)
        # cms(uri).items(offset, limit)

        if self.deleteContent and 'form.buttons.remove' in request.POST:
            uris = self.request.POST.getall('item')
            for uri in uris:
                cms.wrap(uri).delete()

                self.message("Selected content items have been removed.")

        if 'form.buttons.rename' in request.POST:
            uris = self.request.POST.getall('item')
            print '=============', uris

        if 'form.buttons.cut' in request.POST:
            uris = self.request.POST.getall('item')
            print '=============', uris


#class ViewContainer(ContainerListing):
#    view.pview(context = ptah.cms.Container,
#               template = listing_template)


#class RenameForm(view.View):
#    view.pview(
#        'rename.html', cms.Container,
#        template=view.template("devapp:templates/folder_rename.pt"))


class Adding(view.View):
    #view.pview('+', ptah.cms.Container)

    #template=view.template("devapp:templates/adding.pt")

    def update(self):
        self.url = self.request.resource_url(self.context)

        types = [(t.title, t) for t in
                 self.context.__type__.list_types(self.context)]
        types.sort()

        self.types = [t for _t, t in types]

    def render(self):
        subpath = self.request.subpath
        if subpath and subpath[0]:
            tname = subpath[0]
            tinfo = cms.get_type('cms-type:%s'%tname)
            if tinfo is None:
                raise HTTPNotFound

            form = AddContentForm(tinfo, self, self.request)
            form.update()
            return form.render()

        return super(Adding, self).render()


class AddContentForm(cms.AddForm):

    def __init__(self, tinfo, form, request):
        super(AddContentForm, self).__init__(form, request)

        self.tinfo = tinfo
        self.container = form.context
