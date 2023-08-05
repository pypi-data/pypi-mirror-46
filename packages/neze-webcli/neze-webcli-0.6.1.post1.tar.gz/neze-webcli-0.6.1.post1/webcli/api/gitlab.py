# SPECIFICATION: https://docs.gitlab.com/ee/api/
from . import APIFunction,API
from dateutil.parser import parse as _dateparse
from argparse import FileType as _FileType, ArgumentTypeError as _TypeError
import re as _re
from hashlib import md5 as _hash
from base64 import b64decode as _b64decode, b64encode as _b64encode
from subprocess import run as _run,\
        PIPE as _PIPE
# from datetime import datetime as _datetime

__all__=['GitLabAPI']

def _format_response(r,expected=[200]):
    if r.status_code not in expected:
        r.data = '{:d} {}'.format(r.status_code,r.reason)
    try:
        r.data = r.json()
    except Exception:
        r.data = {}

class GitLabFunction(APIFunction):
    def __init__(self,fields=[]):
        super().__init__()

        self.add_output('id',int)
        self.add_argument('id',int)
        for f in fields or []:
            if f == 'id':
                continue
            self.add_output(f)
            self.add_argument(f)
        self.add_output('message',str)
        self.set_output_accept(fields is None)
        self.set_argument_accept(fields is None)
    __call__=APIFunction.get

    def _prepare_all(self,request):
        request.url += self.path
    def _prepare_get(self,request):
        self._prepare_all(request)
        if 'id' in request.kwargs:
            request.url += '/{:d}'.format(int(request.kwargs['id']))
            del request.kwargs['id']
        request.request['params'] = request.kwargs
    def _process(self,response):
        pass

ssh_key_write_fields = ['id','title','key']
ssh_key_fields = ssh_key_write_fields + ['created_at']

class GitLabList(GitLabFunction):
    def _prepare_delete(self,request):
        self._prepare_all(request)
        request.url += '/{:d}'.format(int(request.kwargs['id']))
        del request.kwargs['id']
    def _prepare_post(self,request):
        self._prepare_all(request)
        request.request['data'] = request.kwargs

deploy_key_write_fields = ['id','title','key','can_push']
deploy_key_fields = deploy_key_write_fields + ['created_at']

class GitLabProjectList(GitLabList):
    def _prepare_all(self,request):
        if 'project' in request.kwargs:
            pid=request.kwargs.pop('project')
            if pid is not None:
                request.url += '/projects/{:d}'.format(int(pid))
        super()._prepare_all(request)
    def _prepare_put(self,request):
        self._prepare_all(request)
        request.url += '/{:d}'.format(int(request.kwargs.pop('id')))
        request.request['data'] = request.kwargs

def _strORnull(s):
    if s:
        return str(s)
    return None

def _timestamp(ts):
    try:
        return _dateparse(ts).astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
    except:
        return ts

def _datestamp(ds):
    try:
        return _dateparse(ds).strftime('%d %h %Y')
    except:
        return ds

class GitLabMe(GitLabFunction):
    def __init__(self):
        super().__init__(fields=None)
        for social in ['linkedin','skype','twitter']:
            self.add_output(social,_strORnull)
        for timestamp in ['confirmed_at','created_at','current_sign_in_at',\
                'last_sign_in_at']:
            self.add_output(timestamp,_timestamp)
        self.add_output('last_activity_on',_datestamp)

class GitLabGPG(GitLabList):
    pass

class GitLabAPI(API):
    def __init__(self,url,token=None):
        super().__init__(url)
        self['/user'] = GitLabMe()
        self['/user/keys'] = GitLabList(fields=ssh_key_fields)
        self['/user/gpg_keys'] = GitLabGPG(fields=['key'])
        self['/user/emails'] = GitLabList(fields=['email'])
        self['/projects'] = GitLabList(fields=None)
        self['/deploy_keys'] = GitLabProjectList(fields=deploy_key_fields+['project'])
        self['/namespaces'] = GitLabFunction(fields=None)

    def _prepare(self,request):
        headers = {}
        headers['private-token'] = self.token
        request.request['headers'] = headers
        request.url = self.url

    def _process_get(self,response):
        _format_response(response,[200])
    _process_put = _process_get

    def _process_delete(self,response):
        _format_response(response,[202,204])

    def _process_post(self,response):
        _format_response(response,[201,400])

