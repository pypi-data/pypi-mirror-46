from base64 import b64encode as _b64
from urllib.parse import urlparse as _urlparse
import re as _re

fields = ['activityDate','addedDate','bandwidthPriority','comment','corruptEver','creator','dateCreated','desiredAvailable','doneDate','downloadDir','downloadedEver','downloadLimit','downloadLimited','error','errorString','eta','etaIdle','files','fileStats','hashString','haveUnchecked','haveValid','honorsSessionLimits','id','isFinished','isPrivate','isStalled','leftUntilDone','magnetLink','manualAnnounceTime','maxConnectedPeers','metadataPercentComplete','name','peer-limit','peers','peersConnected','peersFrom','peersGettingFromUs','peersSendingToUs','percentDone','pieces','pieceCount','pieceSize','priorities','queuePosition','rateDownload','rateUpload','recheckProgress','secondsDownloading','secondsSeeding','seedIdleLimit','seedIdleMode','seedRatioLimit','seedRatioMode','sizeWhenDone','startDate','status','trackers','trackerStats','totalSize','torrentFile','uploadedEver','uploadLimit','uploadLimited','uploadRatio','wanted','webseeds','webseedsSendingToUs']

class Status(object):
    _status_values = ['paused','checkwait','check','downloadwait','download','seedwait','seed']
    @classmethod
    def statuses(cls):
        statuses = cls._status_values + ['finished','stalled']
        return statuses + [ 'not-'+s for s in statuses ]

    def __init__(self,status=None):
        if status is None:
            def _check(self,torrent):
                return True
            self._check = _check.__get__(self)
            def _keys(self,*args,**kwargs):
                return []
            self.keys = _keys.__get__(self)
            return
        if status.startswith('not-'):
            status = status[4:]
            self._negate = True
        else:
            self._negate = False
        if status == 'finished':
            def _check(self,torrent):
                i = torrent.get('isFinished',None)
                if i is not None:
                    return bool(i)
                return None
            self._check = _check.__get__(self)
            def _keys(self):
                return ['isFinished']
            self._keys = _keys.__get__(self)
        elif status == 'stalled':
            def _check(self,torrent):
                i = torrent.get('isStalled',None)
                if i is not None:
                    return bool(i)
                return None
            self._check = _check.__get__(self)
            def _keys(self):
                return ['isStalled']
            self._keys = _keys.__get__(self)
        elif status in self._status_values:
            sindex = self._status_values.index(status)
            def _check(self,torrent):
                i = torrent.get('status',None)
                if i is not None:
                    return bool(i==sindex)
                return None
            self._check = _check.__get__(self)
            def _keys(self):
                return ['status']
            self._keys = _keys.__get__(self)
        else:
            raise ValueError(status)

    @classmethod
    def format_torrent(cls,torrent):
        if 'status' not in torrent:
            return
        if torrent.get('isFinished',None):
            s='finished'
        elif torrent.get('isStalled',None):
            s='stalled'
        else:
            s=cls._status_values[int(torrent['status'])]
        torrent['status'] = s

    def check(self,*args,**kwargs):
        if hasattr(self,'_check'):
            if self._negate:
                return not self._check(*args,**kwargs)
            else:
                return self._check(*args,**kwargs)
        return None
    def keys(self,keys=[]):
        if hasattr(self,'_keys_cache'):
            kc = self._keys_cache
            delattr(self,'_keys_cache')
            return kc
        if hasattr(self,'_keys'):
            kc = self._keys()
        else:
            kc = []
        kc = list(set(kc)-set(keys))
        self._keys_cache = kc
        return kc

class Data(dict):
    def __init__(self,raw):
        super().__init__()
        self._parse(raw)

    def _parse(self,raw):
        key = 'filename'
        value = raw
        if not raw.startswith('magnet:'):
            up = _urlparse(raw)
            if not (up.netloc and up.scheme):
                key = 'metainfo'
                value = _b64(open(raw,'rb').read()).decode('utf-8')
        self[key] = value

    def __setitem__(self,key,value):
        if len(self) > 0:
            raise IndexError("Maximum size reached")
        if key not in ['metainfo','filename']:
            raise KeyError("Forbidden key")
        if not isinstance(value,str):
            raise ValueError("Value should be a string.")
        super().__setitem__(key,value)

_int_re = r'[0-9]+'
_sha_re = r'[0-9a-fA-F]{40}'
_int_sha_re = r'(?:(?:'+_int_re+r')|(?:'+_sha_re+r'))'
class Ids(object):
    _recently = 'recently-active'
    _intre = _re.compile(r'^'+_int_re+r'$')
    _share = _re.compile(r'^'+_sha_re+r'$')
    _rangere = _re.compile(r'^(?P<lower>'+_int_re+r')?(?:\.\.(?P<step>'+_int_re+r'))?(?:\.\.(?P<upper>'+_int_re+r'))$')
    _listre = _re.compile(r'^'+_int_sha_re+r'(?:,'+_int_sha_re+r')*$')
    def __init__(self,recently=True):
        self._allow_recently = bool(recently)

    def __call__(self,i):
        if isinstance(i,int):
            return i
        if isinstance(i,str):
            if self._allow_recently and i == self._recently:
                return i
            if self._share.match(i):
                return i
            if self._intre.match(i):
                return int(i)
            if self._listre.match(i):
                return self(i.split(','))
            m=self._rangere.match(i)
            if m:
                l = m.group('lower')
                l = 0 if l is None else int(l)
                s = m.group('step')
                s = 1 if s is None else int(s)
                u = int(m.group('upper'))
                return list(range(l,u,s))
        elif hasattr(i,'__iter__'):
            return list(map(self,i))
        raise TypeError()

    def __contains__(self,key):
        try:
            val = self(key)
        except TypeError:
            return False
        return True

    def __len__(self):
        return 1
    def __str__(self):
        res=['INT','SHA1']
        if self._allow_recently:
            res.append('"recently-active"')
        return ' or '.join(filter(lambda x: x, (', '.join(res[:-1]),''.join(res[-1:]))))
    def __repr__(self):
        return 'Torrent ID'

    def accumulate(self,it,res=None):
        if res is None:
            res = []
        for x in it:
            y = self(x)
            if y == self._recently:
                return y
            if (not isinstance(y,str)) and hasattr(y,'__iter__'):
                self.accumulate(y,res)
            elif y not in res:
                res.append(y)
        return res

