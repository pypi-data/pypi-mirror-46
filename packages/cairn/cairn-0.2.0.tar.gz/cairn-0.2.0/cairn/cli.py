import argparse
import subprocess
import sys

from cairn.versions import next_version, validate_mode, VersionMatchError


def _mode(text):
    validate_mode(text)
    return text


def _name(text):
    if ' ' in text:
        raise RuntimeError('Name must not have spaces in it')
    return text


def current_version():
    cmd = [
        'git', 'describe', '--always'
    ]
    output = subprocess.check_output(cmd).decode().strip()
    return output


def create_tag(name, dry_run):
    # create the git tag
    if not dry_run:
        cmd = [
            'git',
            'tag',
            '-a', name,
            '-m', name,
        ]
        subprocess.check_call(cmd)

    else:
        print('Next Version:', name)


def parse_commandline():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # common args
    parser.add_argument('-n', '--dry-run', action='store_true',
                        help='Do not perform tagging simply print new tag')

    # update parser
    parser_update = subparsers.add_parser('update', aliases=('up',))
    parser_update.add_argument('mode', type=_mode, default='patch', nargs='?', help='The type of version increment')
    parser_update.set_defaults(handler=run_update)

    # create parser
    parser_create = subparsers.add_parser('create', aliases=('new',))
    parser_create.add_argument('name', type=_name, default='v0.0.1', nargs='?', help='The name of the new tag')
    parser_create.set_defaults(handler=run_create)

    return parser, parser.parse_args()


def run_update(args):

    # extract the current version of the project
    curr_ver = current_version()

    # generate the next version of the project
    next_ver = next_version(curr_ver, args.mode)

    if next_ver is None:
        print('Unable to generate a new ')

    create_tag(next_ver, args.dry_run)

    return True


def run_create(args):
    create_tag(args.name, args.dry_run)

    return True


def main():
    parser, args = parse_commandline()

    if not hasattr(args, 'handler'):
        parser.print_usage()
        sys.exit(1)

    success = False
    try:
        success = args.handler(args)
    except VersionMatchError as ex:
        print('Current version: {} can not be matched. Sorry!'.format(ex.version))

    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
