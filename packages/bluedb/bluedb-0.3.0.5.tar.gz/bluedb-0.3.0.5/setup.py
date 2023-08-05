from setuptools import setup

readme = ''
with open('README.rst') as f:
    readme = f.read()

setup(
    name='bluedb',
    author='EnderDas',
    author_email='TheRealEnderDas@gmail.com',
    url='https://github.com/Enderdas/BlueDB',
    packages=['BlueDB'],
    version='0.3.0.5',
    description='Like shelves but better...',
    long_description=readme,
    long_description_content_type='text/x-rst'
)
