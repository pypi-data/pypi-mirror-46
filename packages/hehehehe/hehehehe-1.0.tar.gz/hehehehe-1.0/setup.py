from distutils.core import setup

setup(
    name="hehehehe",  # 对外我们模块的名字
    version="1.0",  # 版本号
    description="这是第一个对外发布的模块",  # 描述
    author="jie lin",  # 作者
    author_email='jielin@qq.com',  # 作者邮箱
    py_modules=["hehehehe.hehe_one", "hehehehe.hehe_two"]  # 要发布的模块
)
