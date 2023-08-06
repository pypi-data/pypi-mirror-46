
### Python支持版本：
支持python3.5及以上版本

### 环境初始化：
安装setuptools：
```bash
sudo pip3 install setuptools
sudo pip3 install twine
```

创建虚拟环境
```bash
sh create-venv.sh
. venv/bin/activate
pip install -r requirements.txt
```

### 设置PyPi用户信息
编辑`~/.pypirc
```ini
[distutils]
index-servers=pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = pypi-user
```
这里pypi-user为在https://pypi.org注册的用户名，密码在后续上传中会用到。

### 执行编译上传脚本
```bash
sh release.sh
```

### 分布流程说明

#### 打包
```bash
python setup.py sdist build
```

#### 上传
```bash
twine upload dist/*
```
过程中需要输入密码，即在https://pypi.org注册时输入的密码

### 使用
请取种子工程https://gitee.com/qcc100/py-server-seed

或者自建工程引入该库：
```bash
pip install tweb-sdk
```


