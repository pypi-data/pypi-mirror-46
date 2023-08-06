from distutils.core import setup

setup(
    name='Vizer',
    version='0.1.0',
    author='lufficc',
    author_email='luffy.lcc@gmail.com',
    packages=['vizer'],
    url='https://github.com/lufficc/Vizer',
    scripts=[],
    description='Boxes and masks visualization tools.',
    install_requires=[
        "cv2",
        "numpy",
        "PIL",
    ],
)
