import setuptools

setuptools.setup(
    name='ByRequests',
    packages=['ByRequests'],  # this must be the same as the name above
    version='1.2.0',
    description='Helper to use proxy services with Requests',
    author='Kevin B. Garcia Alonso',
    author_email='kevangy@hotmail.com',
    url='https://github.com/ByPrice/ByRequests',  # use the URL to the github repo
    download_url='https://github.com/ByPrice/ByRequests/',
    keywords=['requests', 'request', 'proxy', 'proxies', 'beautifulsoap', 'xpath', 'GET', 'POST'],
    install_requires=[
        'beautifulsoup4>=4.6.0',
        'bs4>=0.0.1',
        'requests>=2.18.0',
        'urllib3>=1.21.1',
        'fake-useragent==0.1.11',
        'lxml==4.2.5',
        'eventlet==0.23.0'
    ],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ),
)
