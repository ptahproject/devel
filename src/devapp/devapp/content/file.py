""" file content implementation """
import sqlalchemy as sqla
from ptah import view, form

import ptah, ptah.cmsapp
from ptah import cms
from devapp.permissions import AddFile


class File(ptah.cms.Content):

    __tablename__ = 'ptah_cmsapp_files'

    __type__ = cms.Type(
        'file',
        title = 'File',
        description = 'A file in the site.',
        permission = AddFile,
        addview = 'addfile.html',
        )

    blobref = sqla.Column(
        sqla.Unicode,
        info = {'title': 'Data',
                'field_type': 'file',
                'uri': True})

    @cms.action(permission=cms.ModifyContent)
    def update(self, **data):
        """ Update file content. """
        fd = data.get('blobref')
        if fd:
            blob = ptah.resolve(self.blobref)
            if blob is None:
                blob = cms.blobStorage.create(self)
                self.blobref = blob.__uri__

            blob.write(fd['fp'].read())
            blob.updateMetadata(
                filename = fd['filename'],
                mimetype = fd['mimetype'])

        self.title = data['title']
        self.description = data['description']

    @cms.action(permission=cms.View)
    def data(self):
        """ Download data. """
        blob = ptah.resolve(self.blobref)
        if blob is None:
            raise cms.NotFound()

        return {'mimetype': blob.mimetype,
                'filename': blob.filename,
                'data': blob.read()}


class FileDownloadView(view.View):
    view.pview('download.html', File, layout=None,
               permission = cms.View)

    def render(self):
        data = self.context.data()

        response = self.request.response
        response.content_type = data['mimetype'].encode('utf-8')
        response.headerlist = {
            'Content-Disposition':
            'filename="%s"'%data['filename'].encode('utf-8')}
        response.body = data['data']
        return response


class FileView(FileDownloadView):
    view.pview(context = File, permission = cms.View)

    template = view.template('devapp:templates/file.pt')

    def update(self):
        self.resolve = ptah.resolve

    def render(self):
        if self.request.url.endswith('/'):
            return self.template(
                view = self,
                context = self.context,
                request = self.request)

        return super(FileView, self).render()


class FileAddForm(ptah.cmsapp.AddForm):
    view.pview('addfile.html', cms.Container)

    tinfo = File.__type__

    def chooseName(self, **kw):
        filename = kw['blobref']['filename']
        name = filename.split('\\')[-1].split('/')[-1]

        i = 1
        n = name
        while n in self.container:
            i += 1
            n = u'%s-%s'%(name, i)

        return n
