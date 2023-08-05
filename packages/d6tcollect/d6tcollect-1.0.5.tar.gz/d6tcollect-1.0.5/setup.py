from setuptools import setup

setup(
    name='d6tcollect',
    version='1.0.5',
    packages=['d6tcollect'],
    url='https://github.com/d6t/d6tcollect',
    license='MIT',
    author='DataBolt Team',
    author_email='support@databolt.tech',
    description='d6tcollect: collects anonymous usage statistics for python libraries',
    long_description='Much like websites, this library collects anonymous usage statistics.'
        'It ONLY collects import and function call events. It does NOT collect any of your data.'
        'For details see https://github.com/d6t/d6tcollect'
        "For privacy notice see https://www.databolt.tech/index-terms.html#privacy",
    install_requires=[
    ],
    include_package_data=True,
    python_requires='>=3.5',
    keywords=['d6tcollect', 'ingest csv'],
    classifiers=[]
)
