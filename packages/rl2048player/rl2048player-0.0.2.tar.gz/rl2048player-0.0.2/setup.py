import setuptools


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setuptools.setup(
    name='rl2048player',
    version='0.0.2',
    author='aar015',
    author_email='avirlincoln@gmail.com',
    description='Reinforcement Learning Agent capble of playing 2048',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/aar015/rl-2048-player',
    packages=setuptools.find_packages(),
    install_requires=[
        'imageio',
        'matplotlib',
        'numpy',
        'opencv-python'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='2048 RL'
    )
