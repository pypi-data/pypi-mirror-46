import subprocess,io,os,pathlib2
from ._logging import logger
logger = logger.getChild('pinentry')
__all__=['Pinentry']

if 'PINENTRY' in os.environ: # pragma: no cover
    PINENTRY = os.getenv('PINENTRY')
else:
    PINENTRIES = dict()
    for p in filter(lambda x: x.is_dir(), map(pathlib2.Path,os.getenv('PATH').split(':'))):
        for f in p.iterdir():
            if f.is_file() and os.access(str(f),os.X_OK):
                name = f.name
                if name.startswith('pinentry-') or name == 'pinentry':
                    PINENTRIES.setdefault(name,str(f))
    PINENTRY = PINENTRIES.get('pinentry')
    PINENTRY = PINENTRIES.get('pinentry-curses',PINENTRY)
    if 'DISPLAY' in os.environ:
        PINENTRY = PINENTRIES.get('pinentry-gnome3',PINENTRY)

class PinentryError(Exception):
    pass

class PinentryWarning(PinentryError):
    pass

class Pinentry(object):
    """
    Wrappers for the pinentry program
    """
    program = PINENTRY
    def __init__(self,Werror=False):
        self.Werror = Werror
        pass

    def __enter__(self):
        if hasattr(self,'proc'): return
        self.proc = subprocess.Popen(str(self.program),
                                     stdin  = subprocess.PIPE,
                                     stdout = subprocess.PIPE)
        self.logger = logger.getChild(str(self.proc.pid))

        if self.Werror:
            def warning(self,msg,*a,**k):
                msg = msg % (k if len(k) else a)
                self.logger.warning(msg)
                raise PinentryWarning(msg)
            self.warning = warning.__get__(self)

        def error(self,msg,*a,**k):
            msg = msg % (k if len(k) else a)
            self.logger.error(msg)
            raise PinentryError(msg)
        self.error = error.__get__(self)

        for x in ['debug','info','warning','error']:
            if not hasattr(self,x):
                setattr(self,x,getattr(self.logger,x))

        self.stdin  = io.TextIOWrapper(self.proc.stdin,  encoding = 'utf-8')
        self.stdout = io.TextIOWrapper(self.proc.stdout, encoding = 'utf-8')

        self._read('OK')
        return self

    def __exit__(self,t,v,tb):
        self.close()

    def close(self):
        self._ok_command('BYE')
        self.proc.communicate()

    def _write(self,s,*a,**kw):
        if len(a) and len(kw):
            raise ValueError('Cannot simultaneously take named arguments and '
                    'positional arguments for format string.')
        msg = s % (kw if len(kw) else a)
        self.debug('>:%s',msg)
        self.stdin.write(msg)
        self.stdin.write('\n')
        self.stdin.flush()

    def _readline(self):
        ret = self.stdout.readline().strip()
        self.debug('<:%s',ret)
        return ret

    def _read(self,expected=None):
        status = '#'
        while status == '#':
            ret = self._readline().split(' ',1)
            status = ret.pop(0)
        if expected is not None and status != expected:
            self.warning('Unexpected status %s', status)
        return status,ret[0] if len(ret) else ''

    def _ok_command(self,*a,**kw):
        self._write(*a,**kw)
        s,m = self._read()
        if s == 'OK':  return self
        if s == 'ERR': self.error(m)
        self.error('Unexpected status %s',s) # pragma: no cover

    def _yesno_command(self,*a,**kw):
        self._write(*a,**kw)
        s,m = self._read()
        if s == 'OK':  return True
        if s == 'ERR': return False
        self.error('Unexpected status %s',s) # pragma: no cover

    def _command(self,*a,**kw):
        self._write(*a,**kw)
        s,ret = 'S',None
        while s not in ['OK','ERR']:
            s,m = self._read()
            if s == 'D': ret = m
        if s == 'OK':  return ret

    def reset(self):
        return self._ok_command('RESET')

    def nop(self):
        return self._ok_command('NOP')

    def help(self):
        return self._ok_command('HELP')

    def setdesc(self,desc,*a,**kw):
        return self._ok_command('SETDESC %s' % desc, *a, **kw)

    def setprompt(self,prompt,*a,**kw):
        return self._ok_command('SETPROMPT %s' % prompt, *a, **kw)

    def setrepeat(self):
        return self._ok_command('SETREPEAT')

    def setrepeaterror(self,err,*a,**kw):
        return self._ok_command('SETREPEATERROR %s' % err, *a, **kw)

    def seterror(self,err,*a,**kw):
        return self._ok_command('SETERROR %s' % err, *a, **kw)

    def setok(self,ok,*a,**kw):
        return self._ok_command('SETOK %s' % ok, *a, **kw)

    def setcancel(self,ko,*a,**kw):
        return self._ok_command('SETCANCEL %s' % ko, *a, **kw)

    def getpin(self):
        return self._command('GETPIN')

    def confirm(self):
        return self._yesno_command('CONFIRM')

    def message(self):
        return self._yesno_command('MESSAGE')

    def settimeout(self,to):
        return self._ok_command('SETTIMEOUT %d', to)
