from setuptools import setup, find_packages

setup(
    name='ob-pipelines',
    author='Jacob Feala',
    author_email='jake@outlierbio.com',
    version='0.1',
    url='http://github.com/outlierbio/ob-pipelines',
    packages=find_packages(),
    description='Bioinformatics apps (using Docker) and workflows (using Luigi)',
    include_package_data=True,
    install_requires=[
        'boto3',
        'click',
        'luigi',
        'PyYAML'
    ],
    extras_require={
        'test': [
            'pytest'
        ]
    },
    entry_points='''
        [console_scripts]
        s3wrap=ob_pipelines.s3:s3wrap
        ob-cluster=ob_pipelines.cluster:cli
    '''
)