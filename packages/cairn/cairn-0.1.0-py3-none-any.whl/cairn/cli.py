import argparse
import subprocess
import sys

from cairn.versions import next_version, validate_mode, VersionMatchError


def _mode(text):
    validate_mode(text)
    return text


def current_version():
    cmd = [
        'git', 'describe', '--always'
    ]
    output = subprocess.check_output(cmd).decode().strip()
    return output


def parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=_mode, default='patch', nargs='?', help='The type of version increment')
    parser.add_argument('-n', '--dry-run', action='store_true', help='Do not perform tagging simply print new tag')
    return parser.parse_args()


def run(args):
    # extract the current version of the project
    curr_ver = current_version()

    # generate the next version of the project
    next_ver = next_version(curr_ver, args.mode)

    if next_ver is None:
        print('Unable to generate a new ')

    # create the git tag
    if not args.dry_run:
        cmd = [
            'git',
            'tag',
            '-a', next_ver,
            '-m', next_ver,
        ]
        subprocess.check_call(cmd)

    else:
        print('Next Version:', next_ver)

    return True


def main():
    args = parse_commandline()

    success = False

    try:
        success = run(args)
    except VersionMatchError as ex:
        print('Current version: {} can not be matched. Sorry!'.format(ex.version))

    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
