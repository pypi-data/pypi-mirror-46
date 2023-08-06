# jucie-python-sdk

#### 项目介绍
果汁云IOT的Python SDK
[https://gitee.com/haonan108/juice-cloud](https://gitee.com/haonan108/juice-cloud)


#### 软件架构
软件架构说明


#### 安装教程

1. python setup.py bdist_egg
2. 将包拷贝至目的机器，然后执行 python setup.py install
3. 即可import juice

安装pip
$ wget https://bootstrap.pypa.io/get-pip.py
$ python get-pip.py
$ pip -V　　#查看pip版本

上传到pypi
1.vi ~/.pypirc
  [distutils]
  index-servers =
       pypi

  [pypi]
  repository: https://upload.pypi.org/legacy/
  username: your_username
  password: your_password

2.打包上传
  python setup.py check
  python setup.py sdist
  python setup.py sdist upload -r pypi
  
3.安装
  pip install guozhi

4.查看安装版本
  pip freeze | grep guozhi
