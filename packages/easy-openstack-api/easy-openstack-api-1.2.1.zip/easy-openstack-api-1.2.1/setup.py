from setuptools import setup
setup(
    name='easy-openstack-api',
    version='1.2.1',
    description='some one step openstack api',
    url='https://gitlabe1.ext.net.nokia.com/rolv/easy-openstack-api',
    author='lv yan',
    author_email='rocky.lv@nokia-sbell.com',
    packages=['easy_openstack_api'],
    keywords='openstack api',
    install_requires=['python-openstackclient', 'python-heatclient', 'python-neutronclient'],
)
