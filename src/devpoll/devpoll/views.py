import ptah_cms
from memphis import config, view, form
from pyramid.httpexceptions import HTTPFound

import app
import poll
import permissions


class AddPollForm(form.Form):
    view.pyramidView('addpoll.html', app.PollApplication)

    label = 'Add new poll'
    fields = poll.Poll.__type__.fieldset

    @form.button(u'Add poll', actype=form.AC_PRIMARY)
    def addHandler(self):
        data, errors = self.extract()

        if errors:
            self.message(errors, 'form-error')
            return

        p = poll.Poll(**data)
        ptah_cms.Session.add(p)
        ptah_cms.Session.flush()
        raise HTTPFound(location='%s/'%p.__id__)

    @form.button(u'Cancel')
    def cancelHandler(self):
        raise HTTPFound(location='.')


class ApplicationView(view.View):
    view.pyramidView(context = app.PollApplication,
                     permission = ptah_cms.View,
                     template = view.template('templates/app.pt'))

    def update(self):
        self.polls = self.context.values()


class PollView(view.View):
    view.pyramidView(route = 'devpoll-poll-view',
                     context = app.PollApplication,
                     template = view.template('templates/poll.pt'))

    def update(self):
        self.poll = poll.Poll.get(self.request.matchdict['id'])
