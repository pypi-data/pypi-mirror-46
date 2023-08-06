from setuptools import setup, Command

def readme():
    with open('README.rst') as f:
        return f.read()


class Test_cmd(Command):
    # user_options, initialize_options, finalize_options must be created
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    # run is the function the will be run after following command:
    # python3 setup.py test_cmd
    def run(self):
        print("this is just a test for command line")


setup(
    name='funniest_test1985',
    version='0.1',
    description='The funniest joke in the world for learning',
    long_description=readme(),
    url='https://github.com/gegham85/funniest_python_package',
    author='Gegham Movses',
    author_email='gegham.movses@gmail.com',
    license='MIT',
    packages=['funniest'],
    install_requires=['markdown'],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    cmdclass={
        'test_cmd': Test_cmd,
    },
    zip_safe=False
)
