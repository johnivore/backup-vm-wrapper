# backup-vm-wrapper

This is a quick-and-dirty wrapper for [backup-vm](https://github.com/milkey-mouse/backup-vm.git).

It will:

* back up all [qemu](https://www.qemu.org/) VMs via [borg](https://www.borgbackup.org/)
* create borg repos (one per domain) as needed
* prune backups


## Requirements

* Python 3
* [qemu](https://www.qemu.org/)
* [borg](https://www.borgbackup.org/)
* [backup-vm](https://github.com/milkey-mouse/backup-vm.git)


## Installation / usage

1. create a config file (see `sample_config.conf`) somewhere like `/usr/local/etc/backup-vm-wrapper.conf`
2. copy `backup-vm-wrapper.py` somewhere
3. run it:

        backup-vm-wrapper.py

    or, if your config is not `/usr/local/etc/backup-vm-wrapper.conf`:

        backup-vm-wrapper.py -c /path/to/config
