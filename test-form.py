from pprint import pprint
from memphis import form
from ptah_app.content import Page

def action1(form):
    print ('action1', form)

def action2(form):
    print ('action2', form)

eform = form.Form(None, None)
eform.params = {}
eform.method = 'params'
eform.fields = Page.__type__.fieldset

eform.buttons.addAction('Test submit', name='ac1', action=action1)
eform.buttons.addAction('Test action2', name='ac2', action=action2)

print "==== execute action1 ===="
eform.params = {'%sbuttons.ac1'%eform.prefix: 'value'}
eform.update()

print
print "==== extract data ====="
data, errors = eform.extract()

print
print "DATA:"
pprint(data)

print
print "ERRORS:"
pprint(errors)
