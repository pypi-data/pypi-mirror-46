from distutils.core import setup

setup(
    #对外我们模块的名字
    name="ZhuPengJunTest",
    #版本号
    version='1.0',
    #描述
    description='对外发布的模块，测试第一版',
    # 作者
    author='zhupengjun',
    #email
    author_email='zhumac@foxmail.com',
    # 要发布的模块
    py_modules=['ZhuPengJunTest.pp','ZhuPengJunTest.tt']
)