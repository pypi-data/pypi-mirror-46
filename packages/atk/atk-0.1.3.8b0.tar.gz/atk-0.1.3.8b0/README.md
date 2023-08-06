<h1 align='center'>🐍atk🐋</h1>

<br>

<p align="center">
    <a href="https://pypi.org/project/havedocker/">
        <img src="https://img.shields.io/pypi/v/havedocker.svg?color=blue" alt="PYPI">
    </a>
     <a href="https://pypi.org/project/havedocker/">
        <img src="https://img.shields.io/pypi/pyversions/havedocker.svg?color=red" alt="Contributions welcome">
    </a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-brightgreen.svg" alt="License">
    </a>
    <a href="https://chocolatey.org/">
        <img src="https://img.shields.io/badge/ChocoLatey-0.10.11-blueviolet.svg">
    </a>
</p>

<p align="center">
	<a href="https://pypi.org/project/havedocker/">
    	<img src="https://img.shields.io/pypi/format/havedocker.svg?color=orange" alt="PYPI - Format">
    </a>
    <a href="https://www.docker.com/">
    	<img src="https://img.shields.io/badge/docker-18.09.2-ff69b4.svg">
    </a>
    <a href="https://cmder.net/">
    	<img src="https://img.shields.io/badge/ConEmu-180626-yellow.svg">
    </a>    
</p>

<br>

<p> 
	<h2 align="center">🌴(Automation)-(Terminal)-(Kubernetes)</h2>
</p>
<p>
	<h2 align="center">🎣Automate the administration of docker and kubernetes</h2>
</p>

<br>

<h3 align='center'>⚓支持 Python3.8 版本的atk，正在开发中……</h3>



<br>

> #### `Simple to install`
>
> 1. ```shell
>   pip install atk
>   ```
> ```
> 
> ```
>
> ```
> 
> ```

<br>

> #### `first step`
>
> > 实例化`Agility_Docker()`，如果您没有安装`docker`，那么将会报错。
>
> ```python
> from atk import *
> 
> docker = Agility_Docker()
> ```

<br>

> #### `Check the container`
>
> > 查询容器`query()`
> >
> > 查询镜像`query(self_object_='images')`
>
> ```python
> docker.query()
> docker.query(self_object_='images')
> ```

<br>

> #### `Run the container`
>
> > 运行容器`run()`
>
> ```python
> docker.run(docker.run(images_name='centos', vessel_name='centos1'))
> ```

<br>

> #### `Query the network card`
>
> > 查询网卡`query_network()`
>
> ```python
> docker.query_network(formatting=True)
> ```

<br>

> #### `Modify image tag（label）`
>
> > 修改镜像标签`tag()`
>
> ```python
> docker.tag(old_name='centos', new_name='centos2')
> ```

<br>

> 更多使用说明：[atk-GitHub-tutorial](https://github.com/haitanghuadeng/havedocker)
>
> 当前版本：`version-0.1.3.8b`

