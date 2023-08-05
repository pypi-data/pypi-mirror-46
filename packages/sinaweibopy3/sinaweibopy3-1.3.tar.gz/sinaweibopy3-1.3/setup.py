from distutils.core import setup
import weibo

kw = dict(
    name='sinaweibopy3',
    version=weibo.__version__,
    description='Sina Weibo OAuth 2 API Python SDK',
    long_description=open('README', 'r').read(),
    py_modules=['weibo'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])

setup(**kw)
