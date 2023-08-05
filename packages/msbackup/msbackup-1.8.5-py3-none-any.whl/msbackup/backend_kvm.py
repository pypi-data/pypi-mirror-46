# -*- coding: utf-8 -*-
"""Модуль архиватора виртуальных машин Qemu/KVM."""

import os
import uuid
import shlex
import signal
import libvirt
import logging
import subprocess
import tempfile
import shutil
import tarfile
import xml.etree.ElementTree as ET

from msbackup.backend_base import Base as BaseBackend


logger = logging.getLogger('msbackup')


def preexec_fn():  # pragma: no coverage
    """ОТправка сигнала подпроцессу."""
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)


def get_backend_kwargs(params):
    """Подготовка параметров для режима 'kvm'."""
    kwargs = BaseBackend.get_common_backend_kwargs(params)
    return kwargs


class Kvm(BaseBackend):
    """
    Архиватор виртуальных машин Qemu/KVM.

    Зависимости:
    - установлены пакеты "KVM":http://www.linux-kvm.org/page/Main_Page и
      "libvirt":http://libvirt.org/index.html;
    - "QEMU Guest agent":http://wiki.libvirt.org/page/Qemu_guest_agent
      установлен на каждой виртуальной машине;
    - образы дисков виртуальных машин в формате
      "qcow2":https://en.wikipedia.org/wiki/Qcow;
    - установлен "pigz":http://zlib.net/pigz;
    - установлен Python-3 пакет "libvirt":https://libvirt.org/python.html.
    """

    SECTION = 'Backend-KVM'
    LIBVIRT_CONNECTION = 'qemu:///system'

    @classmethod
    def make_subparser(cls, subparsers):
        """Добавление раздела параметров командной строки для архиватора."""
        parser = subparsers.add_parser('kvm')
        parser.set_defaults(get_backend_kwargs=get_backend_kwargs)
        parser.add_argument(
            'source', nargs='*', metavar='DOMAIN',
            help='Domain name of virtual machine.')

    def __init__(self, config, *args, **kwargs):
        """Конструктор."""
        super().__init__(config, *args, **kwargs)
        self.conn = libvirt.open(self.LIBVIRT_CONNECTION)

    def _backup(self, sources=None, **kwargs):
        """
        Архивация виртуальных машин Qemu/KVM.

        :param sources: Список имён виртуальных машин.
        :type sources: [str]
        :return: Количество ошибок.
        :rtype: int
        """
        if sources is None:
            raise Exception('sources is not specified')
        error_count = 0
        for source in sources:
            output = self.outpath(source)
            logger.info('Backup domain: %s', source)
            try:
                self.archive(
                    source=source,
                    output=output,
                )
            except libvirt.libvirtError as ex:
                error_count += 1
                logger.error('libvirtError: %s', str(ex))
            except subprocess.CalledProcessError as ex:
                logger.error(str(ex))
                error_count += 1
        return error_count

    def _archive(self, source, output, **kwargs):
        """
        Упаковка состояния виртуальной машины в архив.

        :param source: Имя домена виртуальной машины.
        :type source: str
        :param output: Путь к файлу с архивом.
        :type output: str
        """
        snapshot = Snapshot(conn=self.conn, domain_name=source)
        if not snapshot.is_active():
            raise Exception('Domain "%s" is not active.' % source)
        if snapshot.has_current_snapshot():
            raise Exception('Domain "%s" has already a snapshot.' % source)
        ext, tar_mode = '.tar', 'w'
        tar_name = source + ext
        tmpdir = tempfile.mkdtemp(dir=self.tmp_dir)
        cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            tar_path = os.path.join(tmpdir, tar_name)
            tar = tarfile.open(tar_path, mode=tar_mode)
            xml_files = snapshot.dumpXML(path=tmpdir)
            for xml_file in xml_files:
                xml_file_name = os.path.basename(xml_file)
                tar.add(xml_file_name)
                logger.debug('file %s added' % xml_file_name)
                os.remove(xml_file)
            snapshot.create_snapshot()
            logger.debug(
                'Adding image files for "%s" to archive "%s"',
                source,
                tar_path,
            )
            for disk, src in snapshot.disks.items():
                file_name = os.path.basename(src)
                dest = os.path.join(tmpdir, file_name)
                logger.debug('copying "%s" to "%s"', src, dest)
                shutil.copy2(src, dest)
                logger.debug(
                    'Adding "%s" to archive "%s"', file_name, tar_path)
                tar.add(file_name)
                logger.debug('removing "%s" from "%s"', file_name, tmpdir)
                os.remove(file_name)
            snapshot.do_blockcommit()
            tar.close()
            logger.debug('Compressing "%s"', tar_name)
            cmd_list = self.compressor_cmd.copy()
            cmd_list.extend(['--stdout', tar_path])
            with open(output, mode='wb') as file_out:
                subprocess.check_call(
                    cmd_list,
                    stdout=file_out,
                    stderr=self.stream_err,
                    preexec_fn=preexec_fn,
                )
        except Exception:
            raise
        finally:
            os.chdir(cwd)
            shutil.rmtree(tmpdir, ignore_errors=True)


