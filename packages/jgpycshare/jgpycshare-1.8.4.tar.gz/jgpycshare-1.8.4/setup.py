# -*- coding: utf-8 -*-
"""
    author: jiege
    url: http://jieguone.top
    copyright: © jieguone.top
    license: none
    date : 2019/4/3 23:22
    ide : PyCharm
"""
from setuptools import setup, find_packages

# setup(
#     name="jgpycshare",
#     version=1.1,
#     author="jiegemena",
#     author_email="jiegemena@outlook.com",
#     description="cshare lib",
#     keywords="cshare",
#     packages=find_packages(),
#     # entry_points={
#     #     'console_scripts': [
#     #         "say_hello=nxdictionary.script.update_db_files:console_print_hello",
#     #         "say_hello=nxdictionary.script.update_db_files:ndx_up",
#     #     ]
#     # },
#     # test_suite="nxdictionary.test",  # 指定测试包位置， python setup.py test
#     # setup_requires="" 指定安装的依赖，同样可以使用pip freeze > requirements.txt 生成依赖
#     dependency_links=[],  # 添加依赖链接
#     install_requires=[
#         # 'enum34;python_version<"3.4"',
#         # 'pywin32 >= 1.0;platform_system=="Windows"', 可基于不同平台指定依赖
#     ]
# )

setup(name="jgpycshare",
      description="jgpycshare",
      version="1.8.4",
      author="jiegemena",
      author_email="jiegemena@outlook.com",
      packages=find_packages(),
      install_requires=[    # 依赖列表
          'pycryptodome>=3.8.1',
          'requests'
      ]
      )
