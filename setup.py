from distutils.core import setup
import sys
setup(
    name='s3put',
    description='Scp style Amazon S3 backup tool.',
    author='Andrei Antoukh',
    author_email='niwi@niwi.be',
    url='https://github.com/niwibe/py-s3put',
    version='0.1',
    license='BSD',
    scripts=['s3put.py'],
    install_requires=['boto'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX',
    ],
)
