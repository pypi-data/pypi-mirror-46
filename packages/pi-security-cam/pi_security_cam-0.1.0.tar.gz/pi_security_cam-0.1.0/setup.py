from setuptools import setup

setup(
    name='pi_security_cam',
    version='0.1.0',
    description='Security camera built for Raspberry Pi',
    url='http://github.com/tjkessler/pi-security-cam',
    author='Travis Kessler',
    author_email='travis.j.kessler@gmail.com',
    license='MIT',
    packages=['pi_security_cam'],
    install_requires=['dropbox', 'opencv-python'],
    zip_safe=False
)