_pubkey_re = _re.compile(r'^(?P<algo>[a-zA-Z0-9-]+)\s(?P<data>[a-zA-Z0-9/+]+=*)(?:\s(?P<comment>.*))?$')
_keygen_re = _re.compile(r'^(?P<size>[0-9]+)\s(?P<hash>MD5(?::[a-f0-9]{2}){16})\s(?P<comment>.*)\s\((?P<algo>[A-Z0-9]+)\)$')

def errfunc(self):
    raise AttributeError(self)

class KeyData:
    def __init__(self,argument,title=None,raw=False):
        if not isinstance(argument,str):
            raise TypeError(type(argument))
        self.title = title
        self._read(argument,nofile=raw)
        self._parse()
        self._check()

    @property
    def title(self):
        r = self.__title
        if r is None or (len(r)==0):
            r = self.__comment
        if r is None or (len(r)==0):
            raise AttributeError('title')
        return r
    @title.setter
    def title(self,title):
        if title is None:
            pass
        elif not isinstance(title,str):
            raise TypeError(type(title))
        self.__title = title

    def _read(self,argument,nofile=False):
        raw = argument
        if not nofile:
            try:
                with _FileType(mode='r')(argument) as f:
                    raw = f.read()
            except _TypeError:
                pass
        self.__raw = raw.split('\n',1)[0]
        self._read = errfunc.__get__('_read')

    @property
    def raw(self):
        return self.__raw

    def _parse(self):
        m = _pubkey_re.match(self.raw)
        if not m:
            raise _TypeError('Input is not following the syntax of a public key.')
        self.__header = m.group('algo')
        if (len(m.group('data')) % 4):
            raise _TypeError('Invalid padding of base 64 public key data.')
        ko=0
        try:
            self.__data = _b64decode(m.group('data'))
        except Exception:
            ko=1
        if ko:
            raise _TypeError('Base 64 public key data cannot be decoded.')
        self.__hash = _hash(self.__data).hexdigest()
        self.__comment = m.group('comment')
        self._parse = errfunc.__get__('_parse')

    @property
    def header(self):
        return self.__header
    @property
    def data(self):
        return _b64encode(self.__data).decode('utf-8')
    @property
    def comment(self):
        return self.__comment
    @property
    def hash(self):
        return self.__hash

    def _check(self):
        keygen = _run(['which','ssh-keygen'],stdout=_PIPE)
        if keygen.returncode:
            self.__size = None
            self.__algo = None
        else:
            keygen = keygen.stdout.decode('utf-8').split('\n',1)[0]
            keygen = _run([keygen,'-E','md5','-l','-f','-'],
                    input=(self.raw+'\n').encode('utf-8'),stdout=_PIPE,stderr=_PIPE)
            if keygen.returncode:
                raise _TypeError('ssh-keygen raised an error while parsing: %s' % (keygen.stderr.decode('utf-8')))
            keygen = keygen.stdout.decode('utf-8').split('\n',1)[0]
            m = _keygen_re.match(keygen)
            if not m:
                raise _TypeError('ssh-keygen output was not correctly parsed: %s' % keygen)
            self.__size = int(m.group('size'))
            h = ''.join(m.group('hash').split(':')[1:])
            if h != self.__hash:
                raise _TypeError('ssh-keygen hash (%s) does not match the data hash (%s)' % (h,self.__hash))
            c = m.group('comment')
            if self.__comment is None and c == 'no comment':
                pass
            elif self.__comment != c:
                raise _TypeError('ssh-keygen comment (%s) does not match the original (%s)' % (c,self.__comment))
            self.__algo = m.group('algo')
        self._check = errfunc.__get__('_check')

    @property
    def size(self):
        return self.__size
    @property
    def algo(self):
        return self.__algo

    @property
    def key(self):
        k = [self.header,self.data]
        c = self.comment
        if c is not None:
            k.append(c)
        return ' '.join(k)

    #FIXME: will be deleted
    def keys(self):
        return ['title','key']

    def __getitem__(self,key):
        if key in self.keys():
            return getattr(self,key)
        raise KeyError(key)
