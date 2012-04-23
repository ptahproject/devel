import ptah
import ptahcms
import sqlalchemy as sqla
from pyramid.httpexceptions import HTTPFound


class Link(ptahcms.Content):
    __tablename__ = 'ptah_cms_link'
    __type__ = ptahcms.Type('link', permission=ptahcms.AddContent)

    href = sqla.Column(sqla.Unicode(255))


#@ptah.view.pview(context=Link, permission=ptahcms.View)
def link_view(context, request):
    """ This is a default view for a Link model.
        If you have permission to edit it it will display the form.
        If you do not have ability to edit it; you will be redirected.
    """
    can_edit = ptah.checkPermission(ptahcms.ModifyContent, context)

    if can_edit:
        vform = ptah.form.DisplayForm(context, request) # needs better UI
        vform.fields = Link.__type__.fieldset
        vform.content = {
            'title': context.title,
            'description': context.description,
            'href': context.href}
        vform.update()
        # the below render() would display form html without enclosing layout
        #return vform.render()

        """
        this should render the display form with layout applied
        The layout is the "wrapping HTML" e.g. ptahcms.app layout you
        see at http://localhost:8080/
        """
        layout = view.query_layout(request, context)
        return layout(vform.render())

    raise HTTPFound(location=context.href)
