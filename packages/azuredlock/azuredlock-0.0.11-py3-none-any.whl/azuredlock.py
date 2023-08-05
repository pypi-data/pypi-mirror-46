import click
import json
import logging
import requests
import subprocess
import time

SP_DEFAULT_NAME = "http://redlock"
RL_DEFAULT_URL = "https://api.redlock.io/"
_RETRY_TIMES = 12


@click.group()
@click.option('-l', '--log-level', envvar="AR_LOG_LEVEL", default="INFO")
def cli(log_level):
    """azuredlock performs basic tasks to help integrate and manage azure + redlock = azuredlock. It is built to be
    run from the Azure Cloud Shell which already has the necessary dependencies installed: Azure CLI and Azure
    Managed Identity. But, it can be run elsewhere if the azure cli is present. The script assumes the user is either
    logged in to the azure cli and has the necessary privileges to create Azure AD Applications, Service Principles,
    Roles, Resource Groups and can assign these privileges too. The Azure CLI can be launched from the Azure Portal. """
    level = log_level.upper()
    if level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        raise Exception('Bad log level')

    logging.getLogger().setLevel(level)
    logging.debug("DEBUG logging set")


@cli.command()
@click.option('-sp-name', '--service-principle-name', default=SP_DEFAULT_NAME, envvar="AR_SP_NAME",
              prompt="Service Principal Name",
              help='Azure AD Service Principle Name. Azure AD will turn it into a valid URL.')
@click.option('-rl-url', '--redlock_url',
              type=click.Choice(['https://api.redlock.io/', 'https://api2.redlock.io/', 'https://api.eu.redlock.io/']),
              envvar="AR_RL_URL", prompt='Redlock URL', help="Redlock Application URL")
@click.option('-g', '--redlock_group', envvar="AR_RL_GROUP", prompt='Redlock account group name',
              help="Redlock Account Group Name", default="Default Account Group")
@click.option('-u', '--redlock_user', envvar="AR_RL_USER", prompt='Redlock username',
              help="Redlock Username with Admin Privileges")
@click.option('-p', '--redlock_password', envvar="AR_RL_PWD", prompt='Redlock password', hide_input=True,
              confirmation_prompt=True, help="Redlock Password")
@click.option('-d', '--accept-defaults', envvar="AR_ACCEPT_DEFAULTS", is_flag=True,
              help="Automatically accept defaults", default=False)
def onboard(service_principle_name, redlock_url, redlock_group, redlock_user, redlock_password, accept_defaults):
    """creates the required Azure AD objects to integrate an Azure Subscription with Redlock. Then it posts them to
    Redlock. It will ask for required info or it reads environment variables:

    \b
    AR_SP_NAME=<Azure Service Principal Name>
    AR_RL_URL=<Redlock App URL>
    AR_RL_USER=<Redlock Username>
    AR_RL_PWD=<Redlock Password>

    """
    builder = {
        'params': {'service_principle_name': service_principle_name, 'redlock_url': redlock_url,
                   'redlock_group': redlock_group, 'redlock_user': redlock_user,
                   'redlock_password': redlock_password},
        'rl'    : {'headers': {
            'Content-Type': 'application/json',
            'Accept'      : 'application/json'
        }}
    }
    get_account(builder)
    if check_account_exists(builder) and not accept_defaults:
        click.confirm('Cloud Account ID {} already exists. Continue?'.format(builder['account']['id']),
                      default=True, abort=True)
    create_sp_reader(builder)
    get_sp(builder, service_principle_name)
    get_account_group_id(builder)
    if not check_account_exists(builder):
        create_redlock_account(builder)
    else:
        update_redlock_account(builder)


@cli.command()
def cycle_service_principle():
    pass


@cli.command()
@click.option('-rl-url', '--redlock_url',
              type=click.Choice(['https://api.redlock.io/', 'https://api2.redlock.io/', 'https://api.eu.redlock.io/']),
              envvar="AR_RL_URL", prompt='Redlock URL', help="Redlock Application URL")
@click.option('-u', '--redlock_user', envvar="AR_RL_USER", prompt='Redlock username',
              help="Redlock Username with Admin Privileges")
@click.option('-p', '--redlock_password', envvar="AR_RL_PWD", prompt='Redlock password', hide_input=True,
              confirmation_prompt=True, help="Redlock Password")
def show_account_group_names(redlock_url, redlock_user, redlock_password):
    """
    lists the Redlock Account Group Names that are currently setup
    """
    builder = {
        'params': {'redlock_url': redlock_url,
                   'redlock_user': redlock_user,
                   'redlock_password': redlock_password},
        'rl'    : {'headers': {
            'Content-Type': 'application/json',
            'Accept'      : 'application/json'
        }}
    }
    names = get_account_group_names(builder)
    click.echo()
    click.echo("Account Group Names")
    click.echo("===================")
    for name in names:
        click.echo(name)


# TODO add -raw to continue as below
# TODO normal should be a subset of relevant info
@cli.command()
@click.option('-sp-name', '--service-principle-name', default=SP_DEFAULT_NAME, envvar="AR_SP_NAME",
              prompt="Service Principal Name", help="Azure AD Service Principle Name")
def show_info(service_principle_name):
    """show info about the account, tenant, subscription, etc..."""
    builder = {}
    get_account(builder)
    get_sp(builder, service_principle_name)
    click.echo(json.dumps(builder, indent=2))


