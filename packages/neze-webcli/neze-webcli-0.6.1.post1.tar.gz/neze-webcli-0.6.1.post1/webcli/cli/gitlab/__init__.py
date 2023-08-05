from .. import CLI
from ..patches.config import *
from ...data.config import Config,Spec
from ...utils.choices import ChoicesList
from ...api.gitlab import GitLabAPI as gAPI, deploy_key_fields, ssh_key_fields, KeyData as pubKeyData
from argparse import FileType as _FileType

__all__=['cli','main']

csp = Spec('gitlab')
csp.add_section('DEFAULT')
csp.add_key('@secrets',str)
csp.add_key('url',str)
csp.add_key('token',str)
cfg = Config(csp)

# BEGIN CLI
cli = CLI()
"usage: gitlab [-h|options] command [...]"

cli.add_argument('-n',dest='name',default='DEFAULT',
        help="Name of the configuration section for your server.")

cli.bind_config(cfg)

cli._api_by_section = {}
def _get_api(self,section):
    if section in self._api_by_section:
        return self._api_by_section[section]
    url = self.get_config(section,'url')
    api = gAPI(url)
    api.token = self.get_config(section,'token','password')
    self._api_by_section[section] = api
    return api
cli.get_api = _get_api.__get__(cli)

# BEGIN CLI ME
@cli.subparser('me',help='About you')
def my_account(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/user']()
    cli.out(rsp)
# END CLI ME

fpr_field = 'fingerprint'
cli_ssh_key_fields = ssh_key_fields + [fpr_field]
def process_fpr(rsp):
    if isinstance(rsp,list):
        for x in rsp:
            process_fpr(x)
    if isinstance(rsp,dict):
        try:
            key = pubKeyData(rsp['key'],raw=True)
            rsp[fpr_field] = key.hash
        except Exception:
            pass

# BEGIN CLI SSH
@cli.subparser('ssh',help='List SSH keys')
def my_keys(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/user/keys'].get()
    if fpr_field in argv.fields:
        process_fpr(rsp)
    cli.out(rsp,fields=list(argv.fields))
my_keys.add_argument('--fields',type=ChoicesList,choices=ChoicesList(cli_ssh_key_fields),default=cli_ssh_key_fields)
@cli.subparser('ssh:show',help='Show SSH key')
def show_key(cli,argv):
    api = cli.get_api(argv.name)['/user/keys']
    fields = list(argv.fields)
    for key_id in argv.key_id:
        rsp=[api.get(id=key_id)]
        if fpr_field in fields:
            process_fpr(rsp)
        cli.out(rsp,fields=fields)
show_key.add_argument('key_id',type=int,nargs='+')
@cli.subparser('ssh:rm',help='Remove SSH key')
def rm_key(cli,argv):
    api = cli.get_api(argv.name)['/user/keys']
    for key_id in argv.key_id:
        rsp=[api.delete(id=key_id)]
        rsp[0]['id'] = key_id
        cli.out(rsp)
rm_key.add_argument('key_id',type=int,nargs='+')
@cli.subparser('ssh:add',help='Add SSH key')
def add_key(cli,argv):
    api = cli.get_api(argv.name)
    key = argv.key
    key.title = argv.title
    key = dict(key)
    rsp = api['/user/keys'].post(**key)
    cli.out(rsp)
add_key.add_argument('--title',type=str,default=None)
add_key.add_argument('key',type=pubKeyData)
# END CLI SSH

# BEGIN CLI GPG
@cli.subparser('gpg',help='List GPG keys')
def my_keys(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/user/gpg_keys'].get()
    cli.out(rsp)
@cli.subparser('gpg:show',help='Show GPG key')
def show_key(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/user/gpg_keys'].get(id=argv.key_id)
    cli.out(rsp)
show_key.add_argument('key_id',type=int)
@cli.subparser('gpg:rm',help='Remove GPG key')
def rm_key(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/user/gpg_keys'].delete(id=argv.key_id)
    cli.out(rsp)
rm_key.add_argument('key_id',type=int)
@cli.subparser('gpg:add',help='Add GPG key')
def add_key(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/user/gpg_keys'].post(key='\r\n'.join(map(lambda x: x.strip(),argv.key.readlines())))
    cli.out(rsp)
add_key.add_argument('key',type=_FileType(mode='r'))
# END CLI GPG

# BEGIN CLI EMAIL
@cli.subparser('emails',help='List e-mail addresses.')
def my_emails(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/user/emails'].get()
    cli.out(rsp)
@cli.subparser('emails:show',help='Show specific e-mail.')
def show_email(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/user/emails'].get(id=argv.key_id)
    cli.out(rsp)
show_email.add_argument('key_id',type=int)
@cli.subparser('emails:rm',help='Remove e-mail address.')
def rm_email(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/user/emails'].delete(id=argv.key_id)
    cli.out(rsp)
rm_email.add_argument('key_id',type=int)
@cli.subparser('emails:add',help='Add e-mail address.')
def add_email(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/user/emails'].post(email=argv.email)
    cli.out(rsp)
add_email.add_argument('email')
# END CLI EMAIL

# BEGIN CLI PROJECTS
@cli.subparser('projects',help='List my projects.')
def my_projects(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/projects'].get(owned=True)
    rsp = [ {'id': x['id'],'name': x['path_with_namespace']} for x in rsp ]
    cli.out(rsp,fields=['id','name'])
@cli.subparser('projects:show',help='Show specific project.')
def show_project(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/projects'].get(id=argv.project_id)
    cli.out(rsp)
show_project.add_argument('project_id',type=int)
@cli.subparser('projects:new',help='New project.')
def new_project(cli,argv):
    api = cli.get_api(argv.name)
    kwargs = {}
    if argv.group is not None:
        kwargs['namespace_id'] = argv.group
    rsp = api['/projects'].post(name=argv.project_name,visibility=argv.visibility,**kwargs)
    cli.out(rsp)
new_project.set_defaults(visibility='private')
group = new_project.add_mutually_exclusive_group(required=False)
for v in ['private','internal','public']:
    group.add_argument('--{}'.format(v),dest='visibility',const=v,action='store_const')
new_project.add_argument('--group',type=int,default=None)
new_project.add_argument('project_name')
@cli.subparser('projects:rm',help='Remove project.')
def rm_project(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/projects'].delete(id=argv.project_id)
    cli.out(rsp)
rm_project.add_argument('project_id',type=int)
# END CLI PROJECTS

# BEGIN CLI NAMESPACES
@cli.subparser('namespaces',help='List your namespaces.')
def my_namespaces(cli,argv):
    api = cli.get_api(argv.name)['/namespaces']
    rsp = api.get()
    rsp = [ {'id': x['id'],'name': x['full_path']} for x in rsp ]
    cli.out(rsp)
# END CLI NAMESPACES

cli_deploy_key_fields = deploy_key_fields + [fpr_field]
# BEGIN CLI DEPLOY KEYS
@cli.subparser('deploy_keys',help='List deploy keys of project')
def list_deploy_keys(cli,argv):
    api = cli.get_api(argv.name)
    rsp = api['/deploy_keys'].get(project=argv.project)
    if fpr_field in argv.fields:
        process_fpr(rsp)
    cli.out(rsp,fields=list(argv.fields))
list_deploy_keys.add_argument('--fields',type=ChoicesList,choices=ChoicesList(cli_deploy_key_fields),default=cli_deploy_key_fields)
# list_deploy_keys.add_argument('--project',type=int,required=True)
list_deploy_keys.add_argument('project',type=int)
@cli.subparser('deploy_keys:show',help='Show deploy key from project')
def show_deploy_key(cli,argv):
    api = cli.get_api(argv.name)['/deploy_keys']
    fields = list(argv.fields)
    for key_id in argv.key_id:
        rsp = [api.get(project=argv.project,id=key_id)]
        if fpr_field in fields:
            process_fpr(rsp)
        cli.out(rsp,fields=fields)
show_deploy_key.add_argument('key_id',type=int,nargs='+')
@cli.subparser('deploy_keys:rm',help='Remove deploy key for project')
def rm_deploy_key(cli,argv):
    api = cli.get_api(argv.name)['/deploy_keys']
    for key_id in argv.key_id:
        rsp = [api.delete(project=argv.project,id=key_id)]
        rsp[0]['id'] = key_id
        cli.out(rsp)
rm_deploy_key.add_argument('key_id',type=int,nargs='+')
@cli.subparser('deploy_keys:add',help='Add deploy key to project')
def add_deploy_key(cli,argv):
    api = cli.get_api(argv.name)['/deploy_keys']
    key = argv.key
    key.title = argv.title
    key = dict(key)
    rsp = api.post(project=argv.project,can_push=argv.push,**key)
    cli.out(rsp)
add_deploy_key.add_argument('--title',type=str,default=None)
add_deploy_key.add_argument('--push',action='store_true',default=False)
add_deploy_key.add_argument('key',type=pubKeyData)
@cli.subparser('deploy_keys:set',help='Update deploy keys of project')
def set_deploy_key(cli,argv):
    api = cli.get_api(argv.name)['/deploy_keys']
    rsp = api.put(id=argv.key_id,project=argv.project,can_push=argv.push,title=argv.title)
    cli.out(rsp)
set_deploy_key.add_argument('--title',type=str,default=None)
group = set_deploy_key.add_mutually_exclusive_group(required=False)
group.add_argument('--push',dest='push',action='store_true',default=None)
group.add_argument('--no-push',dest='push',action='store_false',default=None)
set_deploy_key.add_argument('key_id',type=int)
# END CLI DEPLOY KEYS

main = cli.run
"Runs the Gitlab CLI"
