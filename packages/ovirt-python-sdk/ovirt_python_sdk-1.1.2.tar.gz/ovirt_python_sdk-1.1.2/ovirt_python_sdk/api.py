import ovirtsdk4 as sdk
from ovirtsdk4 import types

from ovirt_python_sdk.exceptions import TooManyItemsException, NotEnoughMemoryException


class Ovirt:
    def __init__(
        self,
        url,
        username,
        password,
        ca_file,
    ):
        self._connection = sdk.Connection(
            url=url,
            username=username,
            password=password,
            ca_file=ca_file,
        )

    def __del__(self):
        self._connection.close()

    def get_host_by_name(self, name: str) -> types.Host:
        """
        Получение одного хоста по имени

        :param name: Имя хоста
        """
        result = self.get_hosts_by_name(name)

        if len(result) > 1:
            raise TooManyItemsException(len(result))

        return result[0] if result else None

    def get_hosts_by_name(self, name: str) -> list:
        """
        Поиск хостов по имени

        :param name: Имя хоста
        :return: Список найденных хостов
        """
        return self._connection.system_service().hosts_service().list(search=f'name={name}')

    def get_disk_by_name(self, name: str) -> types.Disk:
        """
        Получение одного диска по имени

        :param name: Имя диска
        """
        result = self.get_disks_by_name(name)

        if len(result) > 1:
            raise TooManyItemsException(len(result))

        return result[0] if result else None

    def get_disks_by_name(self, name: str) -> list:
        """
        Поиск дисков по имени

        :param name: Имя диска
        :return: Список найденных дисков
        """
        return self._connection.system_service().disks_service().list(search=f'name={name}')

    def get_host_stat(self, host: types.Host) -> dict:
        """
        Получение статистики хоста

        Пример:

        {
            'memory.total': 67271393280.0, \n
            'memory.used': 62562395750.0, \n
            'memory.free': 4708997530.0, \n
            'memory.shared': 0.0, \n
            'memory.buffers': 0.0, \n
            'memory.cached': 0.0, \n
            'swap.total': 33754710016.0, \n
            'swap.free': 32800505856.0, \n
            'swap.used': 954204160.0, \n
            'swap.cached': 0.0, \n
            'ksm.cpu.current': 0.0, \n
            'cpu.current.user': 10.0, \n
            'cpu.current.system': 2.0, \n
            'cpu.current.idle': 88.0, \n
            'cpu.load.avg.5m': 1.0, \n
            'boot.time': 1548670267.0, \n
            'hugepages.1048576.free': 0.0, \n
            'hugepages.2048.free': 0.0 \n
        }
        """
        stats = self._connection.follow_link(host.statistics)
        return {stat.name: stat.values[0].datum for stat in stats}

    def get_templates_by_name(self, name: str) -> list:
        """
        Поиск шаблонов по имени

        :param name: Имя шаблона
        :return: Список найденных шаблонов
        """
        return self._connection.system_service().templates_service().list(search=f'name={name}')

    def get_template_by_name(self, name: str) -> types.Template:
        """
        Получение одного шаблона по имени

        :param name: Имя шаблона
        """
        result = self.get_templates_by_name(name)

        if len(result) > 1:
            raise TooManyItemsException(len(result))

        return result[0] if result else None

    def get_host_free_memory(self, host: types.Host) -> int:
        """
        Получение объема свободной ОЗУ хоста
        :param host: Исследуемый хост
        :return: Объем ОЗУ в байтах
        """
        return int(self.get_host_stat(host)['memory.free'])

    def create_vm(
        self,
        name: str,
        host: types.Host,
        memory: int,
        cpu_sockets: int,
        template=None
    ) -> types.Vm:
        """
        Создание виртуальной машины

        :param name: Название ВМ
        :param host: Хост ВМ
        :param memory: Объем памяти ВМ в байтах
        :param cpu_sockets: Количество ядер для ВМ
        :param template: Шаблон ВМ
        :return: Созданная ВМ
        """

        vms_service = self._connection.system_service().vms_service()

        free_memory = self.get_host_free_memory(host)

        if free_memory < memory:
            raise NotEnoughMemoryException(free_memory, memory)

        return vms_service.add(
            vm=types.Vm(
                name=name,
                cluster=host.cluster,
                template=template or types.Template(name='Blank'),
                cpu=types.Cpu(
                    topology=types.CpuTopology(
                        sockets=cpu_sockets
                    )
                ),
                memory=memory,
                memory_policy=types.MemoryPolicy(
                    guaranteed=memory,
                    max=memory
                ),
                placement_policy=types.VmPlacementPolicy(
                    affinity=types.VmAffinity.USER_MIGRATABLE,
                    hosts=[host],
                )
            )
        )

    def remove_vm(self, vm: types.Vm):
        """
        Удаление ВМ
        """
        self._connection.system_service().vms_service().vm_service(vm.id).remove()

    def start_vm(self, vm: types.Vm):
        """
        Запуск ВМ
        """
        self._connection.system_service().vms_service().vm_service(vm.id).start()

    def reboot_vm(self, vm: types.Vm):
        """
        Перезагрузка ВМ
        """
        self._connection.system_service().vms_service().vm_service(vm.id).reboot()

    def stop_vm(self, vm: types.Vm):
        """
        Принудительное выключение ВМ
        """
        self._connection.system_service().vms_service().vm_service(vm.id).stop()

    def shutdown_vm(self, vm: types.Vm):
        """
        Запрос на остановку ВМ
        """
        self._connection.system_service().vms_service().vm_service(vm.id).shutdown()

    def get_vms_by_name(self, name: str) -> list:
        """
        Поиск виртуальных машин по имени

        :param name: Название ВМ
        :return: Список найденных ВМ
        """
        return self._connection.system_service().vms_service().list(search=f'name={name}')

    def get_vm_by_name(self, name: str) -> types.Vm:
        """
        Получение одной ВМ по имени

        :param name: Имя ВМ
        """
        result = self.get_vms_by_name(name)

        if len(result) > 1:
            raise TooManyItemsException(len(result))

        return result[0] if result else None

    def get_vm_status_by_name(self, name: str) -> str:
        """
        Получение статуса ВМ
        """
        vm = self.get_vm_by_name(name)
        return vm.status

    def rename_vm(self, vm: types.Vm, new_name: str):
        """
        Изменение имени ВМ
        :param vm: ВМ
        :param new_name: Новое имя
        """
        vm_service = self._connection.system_service().vms_service().vm_service(vm.id)
        vm_service.update(
            types.Vm(
                name=new_name
            )
        )

    def set_vm_cpu_shares(self, vm: types.Vm, cpu_sockets: int):
        """
        Установить количество ядер у ВМ

        :param vm: ВМ
        :param cpu_sockets: Количество ядер
        """
        vm_service = self._connection.system_service().vms_service().vm_service(vm.id)
        vm_service.update(
            types.Vm(
                cpu=types.Cpu(
                    topology=types.CpuTopology(
                        sockets=cpu_sockets
                    )
                )
            )
        )

    def set_vm_memory(self, vm: types.Vm, memory: int):
        """
        Установить количество ОЗУ

        :param vm: ВМ
        :param memory: Количество ОЗУ
        """
        vm_service = self._connection.system_service().vms_service().vm_service(vm.id)
        vm_service.update(
            types.Vm(
                memory=memory,
                memory_policy=types.MemoryPolicy(
                    guaranteed=memory,
                    max=memory
                ),
            )
        )

    def get_storage_domains_by_name(self, name: str) -> list:
        """
        Получение storage domains по имени

        :param name: Название домена
        :return: Список StorageDomain
        """
        return self._connection.system_service().storage_domains_service().list(search=f'name={name}')

    def get_storage_domain_by_name(self, name: str) -> types.StorageDomain:
        """
        Получение одного storage domain по имени

        :param name: Имя домена
        """
        result = self.get_storage_domains_by_name(name)

        if len(result) > 1:
            raise TooManyItemsException(len(result))

        return result[0] if result else None

    def create_vm_disk(
        self,
        vm: types.Vm,
        storage_domain: types.StorageDomain,
        name: str,
        description: str,
        size: int,
        disk_format: types.DiskFormat = types.DiskFormat.RAW,
        bootable: bool = False,
        active: bool = True,
        wipe_after_delete: bool = True,
        read_only: bool = False,
        shareable: bool = False,
    ) -> types.DiskAttachment:
        disk_service = self._connection.system_service().vms_service().vm_service(vm.id).disk_attachments_service()

        return disk_service.add(
            types.DiskAttachment(
                disk=types.Disk(
                    name=name,
                    description=description,
                    format=disk_format,
                    provisioned_size=size,
                    storage_domains=[
                        storage_domain
                    ],
                    wipe_after_delete=wipe_after_delete,
                    read_only=read_only,
                    shareable=shareable,
                ),
                interface=types.DiskInterface.VIRTIO,
                bootable=bootable,
                active=active,
            ),
        )
