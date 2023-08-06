from setuptools import setup

setup(
    # Metadata
    name='algo-base',
    version='0.0.5',
    author='Contributors',
    author_email='mli@amazon.com',
    url='https://www.baidu.com',
    description='组件开发基础工具',
    long_description='组件开发基础工具',
    license='Apache-2.0',
    platforms=["all"],
    # Package info
    packages=['base'],
    install_requires=['pandas>0.24.0'],
    zip_safe=True,
)