@cli.command()
def create_role():
    pass


def get_account(builder):
    completion = subprocess.run(["az account show"], shell=True, stdout=subprocess.PIPE)
    if completion.stdout:
        account = json.loads(completion.stdout.decode("utf-8"))
        builder["account"] = account
        logging.debug(builder)


def get_sp(builder, sp_name=SP_DEFAULT_NAME):
    if not sp_name.startswith("http"):
        fixed_up_sp_name = "http://" + sp_name
    else:
        fixed_up_sp_name = sp_name
    cmd = "az ad sp show --id {}".format(fixed_up_sp_name)
    for l in range(0, _RETRY_TIMES):
        try:
            completion = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE)
            if completion.stdout:
                sp = json.loads(completion.stdout.decode("utf-8"))
                builder["sp"] = sp
        except Exception as ex:
            if l < _RETRY_TIMES and ("doesn't exist" in str(ex)):
                time.sleep(5)
                logging.warning("Retrying get service principle since just created: %s/%s", l + 1, _RETRY_TIMES)
            else:
                logging.warning("Cannot Find Service Principal")
                raise


# TODO catch errors
# TODO catch no az errors on all of these
def create_sp_reader(builder):
    cmd = "az ad sp create-for-rbac -n {} --role reader".format(builder['params']['service_principle_name'])
    completion = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE)
    if completion.stdout:
        builder["sp_rbac"] = json.loads(completion.stdout.decode("utf-8"))


def create_redlock_account(builder):
    get_token(builder)
    params = builder['params']
    # TODO dry the json
    r = requests.post(params['redlock_url'] + 'cloud/azure', headers=builder['rl']['headers'], json={
        "cloudAccount"      : {
            "accountId": builder['account']['id'],
            "enabled"  : "true",
            "groupIds" : [builder['rl']['group_id']],
            "name"     : builder['account']['name']
        },
        "clientId"          : builder['sp_rbac']['appId'],
        "key"               : builder['sp_rbac']['password'],
        "monitorFlowLogs"   : "true",
        "tenantId"          : builder['sp_rbac']['tenant'],
        "servicePrincipalId": builder['sp']['objectId']
    })
    if r.status_code != requests.codes.ok:
        click.echo('Error posting to RedLock service [%d] - %s' % (r.status_code, r.text))
    click.echo(r.status_code)


def update_redlock_account(builder):
    get_token(builder)
    params = builder['params']
    r = requests.put(params['redlock_url'] + 'cloud/azure/{}'.format(builder['account']['id']),
                     headers=builder['rl']['headers'], json={
        "cloudAccount"      : {
            "accountId": builder['account']['id'],
            "enabled"  : "true",
            "groupIds" : [builder['rl']['group_id']],
            "name"     : builder['account']['name']
        },
        "clientId"          : builder['sp_rbac']['appId'],
        "key"               : builder['sp_rbac']['password'],
        "monitorFlowLogs"   : "true",
        "tenantId"          : builder['sp_rbac']['tenant'],
        "servicePrincipalId": builder['sp']['objectId']
    })
    if r.status_code != requests.codes.ok:
        click.echo('Error putting to RedLock service [%d] - %s' % (r.status_code, r.text))
    click.echo(r.status_code)


def get_token(builder):
    """
    Retrieve the token using the credentials if not already seen
    """
    if not builder['rl'].get('token', False):

        params = builder['params']
        r = requests.post(params['redlock_url'] + 'login', headers=builder['rl']['headers'], json={
            'customerName': '',
            'username'    : params['redlock_user'],
            'password'    : params['redlock_password']
        })

        if r.status_code != requests.codes.ok:
            click.echo('Error authenticating to RedLock service [%d] - %s' % (r.status_code, r.text))

        token = r.json()['token']

        logging.debug("rl_token: %s", token)
        builder['rl']['token'] = token
        builder['rl']['headers']['x-redlock-auth'] = token


def check_account_exists(builder):
    """
    Gets default account info (subscription id) and checks with Redlock to see if that account already has been added
    """
    # No key so go check
    if not builder['rl'].get('exists', False):
        get_account(builder)
        get_token(builder)
        params = builder['params']
        r = requests.get(params['redlock_url'] + 'cloud/azure/{}'.format(builder['account']['id']),
                         headers=builder['rl']['headers'])
        if r.status_code != requests.codes.ok:
            builder['rl']['exists'] = False
            return False
        else:
            builder['rl']['exists'] = True
            return True
    # Have already checked before and here is the same answer
    else:
        return builder['rl']['exists']


def get_account_group_names(builder):
    groups = get_account_groups(builder)
    names = []
    for group in groups:
        names.append(group['name'])
    return names


def get_account_group_id(builder):
    groups = get_account_groups(builder)
    for group in groups:
        if group['name'] == builder['params']['redlock_group']:
            builder['rl']['group_id'] = group['id']
        else:
            # TODO what here? Is Default Account Group a well known and reliable name?
            pass


def get_account_groups(builder):
    get_token(builder)

    r = requests.get(builder['params']['redlock_url'] + 'cloud/group/name', headers=builder['rl']['headers'])
    if r.status_code != requests.codes.ok:
        raise Exception("Cannot contact Redlock for Account Groups List")
    else:
        return r.json()
