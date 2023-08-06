# coding=utf8
import os

CONFIG_CONTENT = """
[distutils]
index-servers =
    pypi

[pypi]
username:{username}
password:{password}
"""


# 配置 pypi 用户名

# $HOME/.pypirc

# pyc show
# pyc pypi -u kinegratii -p xxx

def config_pypi_account(username, password):
    with open(os.path.expanduser('~/.pypirc'), 'w+') as fp:
        fp.write(CONFIG_CONTENT.format(
            username=username,
            password=password
        ))
