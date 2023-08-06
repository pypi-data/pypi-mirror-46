# setup.py
from distutils.core import setup

setup(name='foodAdvicer',
	version='1.2',
	author='Patryk Ekiert',
	license='MIT',
	author_email='patryk.ekiert@outlook.com',
	url='https://git.e-science.pl/pwr226110/6_libPython',
	packages=['foodAdvicer', 'foodAdvicer.Items', 'foodAdvicer.ItemsDatabase', 'foodAdvicer.Results', 'foodAdvicer.tests']
)