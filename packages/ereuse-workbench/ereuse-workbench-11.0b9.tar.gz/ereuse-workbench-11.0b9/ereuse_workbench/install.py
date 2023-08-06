"""
This module provides functionality to install an OS in the system being tested.

Important: GPT partition scheme and UEFI-based boot not yet supported. All relevant
code is just placeholder.
"""
import logging
import pathlib
import textwrap
from pathlib import Path

from ereuse_utils import cmd

from ereuse_workbench.utils import Measurable, Severity


class Install(Measurable):
    def __init__(self,
                 path_to_os_image: Path,
                 target_disk: str = '/dev/sda',
                 swap_space: bool = True):
        """
        Initializes variables to sensible defaults
        :param target_disk: Target disk's device name (e.g. /dev/sda).
                            It must exist.
        :param swap_space: Whether to provision a swap partition.
        :param path_to_os_image: A filesystem path to the OS .fsa. It must
                                 be somewhere in the client's filesystem
                                 hiearchy.
        """
        super().__init__()
        self._target_disk = target_disk
        self._swap_space = swap_space
        self._path = path_to_os_image
        self.type = self.__class__.__name__
        self.severity = Severity.Info
        self.name = path_to_os_image.name
        if '32' in self.name or 'x86' in self.name:
            self.address = 32
        elif '64' in self.name:
            self.address = 64
        else:
            self.address = None

    def run(self, callback):
        logging.info('Install %s to %s', self._path, self._target_disk)
        with self.measure():
            try:
                self._run(callback)
            except Exception as e:
                self.severity = Severity.Error
                logging.error('Failed install on %s:', self._target_disk)
                logging.exception(e)
                raise CannotInstall(e) from e

    def _run(self, callback):
        """
        Partitions block device(s) and installs an OS.

        :return: A dictonary with the summary of the operation.
        """
        assert isinstance(self._path, Path)
        # Steps:
        # Zero out disk label
        #   TODO (low prio): ensure disk not mounted (findmnt?)
        # Partition according to BIOS or GPT scheme
        #   TODO: SERIOUSLY consider replacing parted with (s)gdisk
        #   BIOS
        #   ----
        #     Swap: [1MB buffer, 1st part OS from 1M to -4G,
        #       2nd part swap from -4G to 100%]
        #     No swap: [1MB buffer, 1st part OS from 1M to 100%]
        #   UEFI
        #     Swap: [1st part ESP 0% to 100M, 2nd part OS from 100M to -4G,
        #      3rd part swap from -4G to 100%]
        #     No swap: [1st part ESP 0% to 100M, 2nd part OS from 100M to -4G]
        # Install OS to OS partition
        #   fsarchiver vs tar/rsync? Much to my surprise, fsarchiver looks more suited
        #   https://forums.fsarchiver.org/viewtopic.php?t=922
        # Install bootloader
        #   BIOS: GRUB to MBR + VBR
        #   UEFI: GRUB to ESP

        # Zero out disk label
        self.zero_out(self._target_disk)

        # Partition main disk (must set os_partition appropriately in every possible case)
        os_partition = self.partition(self._target_disk, self._swap_space)

        # Install OS
        self.install(self._path, os_partition, callback)

        # Install bootloader
        self.install_bootloader(self._target_disk)

        # sync at the end to prepare for abrupt poweroff
        self.sync()

        # TODO rewrite fstab to use swap space correctly. sth like:
        # OLD_SWAP_UUID=$(grep swap $tmproot/etc/fstab | get_uuid)
        # sed -i "s/$OLD_SWAP_UUID/$NEW_SWAP_UUID/g" $tmproot/etc/fstab

    @classmethod
    def zero_out(cls, drive: str):
        cmd.run('dd', 'if=/dev/zero', 'of={}'.format(drive), 'bs=512', 'count=1')
        cls.sync()

    @staticmethod
    def partition(target_disk: str, swap_space: bool):
        """
        :return: A string representing the partition that has been allocated
                 to the OS
        """
        if swap_space:
            parted_commands = textwrap.dedent("""\
                mklabel msdos \
                mkpart primary ext2 1MiB -1GiB \
                mkpart primary linux-swap -1GiB 100% \
                """)
            os_partition = '{}{}'.format(target_disk, 1)  # "/dev/sda1"
        else:
            parted_commands = textwrap.dedent("""\
                mklabel msdos \
                mkpart primary ext2 1MiB 100% \
            """)
            os_partition = '{}{}'.format(target_disk, 1)  # "/dev/sda1"
        cmd.run('parted', '--script', target_disk, '--', parted_commands)
        return os_partition

    @staticmethod
    def install(path_to_os_image: Path, target_partition: str, callback):
        """
        Installs an OS image to a target partition.
        :param path_to_os_image:
        :param target_partition:
        :return:
        """
        assert path_to_os_image.suffix == '.fsa', 'Set the .fsa extension'
        i = cmd.ProgressiveCmd('fsarchiver',
                               'restfs',
                               '-v',
                               path_to_os_image,
                               'id=0,dest={}'.format(target_partition),
                               number_chars={1, 2, 3},
                               callback=callback)
        i.run()

    @staticmethod
    def install_bootloader(target_disk: str):
        """
        Installs the grub2 bootloader to the target disk.
        :param target_disk:
        :param part_type:
        :return:
        """
        # Must install grub via 'grub-install', but it will complain if --boot-directory is not used.
        pathlib.Path('/tmp/mnt').mkdir(exist_ok=True)  # Exist_ok in case of double wb execution
        cmd.run('mount', '{}1'.format(target_disk), '/tmp/mnt')
        cmd.run('grub-install', '--boot-directory=/tmp/mnt/boot/', target_disk)
        cmd.run('umount', '/tmp/mnt')

    @staticmethod
    def sync():
        cmd.run('sync')


class CannotInstall(Exception):
    def __init__(self, e: Exception) -> None:
        super().__init__()
        self.e = e

    def __str__(self) -> str:
        return ('OS installation failed: {e}'.format(e=self.e))
