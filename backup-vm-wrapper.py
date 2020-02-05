#!/usr/bin/env python3

"""
backup-vm-wrapper.py

Copyright 2020  John Begenisich

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
from pathlib import Path
import argparse
import configparser
import subprocess


# -------------------------------------------------

def run_or_not(command, dry_run):
    if dry_run:
        print('Would run: ' + ' '.join(command))
        return
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stdout.decode().strip())
        print(result.stderr.decode().strip())
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Backup all VMs')
    parser.add_argument('--dry-run', '-n',
                        action='store_true',
                        default=False,
                        help='Dry run')
    parser.add_argument('--config', '-c',
                        default='/usr/local/etc/backup-vm-wrapper.conf',
                        help='Config file')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config_file = Path(args.config)
    if not config_file.is_file():
        print(f'** Config file ({config_file}) not found')
        sys.exit(1)
    config.read(config_file)

    borg_path = Path(config['main']['borg_path'])
    if not borg_path.is_dir():
        print(f'** Borg path ({borg_path}) not found')
        sys.exit(1)

    command = ['virsh', 'list', '--all', '--name']
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(result.stdout.decode().strip())
        print(result.stderr.decode().strip())
        sys.exit(1)
    domain_list = result.stdout.decode().strip().split('\n')

    for domain in domain_list:
        # create borg repo if needed
        domain_repo = borg_path / domain
        if not domain_repo.is_dir():
            command = ['borg', 'init', '-e', 'none', str(domain_repo)]
            run_or_not(command, args.dry_run)
        # back up
        borg_destination = str(domain_repo) + '::' + domain + '-{now:%Y-%m-%d}'
        if config.has_section('disks') and config.has_option('disks', domain):
            disks = config['disks'][domain].strip()
            command = ['backup-vm', domain, disks, borg_destination]
        else:
            command = ['backup-vm', domain, borg_destination]
        run_or_not(command, args.dry_run)
        # prune
        command = ['borg', 'prune', '--keep-daily', '7', '--keep-weekly', '8', str(domain_repo)]
        run_or_not(command, args.dry_run)


if __name__ == '__main__':
    main()
