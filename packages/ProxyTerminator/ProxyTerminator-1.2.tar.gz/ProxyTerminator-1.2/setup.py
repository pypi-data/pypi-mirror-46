from setuptools import setup, find_packages

setup (
    # name in the pypi, easy_install or egg name
    name="ProxyTerminator",
    version="1.2",
    keywords=["Terminator", "terminal", "network", "intranet"],
    description="network Terminator terminal",
    long_description="make your local intranet service can be directly accessed from the internet, just like teamview, but more powerful.",
    license="GPLv3",
    url="https://github.com/davify/Terminator.git",
    author="SpringVi",
    author_email="springvi@qq.com",

    # dir list to be packaged
    # packages=find_packages(),
    packages=[
        "com",
        "com.cleverworld.spring",
        "com.cleverworld.spring.terminator",
        "com.cleverworld.spring.terminator.conf"
    ],

    include_package_data=True,
    package_data = {'': ['*.yaml']},
    platforms="3.7",

    # depend on libraries
    install_requires=[
        "PyYAML>=3.13"
    ],
    scripts=[],

    # entry point definition
    entry_points={
        "console_scripts":[
            "Terminator=com.cleverworld.spring.Terminator:main"
        ]
    },
    # py_modules=["Terminator.py", "Utils.py", "BusinessConnector.py", "CommandExecutor.py"],
    # py_modules=["com/cleverworld/spring/Terminator.py", "com/cleverworld/spring/terminator/Utils.py", "com/cleverworld/spring/terminator/BusinessConnector.py", "com/cleverworld/spring/terminator/CommandExecutor.py"],
    py_modules=["com/cleverworld/spring/", "com/cleverworld/spring/terminator"],

    classifiers=[
        "Development Status :: 6 - Mature",
        # "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
        "Topic :: Internet :: Proxy Servers",
        'Programming Language :: Python :: Implementation :: CPython',
        "License :: OSI Approved :: GNU General Public License (GPL)"
    ],

    zip_safe=False

)

'''
--see also：https://stackoverflow.com/questions/9185307/setup-py-and-installing-a-python-project
usage:
1, build
python setup.py build
2, install
python setup.py install
or
python setup.py install --user
3, run test in windows
Terminator
4，run in linux server
nohup Terminator > tmp 2>&1 &

1、generate gzip package
    setup.py sdist
    
2、generate binary windows installer or linux rpm file
    setup.py bdist --format=wininst
    setup.py bdist --format=rpm
'''