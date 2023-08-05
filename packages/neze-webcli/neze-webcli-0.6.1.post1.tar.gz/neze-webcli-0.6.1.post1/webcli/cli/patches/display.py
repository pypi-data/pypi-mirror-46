from argparse import ArgumentParser
from sys import stdout,stderr
from json import dump as jdump
from webcli.utils.dataparsers import ydump
from collections import OrderedDict as odict

__all__ = ['DisplayEngine']

def obj_cleaner(obj,**kwargs):
    fields = kwargs.get('fields',None)
    res = obj
    if isinstance(obj,str) or (obj is None):
        pass
    elif hasattr(obj,'keys'):
        keys=list(obj.keys())
        if len(keys) < 2:
            for k in keys:
                res[k] = obj_cleaner(obj[k],**kwargs)
        elif fields is not None:
            res = odict()
            keys = fields
        for k in filter(obj.__contains__,keys):
            res[k] = obj_cleaner(obj[k],**kwargs)
    elif hasattr(obj,'__iter__'):
        res = []
        for x in obj:
            res.append(obj_cleaner(x,**kwargs))
    return res

def obj_formatter(dumper,**dkwargs):
    nl = dkwargs.pop('newline',True)
    def formatter(stream,*args,**kwargs):
        try:
            encoding = stream.encoding or 'utf-8'
        except:
            encoding = 'utf-8'
        for i in range(len(args)):
            arg = args[i]
            if isinstance(arg,str):
                stream.write(arg.format(*args[i+1:],**kwargs))
                stream.write('\n')
                break
            elif isinstance(arg,bytes):
                stream.write(arg.encode(encoding))
            else:
                try:
                    dumper(obj_cleaner(arg,**kwargs),stream,**dkwargs)
                except TypeError:
                    stream.write(str(arg))
            if nl:
                stream.write('\n')
        stream.flush()
    return formatter

def itisinstance(o,cls):
    return all(map(lambda x: isinstance(x,cls), o))

def read_fields(l):
    res = list()
    for x in l:
        try:
            for k in x.keys():
                if k not in res:
                    res.append(k)
        except AttributeError:
            raise TypeError()
    if not itisinstance(res,str):
        raise TypeError()
    return res

def mdump(obj,stream,**kwargs):
    delimiter=kwargs.get('delimiter',':')
    headers=kwargs.get('headers',True)
    if isinstance(obj,list):
        fields = None
        try:
            fields = read_fields(obj)
        except TypeError:
            pass
        if fields is not None:
            if headers:
                stream.write(delimiter.join(fields)+'\n\n')
            for o in obj:
                l = []
                for f in fields:
                    l.append(str(o.get(f,'')))
                stream.write(delimiter.join(l)+'\n')
        else:
            stream.write('\n'.join(map(str,obj))+'\n')
    elif hasattr(obj,'keys'):
        l = len(obj.keys()) - 1
        for k in obj.keys():
            if l:
                stream.write(delimiter.join(['',str(k),'\n']))
            mdump(obj[k],stream,**kwargs)
            if l:
                stream.write(delimiter.join(['','!'+str(k),'\n']))
    else:
        stream.write(str(obj)+'\n')

json_formatter = obj_formatter(jdump,sort_keys=True,indent=2)
yaml_formatter = obj_formatter(ydump,default_flow_style=False,indent=2,newline=False)
mchn_formatter = obj_formatter(mdump,headers=False,newline=False)

class DisplayEngine(object):
    __encoding = 'utf-8'
    formatters = odict([
        ('yaml',yaml_formatter),
        ('json',json_formatter),
        ('machine',mchn_formatter),
    ])
    def __init__(self,display,stdout=stdout,stderr=stderr):
        self.__display = display
        self.__formatter = self.formatters[display]
        self.__stdout = stdout
        self.__stderr = stderr
    @property
    def stdout(self):
        return self.__stdout
    @property
    def stderr(self):
        return self.__stderr
    def out(self,*args,**kwargs):
        self.__formatter(self.__stdout,*args,**kwargs)
    def err(self,*args,**kwargs):
        self.__formatter(self.__stderr,*args,**kwargs)

def _add_display_arguments(self,dest='display',default=next(iter(DisplayEngine.formatters)),display=None):
    choices = list(DisplayEngine.formatters)
    # choices = ['human','json','yaml','machine','compact']
    if display is None:
        if default not in choices:
            raise ValueError("Invalid default '{}' not among {}".format(default,choices))
        group = self.add_argument_group(title='Display',description='Output display parameters.')
        group = group.add_mutually_exclusive_group()
        group.add_argument('--{}'.format(dest),dest=dest,choices=choices)
        for choice in choices:
            group.add_argument('--{}'.format(choice),dest=dest,action='store_const',const=choice)
        self.set_defaults(**{dest: default})
        return group
    if display not in choices:
        raise ValueError("Invalid display '{}' not among {}".format(display,choices))
    self.set_defaults(**{dest: display})
    return self
ArgumentParser.add_display_arguments = _add_display_arguments
