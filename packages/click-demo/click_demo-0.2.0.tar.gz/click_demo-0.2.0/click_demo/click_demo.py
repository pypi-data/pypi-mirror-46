import codecs
import json
import os
import sys

import click


@click.group()
def psp():
    pass


@psp.command()
@click.option('--name', '-n', default='there', prompt='Please enter Name', help='Name of the person to greet',
              show_default=True)
def hi(name):
    click.echo('Hi {}!'.format(name))  # used instead of print since print syntax differ by version, just a
    # safer side they say


@psp.command()
@click.option('--name', '-n', default='there', prompt='Please enter Name', help='Name of the person to greet',
              show_default=True)
def bye(name):
    click.echo('Bye {}!'.format(name))


@psp.command()
@click.option('--name', nargs=2, type=str)
def makejson(name):
    event_payload = {
        "fname": name[0],
        "lname": name[1]
    }
    print(json.dumps(event_payload, indent=4, sort_keys=False))


@psp.command()
@click.option('--upper', 'transformation', flag_value='upper',
              default=True)
@click.option('--lower', 'transformation', flag_value='lower')
def info(transformation):
    click.echo(getattr(sys.platform, transformation)())


@psp.command()
@click.option('--hash-type', type=click.Choice(['md5', 'sha1']), prompt='Enter type')
def digest(hash_type):
    click.echo('You selected : ' + hash_type)


@psp.command()
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True)
def encrypt(password):
    click.echo('Encrypting password to {}'.format(codecs.encode(password, 'rot13')))


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()


@psp.command()
@click.option('--username', prompt=True,
              default=lambda: os.environ.get('USER', ''), show_default=os.environ.get('USER', ''))
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def hello(username):
    print("Hello", username)


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@psp.command()
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
@click.option('--username', prompt="Enter Username")
def dropdb(username):
    click.echo('DB dropped by user {}!'.format(username))


@psp.command()
@click.option('--username', envvar='USERNAME')
@click.option('--dob')
def greet(username, dob):
    click.echo('Hey %s' % username + '!')
    click.echo('Your DOB is %s' % dob)
    # click.echo('{}'.format(username) + ' has DOB {}'.format(dob))


@psp.command()
@click.option('paths', '--path', envvar='PATH', multiple=True,
              type=click.Path())
def perform(paths):
    for path in paths:
        click.echo(path)


if __name__ == '__main__':
    perform()

# psp.add_command(hi)
# psp.add_command(bye)


if __name__ == '__main__':
    psp(auto_envvar_prefix='PSP')
