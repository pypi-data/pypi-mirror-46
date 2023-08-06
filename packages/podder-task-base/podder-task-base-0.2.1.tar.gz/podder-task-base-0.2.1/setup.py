from setuptools import setup, find_packages

install_requires = ['grpcio-tools==1.18.0',
                    'googleapis-common-protos==1.5.6',
                    'python-daemon==2.2.0',
                    'mysqlclient==1.4.1',
                    'SQLAlchemy==1.2.17',
                    'python-dotenv==0.10.1',
                    'click==6.7',
                    'jinja2==2.10',
                    'PyYAML==5.1',
                    'pytest==4.3.1',
                    'requests==2.21.0']

setup(
    name='podder-task-base',
    version='0.2.1',
    packages=find_packages(),
    author="podder-ai",
    url='https://github.com/podder-ai/podder-task-base',
    include_package_data=True,
    install_requires=install_requires,
    package_data = {
        'podder_task_base': [
            'task_initializer/templates/*',
            'task_initializer/templates/api/*',
            'task_initializer/templates/api/protos/*',
            'task_initializer/templates/scripts/*',
        ],
    },
)
