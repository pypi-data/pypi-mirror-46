# -*- coding:utf-8 -*-


class DockerInitRunError(Exception):
    """
        # 定义DockerInitRunError异常，当前主机没有docker.server。
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerRunImageError(Exception):
    """
        # 定义DockerRunImageError异常，实例化未知镜像错误。
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerRunImageTypeError(Exception):
    """
        # 定义DockerRunImageTypeError异常，实例化未知镜像错误。
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerHistoryArgsError(Exception):
    """
        # 定义DockerHistoryArgsError异常，层级树缺少参数args。
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerHistoryTypeError(Exception):
    """
        # 定义DockerHistoryTypeError异常，层级树类型错误。
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerfileError(Exception):
    """
        # 定义DockerHistoryArgsError异常，层级树缺少参数args。
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerfileLocationError(Exception):
    """
        # 定义DockerfileLocationError异常，指令集位置错误。
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerStatusError(Exception):
    """
        # 定义DockerStatusError异常，容器已启动。
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerPushError(Exception):
    """
        # 定义DockerPushError异常，容器已启动。
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerPullError(Exception):
    """
        # 定义DockerPushError异常，容器已启动。
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerNetWorkError(Exception):
    """
        # 定义DockerNetWorkError异常，错误指令。
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerPortError(Exception):
    """
        # 定义DockerPortError异常，不存在的ID或名称。
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerTagError(Exception):
    """
        # 定义DockerTagError异常，不存在的ID或名称。
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerNewNetworkError(Exception):
    """
        # 定义DockerNewNetworkError异常
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerQueryNetworkError(Exception):
    """
        # 定义DockerQueryNetworkError异常
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerRmNetworkError(Exception):
    """
        # 定义DockerRmNetworkError异常
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerConnectNetworkError(Exception):
    """
        # 定义DockerConnectNetworkError异常
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerTopError(Exception):
    """
        # 定义DockerTopError异常
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerLogsError(Exception):
    """
        # 定义DockerLogsError异常
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerCommitError(Exception):
    """
        # 定义DockerCommitError异常
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerQueryVolumeError(Exception):
    """
        # 定义DockerQueryVolumeError异常
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerRmVolumeError(Exception):
    """
        # 定义DockerRmVolumeError异常
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerCreateVolumeError(Exception):
    """
        # 定义DockerCreateVolumeError异常
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerMachineError(Exception):
    """
        # 定义DockerMachineError异常
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class DockerBuildError(Exception):
    """
        # 定义DockerBuildError异常
    """

    def __init__(self, error_info):
        super(Exception, self).__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info
