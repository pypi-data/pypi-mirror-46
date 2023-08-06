from setuptools import setup, find_packages

setup(
    name='kafka-utils-netease',
    version='1.2',
    packages=find_packages(),
    author='liuweidong',
    author_email='discoheaven@163.com',
    description='Easy way to use Kafka in python',
    install_requires=['confluent-kafka',
                      'gevent']
)
