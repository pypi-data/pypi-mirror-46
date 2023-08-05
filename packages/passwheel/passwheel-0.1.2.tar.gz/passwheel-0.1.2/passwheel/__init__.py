'''
passwheel

A password and secret personal storage tool.
'''

__title__ = 'passwheel'
__version__ = '0.1.2'
__all__ = ('Wheel',)
__author__ = 'Johan Nestaas <johannestaas@gmail.com>'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2019 Johan Nestaas'

import sys

from .wheel import Wheel
from .passgen import gen_password
from .clipboard import copy
from .util import info, warning, error


def main():
    import argparse
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='cmd')

    p = subs.add_parser('add', help='add a login')
    p.add_argument('service', help='service/website')
    p.add_argument('username', help='login')
    p.add_argument(
        '--custom', '-c', action='store_true',
        help='input custom password',
    )
    p.add_argument(
        '--words', '-w', type=int, default=2,
        help='number of words in generated password',
    )
    p.add_argument(
        '--digits', '-d', type=int, default=3,
        help='number of digits in generated password',
    )
    p.add_argument(
        '--symbol', '-s', action='store_true',
        help='append a random symbol to the password',
    )

    p = subs.add_parser('rm', help='remove a service or login')
    p.add_argument('service', help='service/website')
    p.add_argument('username', nargs='?', default=None, help='login')

    p = subs.add_parser('get', help='fetch creds for service/website')
    p.add_argument('service', help='service/website')
    p.add_argument('username', nargs='?', default=None, help='login name')
    p.add_argument(
        '--copy', '-c', action='store_true',
        help='copy to clipboard',
    )

    p = subs.add_parser('dump', help='dump all decrypted credentials')
    p.add_argument('service', nargs='?', default=None, help='service/website')
    p.add_argument(
        '--no-passwords', '-n', action='store_true',
        help='dont print passwords',
    )

    p = subs.add_parser('changepw', help='change master password')

    args = parser.parse_args()

    wheel = Wheel()
    if args.cmd == 'dump':
        pw = wheel.get_pass(prompt='unlock: ')
        data = wheel.decrypt_wheel(pw)
        if args.service:
            data = {
                k: v
                for k, v in data.items()
                if k.lower() == args.service.lower()
            }
        if not data:
            warning('no passwords found.')
        else:
            for service, logins in data.items():
                print(service)
                for user, pw in logins.items():
                    if args.no_passwords:
                        print('  {}'.format(user))
                    else:
                        print('  {}: {}'.format(user, pw))
    elif args.cmd == 'add':
        if args.custom:
            add_pw = wheel.get_pass(prompt='new password: ', verify=True)
        else:
            add_pw, entropy = gen_password(
                num_words=args.words,
                num_digits=args.digits,
                add_symbol=args.symbol,
            )
            info('generated password with {} bits of entropy'.format(
                int(entropy),
            ))
            if copy(add_pw):
                info('password copied to clipboard')
            else:
                warning("couldn't copy to clipboard, please run `get` command")
        wheel.add_login(args.service, args.username, add_pw)
    elif args.cmd == 'rm':
        wheel.rm_login(args.service, args.username)
    elif args.cmd == 'get':
        logins = sorted(wheel.get_login(args.service).items())
        if args.username:
            logins = [
                (user, pw)
                for user, pw in logins
                if user == args.username
            ]
        if not logins:
            warning('{!r}::{!r} not found'.format(
                args.service,
                args.username or '*',
            ))
            sys.exit(1)
        if args.copy:
            if len(logins) > 1:
                users = sorted([x[0] for x in logins])
                warning(
                    '{} logins found, please specify user from: {}'
                    .format(len(logins), ', '.join(users))
                )
                sys.exit(2)
            user, pw = logins[0]
            if copy(pw):
                info('copied password to clipboard for user:')
                print(user)
            else:
                error('couldnt copy password to clipboard. Please remove -c.')
                sys.exit(3)
        else:
            if args.username:
                # Just print the first and only password.
                print(logins[0][1])
            else:
                # Dump the users and passwords for this service.
                for key, val in logins:
                    print('{}|{}'.format(key, val))
    elif args.cmd == 'changepw':
        wheel.change_password()
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
