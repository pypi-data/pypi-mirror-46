#!/usr/bin/env python
from setuptools import setup, find_packages


name = "promql" # TODO give me a name

#subprocess.check_call("touch {}.py".format(name), shell=True)

kwargs = {"name": name}
kwargs["version"] = "0.0.1"
kwargs["long_description"] = "Coming Soon"

#kwargs["py_modules"] = [name]

setup(
    description=kwargs["long_description"],
    keywords="",
    author='Jay Marcyes',
    author_email='jay@marcyes.com',
    url='http://github.com/Jaymon/{}'.format(name),
    #py_modules=[name], # files
    #packages=find_packages(), # folders
    license="MIT",
    #install_requires=install_modules,
    #tests_require=tests_modules,
    #extras_require={"extra_name": []},
    classifiers=[ # https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
#     entry_points = {
#         'console_scripts': [
#             '{} = {}:console'.format(name, name),
#         ],
#     }
    **kwargs
)

