from distutils.core import setup

setup(
    name = 'SuperC',    # 对外模块的名称
    version = '1.0',    # 版本号
    description = '这是一个对外发布的模块，用于测试',   # 描述
    author = 'AlexLu',  # 作者
    author_email = '275542223@qq.com',  # 作者邮箱
    py_modules = ['SuperC.demo_1','SuperC.demo_2']  # 要发布的模块
)