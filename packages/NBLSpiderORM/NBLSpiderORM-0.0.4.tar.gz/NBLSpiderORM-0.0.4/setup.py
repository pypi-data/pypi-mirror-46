from setuptools import setup,find_packages


setup(
    name='NBLSpiderORM',
    version='0.0.4',
    author='nbltrust',
    author_email='',
    url='https://www.nbltrust.com/#/cn/home',
    description=u'NBLSpiderORM',
    packages=find_packages(),
    install_requires=['configparser','pymysql','DBUtils','pandas'],
    entry_points={
        "console_scripts": ['NBLSpiderORM = DBModel:DBModel']
    }
)