import sys
from ._logging import logger
logger = logger.getChild('askpass')
from .pinentry import Pinentry
__all__=['AskPass']

class AskPass(object):
    """
    Helper for using Pinentry and asking for a password
    """
    defaults = dict(title='Password',
        tries=2,
        prompt='Type in your password',
        error='Bad password. %(tries)d tries left.',
        ok='Ok',cancel='Cancel',
        retry=True,
        try_again='Do you want to try again?',
        fail='Too many failures.',
        yes='Try again',no='Give up',
        timeout=10)

    def __init__(self, **kw):
        args = dict(self.defaults)
        args.update(kw)
        for attr in self.defaults.keys():
            setattr(self,attr,args[attr])

    def __enter__(self):
        self.pinentry = Pinentry().__enter__()
        return self

    def __exit__(self,t,v,tb):
        self.pinentry.__exit__(t,v,tb)

    def __iter__(self):
        if hasattr(self,'tries_left'): return
        self.tries_left = self.tries
        return self

    def __next__(self):
        pwd = None
        if self.tries_left <= 0: self.ask_retry()
        if self.tries_left > 0:  pwd = self.ask_pass()
        if pwd is None:          raise StopIteration()
        return pwd

    def ask_retry(self):
        if self.retry:
            retry = self.pinentry.setprompt(self.title)\
                                 .setdesc(self.try_again)\
                                 .seterror(self.fail)\
                                 .setok(self.yes)\
                                 .setcancel(self.no)\
                                 .settimeout(self.timeout)\
                                 .confirm()
            if retry:
                self.pinentry.reset()
                self.tries_left = self.tries

    def ask_pass(self):
        pwd = self.pinentry.setprompt(self.title)\
                           .setdesc(self.prompt)\
                           .setok(self.ok)\
                           .setcancel(self.cancel)\
                           .settimeout(self.timeout)\
                           .getpin()
        self.tries_left -= 1
        self.pinentry.seterror(self.error % { 'tries': self.tries_left })
        return pwd

def main(): # pragma: no cover
    with AskPass() as ap:
        for p in ap:
            if p == 'password': break
        else:
            print('didnt get password')
            sys.exit(2)
    sys.exit(0)
