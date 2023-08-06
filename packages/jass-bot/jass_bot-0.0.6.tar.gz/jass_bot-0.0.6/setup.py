import setuptools

setuptools.setup(
    name='jass_bot',
    version='0.0.6',
    install_requires=['gym>=0.10.8', 'gym-jass>=0.1.16', 'schieber>=0.1.8'],
    author="Joel Niklaus",
    author_email="me@joelniklaus.ch",
    description="An AI for the Schieber variant of the Swiss card game Jassen",
    license=open('LICENSE', "r").read(),
    long_description=open('README.md', "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JoelNiklaus/JassBot",
    packages=setuptools.find_packages(exclude=('jass_bot.rl.log', 'jass_bot.cfr.tests', 'jass_bot.mcts.tests', 'jass_bot.rl.tests')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