class Snapshot():
    """Снимок виртуальной машины."""

    def __init__(self, conn, domain_name):
        """Конструктор."""
        self.domain_name = domain_name
        self.snapshot_xml = None
        self.disks = None
        self.snapshot_disk = None
        self.snapshotId = None
        self.conn = conn
        self.snapshot = None

    def get_domain(self):
        """Получение виртуальной машины по имени домена."""
        return self.conn.lookupByName(self.domain_name)

    def is_active(self):
        """Проверка активности виртуальной машины."""
        return self.get_domain().isActive() != 0

    def get_disks(self):
        """Получение всех дисков виртуальной машины."""
        domain = self.get_domain()
        root = ET.fromstring(domain.XMLDesc())
        devices = root.findall('./devices/disk[@device=\'disk\']')
        sources = [device.find('source').attrib for device in devices]
        targets = [device.find('target').attrib for device in devices]
        if len(sources) != len(targets):  # pragma: no coverage
            raise Exception("Targets and sources lengths are different %s:%s" %
                            (len(sources), len(targets)))
        devs = {}
        for i in range(len(sources)):
            devs[targets[i]['dev']] = sources[i]['file']
        return devs

    def dumpXML(self, path):
        """Сохранение настроек виртуальной машины."""
        domain = self.get_domain()
        logger.debug('Dumping XMLs for domain %s', domain.name())
        xml_files = []
        dest_file = os.path.join(path, '%s.xml' % domain.name())
        if os.path.exists(dest_file):  # pragma: no coverage
            raise Exception('File %s already exists!' % dest_file)
        with open(dest_file, mode='w') as dest_fh:
            # dump different xmls files. First of all, the offline dump
            xml = domain.XMLDesc()
            dest_fh.write(xml)
        xml_files += [dest_file]
        logger.debug('File %s wrote', dest_file)
        # All flags:
        # - libvirt.VIR_DOMAIN_XML_INACTIVE
        # - libvirt.VIR_DOMAIN_XML_MIGRATABLE
        # - libvirt.VIR_DOMAIN_XML_SECURE
        # - libvirt.VIR_DOMAIN_XML_UPDATE_CPU
        dest_file = '%s-inactive.xml' % domain.name()
        dest_file = os.path.join(path, dest_file)
        if os.path.exists(dest_file):  # pragma: no coverage
            raise Exception('File %s already exists!' % dest_file)
        with open(dest_file, mode='w') as dest_fh:
            # dump different xmls files. First of all, the offline dump.
            xml = domain.XMLDesc(flags=libvirt.VIR_DOMAIN_XML_INACTIVE)
            dest_fh.write(xml)
        xml_files += [dest_file]
        logger.debug('File %s wrote', dest_file)
        # Dump a migrate config file
        dest_file = '%s-migratable.xml' % domain.name()
        dest_file = os.path.join(path, dest_file)
        if os.path.exists(dest_file):  # pragma: no coverage
            raise Exception('File %s already exists!' % dest_file)
        with open(dest_file, mode='w') as dest_fh:
            # dump different xmls files. First of all, the offline dump.
            xml = domain.XMLDesc(
                flags=(libvirt.VIR_DOMAIN_XML_INACTIVE +
                       libvirt.VIR_DOMAIN_XML_MIGRATABLE))
            dest_fh.write(xml)
        xml_files += [dest_file]
        logger.debug('File %s wrote', dest_file)
        return xml_files

    def has_current_snapshot(self):
        """Проверка наличия снимка виртуальной машины."""
        return self.get_domain().hasCurrentSnapshot() != 0

    def getXML(self):
        """Получение состояния дисков виртуальной машины в формате XML."""
        domain = self.get_domain()
        self.disks = self.get_disks()
        self.snapshotId = str(uuid.uuid1()).split("-")[0]
        diskspecs = []
        fmt = ('--diskspec %s,'
               'file=/var/lib/libvirt/images/snapshot_%s_%s-%s.img')
        for disk in self.disks:
            diskspecs += [
                fmt % (disk, self.domain_name, disk, self.snapshotId)]
        my_cmd = (
            'virsh snapshot-create-as --domain {domain_name} '
            '{snapshotId} {diskspecs} --disk-only --atomic --quiesce '
            '--print-xml'.format(
                domain_name=domain.name(),
                snapshotId=self.snapshotId,
                diskspecs=' '.join(diskspecs),
            )
        )
        logger.debug("Executing: %s", my_cmd)
        create_xml = subprocess.Popen(
            shlex.split(my_cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=preexec_fn,
            shell=False,
        )
        self.snapshot_xml = create_xml.stdout.read().decode('utf-8')
        status = create_xml.wait()
        if status != 0:  # pragma: no coverage
            logger.error('Error for %s:%s', my_cmd, create_xml.stderr.read())
            logger.critical('%s returned %s state', 'virsh', status)
            raise Exception('snapshot-create-as didn\'t work properly')
        return self.snapshot_xml

    def create_snapshot(self):
        """Создание снимка состояния виртуальной машины."""
        if self.snapshot is not None:
            logger.error('A snapshot is already defined for this domain')
            logger.warning('Returning the current snapshot')
            return self.snapshot
        if self.snapshot_xml is None:
            self.getXML()
        domain = self.get_domain()
        logger.debug(
            'Creating snapshot %s for %s', self.snapshotId, self.domain_name)
        self.snapshot = domain.snapshotCreateXML(
            self.snapshot_xml,
            flags=sum([
                libvirt.VIR_DOMAIN_SNAPSHOT_CREATE_DISK_ONLY,
                libvirt.VIR_DOMAIN_SNAPSHOT_CREATE_ATOMIC,
                libvirt.VIR_DOMAIN_SNAPSHOT_CREATE_QUIESCE,
            ]),
        )
        self.snapshot_disk = self.get_disks()
        for disk, top in self.snapshot_disk.items():
            logger.debug(
                'Created top image {top} for {domain_name} {disk}',
                top=top,
                domain_name=domain.name(),
                disk=disk,
            )
        return self.snapshot

    def do_blockcommit(self):
        """Выполнение команды blockcommit для каждого диска в снимке."""
        if self.snapshot is None:
            raise Exception('no snapshot of domain')
        domain = self.get_domain()
        logger.debug("Blockcommitting %s", domain.name())
        for disk in self.disks:
            my_cmd = (
                'virsh blockcommit {domain_name} {disk} --active '
                '--pivot').format(domain_name=domain.name(), disk=disk)
            logger.debug('Executing: %s', my_cmd)
            blockcommit = subprocess.Popen(
                shlex.split(my_cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=preexec_fn,
                shell=False,
            )
            for line in blockcommit.stdout:
                line = line.strip()
                if len(line) == 0:
                    continue
                logger.debug(line)
            status = blockcommit.wait()
            if status != 0:
                logger.error(
                    'Error for %s => %s', my_cmd, blockcommit.stderr.read())
                logger.critical('%s returned %s state', 'virsh', status)
                raise Exception('blockcommit didn\'t work properly')
        test_disks = self.get_disks()
        for disk, base in self.disks.items():
            test_base = test_disks[disk]
            top = self.snapshot_disk[disk]
            if base == test_base and top != test_base:
                logger.debug('Removing %s', top)
                os.remove(top)
            else:  # pragma: no coverage
                logger.error('original base: %s, top: %s, new_base: %s',
                             base, top, test_base)
                raise Exception(
                    'Something goes wrong for snaphost %s', self.snapshotId)
        logger.debug('Removing snapshot %s', self.snapshotId)
        metadata = [libvirt.VIR_DOMAIN_SNAPSHOT_DELETE_METADATA_ONLY]
        self.snapshot.delete(flags=sum(metadata))
