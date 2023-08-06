from distutils.core import setup

setup(
    name='ybc_qrcode',
    version='1.0.4',
    description='generate a qrcode',
    long_description='generate a qrcode according input text',
    author='mengxf',
    author_email='mengxf01@fenbi.com',
    keywords=['pip3', 'qrcode', 'python3', 'python'],
    url='http://pip.zhenguanyu.com/',
    packages=['ybc_qrcode'],
    package_data={'ybc_qrcode': ['*.py']},
    license='MIT',
    install_requires=[
        'qrcode',
        'ybc_exception'
    ],
)
