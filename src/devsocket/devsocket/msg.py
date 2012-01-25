import ptah
import logging

logger = logging.getLogger('devsocket')


@ptah.subscriber(ptah.events.ContentEvent)
def contentEvent(ev):
        MSG.send('%s: %s'%(ev.__class__.__name__, ev.object.title))
