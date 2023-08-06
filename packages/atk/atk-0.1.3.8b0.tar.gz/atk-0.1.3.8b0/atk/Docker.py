# -*- coding:utf-8 -*-


import os
import inspect
import getpass
import platform
import subprocess
from havedocker.DockerError import *


class AgilityDocker(object):
    def __init__(self,):
        self.DockerHelp = subprocess.Popen(
            'docker --help',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        self.DockerVersion = subprocess.Popen(
            'docker -v',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT).communicate()[0].decode()
        self.DockerMachineVersion = subprocess.Popen(
            'docker-machine version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        ).communicate()[0].decode()
        self.DockerStatus = self.DockerHelp.wait()
        if self.DockerStatus == 1:
            raise DockerInitRunError('当前主机没有docker.server')
        elif self.DockerStatus == 127:
            raise DockerInitRunError(
                '当前主机并不存在docker指令集 status={}'.format(
                    self.DockerHelp.wait()))
        elif self.DockerStatus == 128:
            raise DockerInitRunError(
                '效验docker无效， status={}'.format(
                    self.DockerHelp.wait()))

    @staticmethod
    def __get__function_name():
        return inspect.stack()[1][3]

    @staticmethod
    def query(formatting=False, self_object_='vessel'):
        """
            # DockerQuery方法，用来查看所有在后台运行的docker实例化对象
            :param self_object_: ['vessel' / 'images'] 默认为'vessel'，只接收所有实例化容器信息。
            为'images'时，将收集本地docker中所存在images。
            :param formatting: 默认为False。不为True时，只返回实例化vessel对象组的dict或images对象组的dict。
            为True时，不做修改将直接返回str
            :return: 如果docker存在后台运行容器，返回容器ID字典，dict_key为vessel的ID，值为除ID之外所有查询到的结果。
            反之，只返回False。当help=True时，将返回'help'
        """
        if self_object_ == 'vessel':
            cmd = subprocess.Popen('docker ps -a', shell=True, stdout=subprocess.PIPE)
            cmd = cmd.communicate()[0].decode()
            if formatting:
                return cmd
            if cmd.count('\n') > 1:
                vessel_list = cmd.split('\n')
                vessel = {}
                vessel_type = vessel_list[0]

                vessel_id = [
                    vessel_type.index('CONTAINER ID'),
                    vessel_type.index('IMAGE')]
                vessel_image = [
                    vessel_type.index('IMAGE'),
                    vessel_type.index('COMMAND')]
                vessel_command = [
                    vessel_type.index('COMMAND'),
                    vessel_type.index('CREATED')]
                vessel_created = [
                    vessel_type.index('CREATED'),
                    vessel_type.index('STATUS')]
                vessel_status = [
                    vessel_type.index('STATUS'),
                    vessel_type.index('PORTS')]
                vessel_ports = [
                    vessel_type.index('PORTS'),
                    vessel_type.index('NAMES')]
                vessel_names = [
                    vessel_type.index('NAMES'),
                    len(vessel_type) + 15]
                vessel_body = vessel_list[1:-1]

                for name in vessel_body:
                    vessel['{}'.format((name[vessel_id[0]:vessel_id[1]]).rstrip())] = {
                        'image': (name[vessel_image[0]:vessel_image[1]]).rstrip(),
                        'command': (name[vessel_command[0]:vessel_command[1]]).rstrip(),
                        'created': (name[vessel_created[0]:vessel_created[1]]).rstrip(),
                        'status': (name[vessel_status[0]:vessel_status[1]]).rstrip(),
                        'ports': (name[vessel_ports[0]:vessel_ports[1]]).rstrip(),
                        'names': (name[vessel_names[0]:vessel_names[1]]).rstrip()
                    }
                return vessel
            else:
                return False
        elif self_object_ == 'images':
            cmd = subprocess.Popen('docker images', shell=True, stdout=subprocess.PIPE)
            cmd = cmd.communicate()[0].decode()
            if formatting:
                return cmd
            if cmd.count('\n') > 1:
                images_list = cmd.split('\n')
                images = {}
                images_type = images_list[0]
                images_repository = [
                    images_type.index('REPOSITORY'),
                    images_type.index('TAG')]
                images_tag = [
                    images_type.index('TAG'),
                    images_type.index('IMAGE ID')]
                images_image_id = [
                    images_type.index('IMAGE ID'),
                    images_type.index('CREATED')]
                images_created = [
                    images_type.index('CREATED'),
                    images_type.index('SIZE')]
                images_size = [images_type.index('SIZE'), len(images_type) + 1]
                images_body = images_list[1:-1]
                for name in images_body:
                    images['{}'.format((name[images_repository[0]:images_repository[1]]).rstrip())] = {
                        'tag': (name[images_tag[0]:images_tag[1]]).rstrip(),
                        'image_id': (name[images_image_id[0]:images_image_id[1]]).rstrip(),
                        'created': (name[images_created[0]:images_created[1]]).rstrip(),
                        'size': (name[images_size[0]:images_size[1]]).rstrip()
                    }
                return images
            else:
                return False

    @staticmethod
    def pull(images_name=None):
        """
            # pull，拉取镜像
            :param images_name: 提供的镜像名，以作拉取对象
            :return: 默认返回执行命令结果，如果未提供拉取镜像名称，抛出异常。
        """
        if images_name:
            commend = os.popen('docker pull {}'.format(images_name)).read()
            return commend
        else:
            raise DockerPullError(
                "images_name:'{}'is None, 需要提供一个镜像名参数".format(images_name))

    def run(self, images_name=None,
            run_cmd='/bin/bash',
            vessel_name=None,
            network=None,
            ip=None,
            cpu_shares=None,
            cpu_amount=None,
            block_weight=None,
            ):
        """
            # existing problem
                memory: int 100
                memory_swap: int memory+swap
                暂未设定memory、BlockIO相关参数
            # 实例化容器对象，并返回实例化对象的唯一HASH64中前12位，因为这是容器ID
            :param images_name: 默认为None
            :param run_cmd: 默认实例化运行镜像时，将会以'/bin/bash'
            :param vessel_name: str
            :param network: 指定虚拟网卡类型, 可指定自定义网卡类型 str
            :param ip: 指定IP地址 str
            :param cpu_shares: int 0~65535 限定cpu权重
            :param cpu_amount: int [0, 1, 2] 限定cpu颗数
            :param block_weight: int 10~1000 限定磁盘权重
            :return: 返回HASH64[:12]，以及命令执行结果
        """
        self_commend = 'docker run -itd'
        if not images_name:
            raise DockerRunImageError('{}镜像不存在，无法实例化。'.format(images_name))
        if run_cmd is None:
            raise DockerRunImageTypeError('{} Error'.format(run_cmd))
        if vessel_name is not None:
            if not isinstance(vessel_name, str):
                raise DockerRunImageTypeError('{} Namespace Error')
            else:
                vessel_name = ' --name %s' % vessel_name
        else:
            vessel_name = ''
        if cpu_shares is not None:
            if not (0 <= cpu_shares <= 65535):
                raise DockerRunImageTypeError(
                    '{} Type is int, -128<= cpu_shares <=127, number error'.format(cpu_shares))
            else:
                cpu_shares = ' --cpu-shares {}'.format(cpu_shares)
        else:
            cpu_shares = ''
        if cpu_amount is not None:
            if cpu_amount not in [0, 1, 2]:
                raise DockerRunImageTypeError(
                    '{} Type is int, 0< cpu_amount <=127, number error'.format(cpu_amount))
            else:
                cpu_amount = ' -c {}'.format(cpu_amount)
        else:
            cpu_amount = ''
        if block_weight is not None:
            if not (10 < block_weight <= 1000):
                raise DockerRunImageTypeError(
                    '{} Type is int, 0< block_weight <=65535, number error'.format(block_weight))
            else:
                block_weight = ' --block-weight {}'.format(block_weight)
        else:
            block_weight = ''
        if network:
            if isinstance(network, str):
                network_str = self.query_network(formatting=True)
                if network in network_str:
                    network = ' --network {}'.format(network)
                else:
                    raise DockerRunImageError(
                        "network:{}, 提供了错误的虚拟网卡名称".format(network))
            else:
                raise DockerRunImageError(
                    "network:{}, 提供了错误格式的虚拟网卡".format(type(network)))
        else:
            network = ''
        if ip:
            if isinstance(type(ip), str):
                network = ' --ip {}'.format(ip)
            else:
                raise DockerRunImageError(
                    "ip:{], 提供了错误格式的虚拟网卡".format(type(ip)))
        else:
            ip = ''
        self_commend = '{}{}{}{}{}{}{} {} {}'.format(self_commend,
                                                     vessel_name,
                                                     cpu_shares,
                                                     cpu_amount,
                                                     block_weight,
                                                     network,
                                                     ip,
                                                     images_name,
                                                     run_cmd)
        commend = os.popen(self_commend).read()
        if commend.count('\n') > 1:
            images_id = commend.split('\n')[-1][:12]
        else:
            images_id = commend[:12]
        return [images_id, commend]

    def remove_object_(self, exclude=None, self_object_='vessel'):
        """
            # remove_object_ 用来删除实例化容器
            :param exclude: 默认为None。添加排除项，除Exclude之外删除
            :param self_object_: 默认对象为实例化容器 ['vessel' / 'images']

            :return: 默认返回None。如果docker后台运行的容器介被删除，将以True作为尾值闭包。
            如果cmd_ps_a()并没有给出正确值，那么将返回False。当help=True时，将返回'help'
        """
        vessel_id = self.query()
        images_id = self.query(self_object_='images')
        if self_object_ == 'vessel':
            if vessel_id:
                if exclude:
                    for e in exclude:
                        if e in vessel_id.keys():
                            del vessel_id[e]
                        else:
                            pass
                    for j in vessel_id:
                        os.popen('docker rm -f {}'.format(j))
                else:
                    for j in vessel_id:
                        os.popen('docker rm -f {}'.format(j))
                return True
            else:
                return False
        elif self_object_ == 'images':
            if images_id:
                if exclude:
                    for E in exclude:
                        if E in images_id.keys():
                            del images_id[E]
                        else:
                            pass
                    for idk in images_id.keys():
                        os.popen(
                            'docker rmi -f {}'.format(images_id[idk]['image_id']))
                else:
                    for id_ in images_id:
                        os.popen(
                            'docker rmi -f {}'.format(images_id[id_]['image_id']))
                return True
            else:
                return False

    @staticmethod
    def cp(goods=None, vessel=None, path=':/'):
        """
            # cp 用于就文件、文件夹复制移动到实例化容器指定路径上
            :param goods: 被复制对象(file/dir)
            :param vessel: 实例化容器
            :param path: 实例化容器中的指定路径

            :return: goods和vessel同时存在(True), 将返回True。不满条件，返回False。当help=True时，将返回'help'
        """
        if goods and vessel:
            os.popen('docker cp {} {}{}'.format(goods, vessel, path))
            return True
        else:
            return False

    def history(self, argument=None, entire=False):
        """
            # history 将对镜像进行分层树
            :param argument: 镜像repository
            :param entire: 默认为False， entire=False时，argument需要提供参数。
                    entire=True时, argument不需要参数支持将返回所有镜像的history

            :return: *args为单值时，返回command。*args为list时，返回key-value。
        """
        if not entire:
            try:
                assert argument
            except AssertionError:
                raise DockerHistoryArgsError(
                    '{}缺少参数，argument=False'.format(argument))
            if isinstance(argument, str):
                command = subprocess.Popen(
                    'docker history {}'.format(argument),
                    shell=True, stdout=subprocess.PIPE)
                command = command.communicate()[0].decode()
                return command
            elif isinstance(argument, list):
                history = {}
                for sh in argument:
                    command = subprocess.Popen(
                        'docker history {}'.format(argument),
                        shell=True, stdout=subprocess.PIPE)
                    command = command.communicate()[0].decode()
                    history[sh] = command
                return history
            else:
                raise DockerHistoryTypeError(
                    '{} unknown Type()'.format(argument))
        else:
            cmd = self.query(self_object_='images')
            history = {}
            for sh in cmd.keys():
                if 'none' in sh:
                    continue
                else:
                    command = subprocess.Popen(
                        'docker history {}'.format(sh),
                        shell=True, stdout=subprocess.PIPE)
                    command = command.communicate()[0].decode()
                    history[sh] = command
            return history

    @staticmethod
    def docker_file(
        from_=None,
        maintainer=platform.system(),
        run=None,
        cmd=None,
        copy=None,
        add=None,
        expose=None,
        workdir=None,
        entrypoint=None,
        env=None,
        volume=None,
    ):
        """
            # existing problem
            - 关于dockerfile文件中，MAINTAINER作者项暂时以兼容方式获取username
            - 关于dockerfile-body中，暂时采用dict方式进行存储。
            - 暂未编写VOLUME，
            :param from_: 默认None，镜像源
            :param maintainer : 默认为系统名称，支持自定义
            :param run: 例子 RUN=['pip3 install tornado', 'apt update']，type=str/list
            :param cmd: 例子 CMD=['apt install httpd', 'yum install tree'], type=str/list
            :param copy: 例子 COPY=[['EPC_test', '/'], [3]] type=str/list
                    COPY位置摆放逻辑：并不以下标为准，以存在的元素数量。如果有七条命令，那么指定的位置将为第几条命令。不存在0
            :param add: 例子 ADD=[['nginx.1.14.2.tar', '/'], [4]] type=str/list
            :param expose: 例子 EXPOSE=[80, 8080, 443], type=int/list 始终位于dockerfile最底层
            :param workdir: 例子 WORKDIR=[[['/root'], ['/bin']], [2, 3]], type=str/list
            :param entrypoint: 例子 ENTRYPOINT=[[['/bin/echo'], ['Hello World']], [2, 3]]
            :param env: 例子 type=str/list
                    ENV=[
                         [['WELCOME "You are in my container, welcome!"'],
                          ['name Cloud Man ENTRYPOINT echo "Hello, $name"']],
                         [2, 3]
                        ]
            :param volume: 例子 VOLUME=["/data1", "/data2"]，位于FROM、MAINTAINER之后 type=str/list

            :return: 默认返回None， 当help=True时，将返回'help'
        """
        dockerfile = []
        os_name = maintainer
        if isinstance(from_, str):
            dockerfile.append('FROM {}'.format(from_))
        else:
            raise DockerfileError("from_:{}错误类型，查询help".format(type(from_)))

        if os_name == 'LINUX':
            username = getpass.getuser()
            dockerfile.append('MAINTAINER {} {}'.format(os_name, username))
        elif os_name == 'Windows':
            username = os.environ['USERNAME']
            dockerfile.append('MAINTAINER {} {}'.format(os_name, username))
        else:
            if maintainer is str:
                dockerfile.append('MAINTAINER {}'.format(maintainer))
            else:
                os_name = 'None'
                username = 'None'
                dockerfile.append('MAINTAINER {} {}'.format(os_name, username))

        type_volume = type(volume)
        if type_volume is list:
            for volume_ in volume:
                dockerfile.append('VOLUME {}'.format(volume_))
        elif type_volume is 'NoneType':
            pass

        type_run = type(run)
        if type_run is list:
            for run_ in run:
                dockerfile.append('RUN {}'.format(run_))
        elif type_run is 'NoneType':
            pass

        type_command = type(cmd)
        if type_command is list:
            for command in cmd:
                dockerfile.append('CMD {}'.format(command))
        elif type_command is 'NoneType':
            pass

        def location(object_, head_cmd=None):
            type_copy = type(object_)
            if type_copy is list:
                if len(object_) > 1:
                    if len(object_[0]) == len(object_[1]):
                        if type_run is 'NoneType':
                            for cmd_ in object_[0]:
                                dockerfile.append(
                                    '{} {}'.format(head_cmd, cmd_))
                        else:
                            for body in object_[0]:
                                dockerfile.append(
                                    '{} {}'.format(head_cmd, body))
                            for num in object_[1]:
                                dockerfile.remove('{} {}'.format(
                                    head_cmd, object_[0][object_[1].index(num)]))
                                dockerfile.insert(
                                    num - 1, '{} {}'.format(head_cmd, object_[0][object_[1].index(num)]))
                    else:
                        raise DockerfileError(
                            '{} 提供了{} body参数， 提供了{} 位置参数'.format(
                                head_cmd, len(
                                    object_[0]), len(
                                    object_[1])))
                elif len(object_):
                    for cmd_ in object_[0]:
                        dockerfile.append('{} {}'.format(head_cmd, cmd_))
                else:
                    pass
            elif type_copy is str:
                dockerfile.append('{} {}'.format(head_cmd, object_))
            elif type_copy is 'NoneType':
                pass

        location(object_=copy, head_cmd='COPY')
        location(object_=add, head_cmd='ADD')
        location(object_=workdir, head_cmd='WORKDIR')
        location(object_=entrypoint, head_cmd='ENTRYPOINT')
        location(object_=env, head_cmd='ENV')

        type_port = type(expose)
        if type_port is list:
            for port in expose:
                dockerfile.append('EXPOSE {}'.format(port))
        elif type_port is 'NoneType':
            pass
        elif type_port is int:
            dockerfile.append('EXPOSE {}'.format(expose))

        if 'FROM' in dockerfile[0]:
            pass
        else:
            raise DockerfileLocationError(
                "Your dockerfile first line is {}, Is should be 'FROM ...'!".format(
                    (dockerfile[0].split(' '))[0]))

        for element in dockerfile:
            print(element)

    def vessel_status(self,
                      argument='unpause',
                      vessel_id=None,
                      ):
        """
            vessel_status 方法，暂停或继续运行容器。区别于cmd_run_vessel()方法，提供针对容器管理的方案。
            :param argument: 默认'unpause'， 可选参数 ['unpause' / 'pause']
            :param vessel_id: 实例化容器ID，
            :return: 默认返回None， 当help=True时，将返回'help'
        """
        if vessel_id is None:
            raise DockerStatusError('vessel_status需要vessel_id参数， 而非None')
        vessel_list = self.query()
        if argument == 'unpause':
            if vessel_id in vessel_list.keys():
                if '(Paused)' in vessel_list.get(vessel_id)['status']:
                    subprocess.Popen(
                        'docker {} {}'.format(argument, vessel_id),
                        shell=True, stdout=subprocess.PIPE)
                else:
                    raise DockerStatusError(
                        '{}容器状态并非...(Paused)，unpause失效'.format(vessel_id))
            else:
                raise DockerStatusError('{}容器未存在， unpause失效'.format(vessel_id))
        elif argument == 'pause':
            if vessel_id in vessel_list.keys():
                subprocess.Popen(
                    'docker {} {}'.format(argument, vessel_id),
                    shell=True, stdout=subprocess.PIPE)
            else:
                raise DockerStatusError('{}容器未存在， pause失效'.format(vessel_id))
        else:
            raise DockerStatusError('argument={}，未知指令'.format(argument))

    @staticmethod
    def push(images_name=None):
        """
            # push，推送镜像
            :param images_name: 提供的镜像名，以作推送对象
            :return: 如果被推送的镜像存在，程序执行完成之后将会返回True。
        """
        if not images_name:
            raise DockerPushError(
                "images_name:'{}'is None, 需要提供一个镜像名参数".format(images_name))
        commend = os.popen('docker push {}'.format(images_name)).read()
        print(commend)
        return True

    @staticmethod
    def create_network(
            create=True,
            driver='bridge',
            subnet=None,
            gateway=None,
            network_name=None,
    ):
        """
            # create_network
            :param create: 默认True， create=True时，意为创建虚拟网卡  bool值
            :param driver: 默认None'，指定虚拟网卡类型 ['bridge' / 'overlay' / 'macvlan'] 'host'和'null'无法成为有效命令
            :param subnet: 默认None，提供网段信息 [127.0.0.1/24] str类型
            :param gateway: 默认None，提供网关信息 [192.168.1.1] str类型
            :param network_name: 默认为None，新建虚拟网卡的名称。如果query=False，NetWorkName若为None将抛出异常
            :return: 默认返回成功执行的命令结果，同样包含错误命令。
        """
        if not create:
            raise DockerNetWorkError("关键参数错误：create必须为True")
        if not network_name:
            raise DockerNetWorkError(
                "NetWorkName:{} not is None，需要提供参数".format(network_name))
        if type(network_name) not in [str, None]:
            raise DockerNetWorkError("create=True时，必须提供NetWorkName参数")
        if driver not in ['bridge', 'overlay', 'macvlan']:
            raise DockerNetWorkError(
                "--driver {}提供的参数错误，查询help".format(driver))
        if not subnet and not gateway and network_name:
            commend = os.popen(
                'docker network create {}'.format(network_name)).read()
            return commend
        if subnet and not gateway and network_name:
            raise DockerNetWorkError("--gateway 需要提供参数")
        elif not subnet and gateway and network_name:
            raise DockerNetWorkError("--subnet 需要提供参数")
        elif not subnet and not gateway and driver and network_name:
            commend = os.popen('docker network create --driver {} {}'.format(
                driver, network_name)).read()
            return commend
        else:
            if isinstance(
                subnet,
                str) and isinstance(
                gateway,
                str) and isinstance(
                driver,
                    str):
                if '/' in subnet:
                    commend = os.popen(
                        'docker network create --driver {} --subnet {} --subnet {} {}'.format(
                            driver, subnet, subnet, network_name)).read()
                    return commend
                else:
                    raise DockerNetWorkError(
                        "--subnet 需要标准IP地址格式，当前类型不符，查询help")
            else:
                raise DockerNetWorkError(
                    "subnet | gateway | driver 需要str类型，当前类型不符")

    def query_network(
            self,
            formatting=False,
            inspect_=False,
            network_name=None,
    ):
        """
            # query_network，用于查询docker中的虚拟网卡
            :param formatting: 默认False， 不做处理直接返回执行结果。formatting=True，将返回字典
            :param inspect_: 默认False，Inspect=True时，必须提供NetworkName值
            :param network_name: 默认None，需要时，传入str值
            :return: 返回结果
        """
        if inspect_:
            if isinstance(network_name, str):
                if network_name in self.query_network():
                    command = subprocess.Popen(
                        'docker network inspect {}'.format(network_name),
                        shell=True, stdout=subprocess.PIPE)
                    command = command.communicate()[0].decode()
                    return command
                else:
                    raise DockerQueryNetworkError(
                        "NetworkName:{}错误传参".format(network_name))
            else:
                raise DockerQueryNetworkError(
                    "NetworkName:{} 错误类型或未传参".format(
                        type(network_name)))
        else:
            if isinstance(network_name, str):
                raise DockerQueryNetworkError("只查询时，无需NetworkName参数")
            command = subprocess.Popen(
                'docker network ls', shell=True, stdout=subprocess.PIPE)
            command = command.communicate()[0].decode()
            if formatting:
                network_list = command.split('\n')
                network = {}
                vessel_type = network_list[0]

                network_id = [
                    vessel_type.index('NETWORK ID'),
                    vessel_type.index('NAME')]
                network_name = [
                    vessel_type.index('NAME'),
                    vessel_type.index('DRIVER')]
                network_driver = [
                    vessel_type.index('DRIVER'),
                    vessel_type.index('SCOPE')]
                vessel_scope = [
                    vessel_type.index('SCOPE'),
                    len(vessel_type) + 1]
                vessel_body = network_list[1:-1]

                for name in vessel_body:
                    network['{}'.format((name[network_id[0]:network_id[1]]).rstrip())] = {
                        'name': (name[network_name[0]:network_name[1]]).rstrip(),
                        'driver': (name[network_driver[0]:network_driver[1]]).rstrip(),
                        'scope': (name[vessel_scope[0]:vessel_scope[1]]).rstrip()
                    }
                return network
            else:
                return command

    def remove_network(self, exclude=None, remove_network_name=None):
        """
            # remove_network，用于删除指定的虚拟网卡
            :param exclude: 默认为None，添加排除项 str / list
            :param remove_network_name: 选择删除指定的虚拟网卡名称
            :return: 返回执行结果
        """
        if remove_network_name is None:
            if isinstance(exclude, str):
                network_list = [
                    i for i in self.query_network(
                        formatting=True)]
                if exclude in network_list:
                    network_list.remove(exclude)
                    for name in network_list:
                        subprocess.Popen(
                            'docker network rm {}'.format(name),
                            shell=True, stdout=subprocess.PIPE)
                return True
            elif isinstance(exclude, list):
                network_list = [
                    i for i in self.query_network(
                        formatting=True)]
                if exclude in network_list:
                    for exclude in network_list:
                        network_list.remove(exclude)
                    if network_list is []:
                        return True
                    for name in network_list:
                        subprocess.Popen(
                            'docker network rm {}'.format(name),
                            shell=True, stdout=subprocess.PIPE)
                return True
            else:
                raise DockerRmNetworkError("Exclude:{} 参数需要提供".format(exclude))
        elif isinstance(remove_network_name, str):
            subprocess.Popen(
                'docker network rm {}'.format(remove_network_name),
                shell=True, stdout=subprocess.PIPE)
            return True
        elif isinstance(remove_network_name, list):
            commend = 'docker network rm'
            for name in remove_network_name:
                commend = commend + ' ' + name
            subprocess.Popen(
                'docker network rm {}'.format(commend),
                shell=True, stdout=subprocess.PIPE)
            return True
        else:
            raise DockerRmNetworkError(
                "DockerRmNetwork:{}未知类型".format(
                    type(remove_network_name)))

    def connect_network(self, network=None, vessel_name=None):
        """
            # connect_network，用于对指定容器添加虚拟网卡
            :param network: 默认None，指定虚拟网卡名称
            :param vessel_name: 默认None，指定容器ID
            :return:默认返回执行结果
        """
        if isinstance(network, str) and isinstance(vessel_name, str):
            vessel_name = [self.query()[i]['names']
                           for i in self.query()]
            if vessel_name in self.query():
                if network in self.query_network(formatting=True):
                    subprocess.Popen(
                        'docker network connect {} {}'.format(
                            network, vessel_name), shell=True, stdout=subprocess.PIPE)
                    return True
                else:
                    raise DockerConnectNetworkError(
                        "Network:{}未知参数".format(network))
            if vessel_name in vessel_name:
                if network in self.query_network(formatting=True):
                    subprocess.Popen(
                        'docker network connect {} {}'.format(
                            network, vessel_name), shell=True, stdout=subprocess.PIPE)
                    print(
                        'docker network connect {} {}'.format(
                            network, vessel_name))
                    return True
                else:
                    raise DockerConnectNetworkError(
                        "Network:{}未知参数".format(network))
            else:
                raise DockerConnectNetworkError(
                    "VesselName:{}未知参数".format(vessel_name))
        elif isinstance(network, str) and not vessel_name:
            raise DockerConnectNetworkError(
                "VesselName:{}未传递参数".format(vessel_name))
        elif isinstance(vessel_name, str) and not network:
            raise DockerConnectNetworkError("Network:{}未传递参数".format(network))
        else:
            raise DockerConnectNetworkError(
                "DockerConnectNetworkError:未传递任何参数!")

    def port(self, vessel_name=None):
        """
            # port，用于查询指定容器下，所有端口信息
            :param vessel_name: 提供指定容器的ID或名称 [vesselID / vesselName]
            :return: 默认返回执行命令的结果
        """
        if isinstance(vessel_name, str):
            vessel_list = self.query()
            names = []
            if vessel_name in vessel_list.keys():
                cmd = subprocess.Popen('docker port {}'.format(vessel_name),
                                       shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       bufsize=1)
                return cmd.communicate()[0].decode()
            else:
                for vessel_name_value in vessel_list:
                    names.append(vessel_list.get(vessel_name_value)['names'])
                if vessel_name in names:
                    cmd = subprocess.Popen(
                        'docker port {}'.format(vessel_name),
                        shell=True, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        bufsize=1)
                    return cmd.communicate()[0].decode()
                else:
                    raise DockerPortError(
                        "Vessel_name:{}，不存在于docker实例化容器列表中".format(vessel_name))

        else:
            raise DockerPortError(
                "Vessel_name:{}，错误的vessel_name类型".format(
                    type(vessel_name)))

    def tag(self, old_name=None, new_name=None):
        """
            # tag，用来修改镜像标签
            :param old_name: 原镜像名称 str
            :param new_name: 新镜像名称 str
            :return: 返回命令执行状态
        """
        docker_images = self.query(self_object_='images')
        if isinstance(old_name, str):
            if isinstance(new_name, str):
                images_list = []
                for name in docker_images:
                    images_list.append(docker_images[name]['image_id'])
                if old_name in docker_images or old_name in images_list:
                    subprocess.Popen(
                        'docker tag {} {}'.format(old_name, new_name),
                        shell=True, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        bufsize=1)
                else:
                    raise DockerTagError("oldname:{}未知参数，镜像名不存在")
            elif not new_name:
                raise DockerTagError("newName:{}未知参数，可查询帮助".format(new_name))
            else:
                raise DockerTagError(
                    "newName:{}提供了错误类型，可查询帮助".format(
                        type(new_name)))
        else:
            raise DockerTagError(
                "oldName:{}提供了错误类型，可查询帮助".format(
                    type(old_name)))

    def top(self, vessel_name=None):
        """
            # top，查询容器信息
            :param vessel_name: 默认None，提供容器名称或ID str
            :return: 默认返回执行结果
        """
        vessel_dict = self.query()
        vessel_list = [id_ for id_ in vessel_dict]
        for id_ in vessel_dict:
            vessel_list.append(vessel_dict[id_]['names'])
        if isinstance(vessel_name, str):
            if vessel_name in vessel_list:
                command = subprocess.Popen(
                    'docker top {}'.format(vessel_name),
                    shell=True, stdout=subprocess.PIPE)
                command = command.communicate()[0].decode()
                return command
            else:
                raise DockerTopError(
                    "vessel_name:{}，不存在的容器名称或ID".format(vessel_name))
        else:
            raise DockerTopError(
                "vessel_name:{}，错误类型，查询help".format(
                    type(vessel_name)))

    def logs(self, vessel_name=None, block=False):
        """
            # logs，用于输出容器启动以来的日志信息
            :param vessel_name: 默认None， 提供容器ID
            :param block: 默认False，声明：block=False时，将进行阻塞
            :return: 默认返回执行结果
        """
        vessel_dict = self.query()
        vessel_list = [id_ for id_ in vessel_dict]
        for id_ in vessel_dict:
            vessel_list.append(vessel_dict[id_]['names'])
        if isinstance(vessel_name, str):
            if vessel_name in vessel_list:
                if block:
                    command = subprocess.Popen('docker stats',
                                               shell=True, stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               bufsize=1)
                    data = []
                    while command.poll() is None:
                        try:
                            read_command = command.stdout.readline().decode('GBK')
                            data.append(read_command)
                            if read_command == '':
                                pass
                            else:
                                print(read_command)
                        except KeyboardInterrupt:
                            return data
                else:
                    command = subprocess.Popen(
                        "docker logs {}".format(vessel_name),
                        shell=True, stdout=subprocess.PIPE)
                    command = command.communicate()[0].decode()
                    return command
            else:
                print(vessel_list)
                raise DockerLogsError(
                    "vessel_name:{}，提供未知参数".format(vessel_name))
        else:
            raise DockerLogsError(
                "vessel_name:{}，错误类型，查询help".format(
                    type(vessel_name)))

    def query_volume(self, inspect_name=None):
        """
            # query_volume，查询卷
            :param inspect_name: 默认None，提供一个或多个卷名 str/list
            :return: 默认返回执行结果
        """
        if not inspect_name:
            command = subprocess.Popen(
                'docker volume ls', shell=True, stdout=subprocess.PIPE)
            command = command.communicate()[0].decode()
            if command.count('\n') > 1:
                volume_list = command.split('\n')
                volume = {}
                volume_type = volume_list[0]

                volume_driver = [
                    volume_type.index('DRIVER'),
                    volume_type.index('VOLUME NAME')]
                volume_name = [
                    volume_type.index('VOLUME NAME'),
                    len(volume_type) + 70]

                volume_body = volume_list[1:-1]
                for name in volume_body:
                    volume['{}'.format((name[volume_name[0]:volume_name[1]]).rstrip())] = {
                        'driver': (name[volume_driver[0]:volume_driver[1]]).rstrip()
                    }
                return volume
            return None
        elif isinstance(inspect_name, str):
            volume_name = [name for name in self.query_volume()]
            if inspect_name in volume_name:
                command = subprocess.Popen(
                    'docker volume inspect {}'.format(inspect_name), shell=True, stdout=subprocess.PIPE)
                command = command.communicate()[0].decode()
                return command
            else:
                raise DockerQueryVolumeError(
                    "Inspect_name:{}，提供了未知参数".format(inspect_name))
        elif isinstance(inspect_name, list):
            volume_name = [name for name in self.query_volume()]
            command_body = 'docker volume inspect'
            for names in inspect_name:
                if names not in volume_name:
                    raise DockerQueryVolumeError(
                        "Inspect:{}，提供了未知参数".format(names))
                else:
                    command_body = '{} {}'.format(command_body, names)
            command = subprocess.Popen(command_body, shell=True, stdout=subprocess.PIPE)
            command = command.communicate()[0].decode()
            return command
        else:
            raise DockerQueryVolumeError(
                "Inspect:{}，错误类型".format(type(inspect_name)))

    def remove_volume(self, prune=True, rm=None):
        """
            # remove_volume，用于删除卷
            :param prune: 默认True，删除所有孤儿卷
            :param rm: 默认None，提供卷名 str/list
            :return: 默认返回执行结果
        """
        if prune:
            command = subprocess.Popen(
                'docker volume prune', shell=True, stdout=subprocess.PIPE)
            command = command.communicate()[0].decode()
            return command
        if isinstance(rm, str):
            volume_list = [name for name in self.query_volume()]
            if rm in volume_list:
                command = subprocess.Popen('docker volume rm {}'.format(rm), shell=True, stdout=subprocess.PIPE)
                command = command.communicate()[0].decode()
                return command
            else:
                raise DockerRmVolumeError("rm:{}，未知参数".format(rm))
        elif isinstance(rm, list):
            volume_list = [name for name in self.query_volume()]
            command_body = 'docker volume rm'
            for names in rm:
                if names not in volume_list:
                    raise DockerRmVolumeError("rm:{},未知参数".format(rm))
                else:
                    command_body = '{} {}'.format(command_body, names)
            command = subprocess.Popen(command_body, shell=True, stdout=subprocess.PIPE)
            command = command.communicate()[0].decode()
            return command
        else:
            raise DockerRmVolumeError("rm:{}，错误类型".format(rm))

    @staticmethod
    def create_volume(name=None):
        """
            # create_volume，用于创建卷
            :param name: 默认None，提供卷名 str
            :return: 默认返回执行结果
        """
        if isinstance(name, str):
            command = subprocess.Popen(
                'docker volume create {}'.format(name), shell=True, stdout=subprocess.PIPE)
            command = command.communicate()[0].decode()
            return command
        elif name is None:
            command = subprocess.Popen('docker volume create', shell=True, stdout=subprocess.PIPE)
            command = command.communicate()[0].decode()
            return command
        else:
            raise DockerCreateVolumeError

    def machine(self):
        """develop......"""
        pass

    @staticmethod
    def commit(vessel_name=None, image_name=None):
        """
            # commit 用于将容器持久化
            :param vessel_name: 默认None，提供容器名称或ID str
            :param image_name: 默认None，提供镜像名称或ID str
            :return: 默认返回执行结果
        """
        if isinstance(vessel_name, str):
            if isinstance(image_name, str):
                command = subprocess.Popen('docker commit {} {}'.format(vessel_name, image_name),
                                           shell=True, stdout=subprocess.PIPE)
                command = command.communicate()[0].decode()
                return command
            elif image_name is None:
                command = subprocess.Popen('docker commit {}'.format(vessel_name), shell=True, stdout=subprocess.PIPE)
                command = command.communicate()[0].decode()
                return command
            else:
                raise DockerCommitError("image_name:{}错误类型".format(type(image_name)))
        else:
            raise DockerCommitError("vessel_name:{}错误类型".format(type(vessel_name)))

    @staticmethod
    def stats():
        """
            # DockerStats方法，用于将终端结果同步显示
            # develop......
            :return: None
        """
        command = subprocess.Popen(
            'docker stats',
            shell=True, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1)
        while command.poll() is None:
            try:
                r = command.stdout.readline().decode()
                if r == '':
                    pass
                print(r)
            except KeyboardInterrupt:
                pass

    @staticmethod
    def build_image(tag=None, path='.'):
        """
            # build 用于从dockerfile处创建镜像
            :param tag: 默认None，指定标签名称
            :param path: 默认'.'
            :return: 默认返回执行结果
        """
        if isinstance(tag, str):
            if isinstance(path, str):
                command = subprocess.Popen(
                    'docker build -t {} {}'.format(tag, path), shell=True, stdout=subprocess.PIPE)
                command = command.communicate()[0].decode()
                return command
            else:
                raise DockerBuildError("path:{}类型错误".format(type(path)))
        else:
            raise DockerBuildError("tag:{}类型错误".format(type(tag)))
