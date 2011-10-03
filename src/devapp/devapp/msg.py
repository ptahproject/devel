""" ploud mainenenance support """
import sys, logging, time
import Queue, httplib, urlparse, urllib, threading, socket

import ptah, ptah_cms
from memphis import config

logger = logging.getLogger('plone.utils')

MSG = None


#@config.subscriber(ptah_cms.ContentEvent)
#def contentEvent(ev):
#    global MSG
    #if MSG is not None:
    #    MSG.send('%s: %s'%(ev.__class__.__name__, ev.object.title))


#@config.subscriber(config.SettingsInitialized)
#def initialized(ev):
#    global MSG
    #if ev.config:
    #    MSG = MSGService()

#@config.shutdownHandler
#def shutdown():
#    global MSG
    #if MSG is not None:
    #    MSG.stopThreads()


class MSGService(object):

    def __init__(self, host='localhost:9090', timeout=30, backlog=10000,
                 postfix=''):
        self.timeout = timeout
        self.queue = Queue.Queue(backlog)
        self.worker = Worker(self.queue, host, self)
        self.worker.start()
        self.backlog = backlog
        self.postfix = postfix

    def send(self, msg):
        self.queue.put((True, msg), block=False)

    def stopThreads(self, wait=False):
        if not self.worker.stopping:
            self.worker.stopping = True
            self.queue.put(None, block=False)

        ok = True
        if wait:
            self.worker.join(5)
            if self.worker.isAlive():
                logger.warning(
                    "Worker thread %s failed to terminate", self.worker)
                ok = False
        return ok

    def _purgeSync(self, conn, host, msg):
        conn._http_vsn = 11
        conn._http_vsn_str = 'HTTP/1.1'

        conn.putrequest(
            'GET', '/broadcast?%s'%urllib.urlencode({'message': msg}),
            skip_accept_encoding=True)
        conn.endheaders()
        resp = conn.getresponse()


class Worker(threading.Thread):
    """Worker thread"""

    def __init__(self, queue, host, producer):
        self.host = host
        self.producer = producer
        self.queue = queue
        self.stopping = False

        super(Worker, self).__init__(name="Maintenance for http://%s" % host)

    def stop(self):
        self.stopping = True

    def run(self):
        q = self.producer.queue
        connection = None
        try:
            while 1:
                item = q.get()
                if item is None: # Shut down thread signal
                    logger.debug('Stopping worker thread for %s'%self.host)
                    break
                host, msg = item

                # Loop handling errors (other than connection errors)
                for i in range(5):
                    # Get a connection.
                    if connection is None:
                        connection = self.getConnection()
                        if connection is None: # stopping
                            break
                    # Got an item, purge it!
                    try:
                        self.producer._purgeSync(connection, host, msg)
                        connection.close()
                        connection = None
                        break
                    except (httplib.HTTPException, socket.error), e:
                        logger.debug('Transient failure on %s for %s, '
                                     're-establishing connection and '
                                     'retrying: %s' % (httpVerb, url, e))
                        connection.close()
                        connection = None
                    except Exception:
                        connection.close()
                        connection = None
                        import traceback
                        traceback.print_exc()
                        break
        except:
            logger.exception('Exception in worker thread %s' % self.host)
            import traceback
            traceback.print_exc()
        logger.debug("%s terminating", self)

    def getConnection(self):
        """Get a connection to the given URL.

        Blocks until either a connection is established, or we are asked to
        shut-down. Includes a simple strategy for slowing down the retry rate,
        retrying from 5 seconds to 20 seconds until the connection appears or
        we waited a full minute.
        """
        wait_time = 1
        while 1:
            try:
                conn = httplib.HTTPConnection(
                    self.host, timeout=self.producer.timeout)
                conn.connect()
                return conn
            except socket.error as e:
                wait_time = min(wait_time * 2, 21)
                if wait_time > 20:
                    # we waited a full minute, we assume a permanent failure
                    logger.warning("Error %s - reconnect failed.", e)
                    self.stopping = True
                    break
                wait_time += 1
                logger.warning("Error %s connecting to - will "
                               "retry in %d second(s)", e, wait_time)
                for i in xrange(wait_time):
                    time.sleep(0.1)
        return None # must be stopping!
