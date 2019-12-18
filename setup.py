from setuptools import setup

setup(
    name='Choose activity',
    version='1.0',
    description='Choose a random activity to do from a list',
    author='Jacopo Farina',
    python_requires='>=3.7', # it uses dataclasses
    install_requires=[],  # yep, nothing
    # dependency only for tests, yet to investigate the best practice
    extras_require={
        'dev': [
            'pytest>=5',
            'pytest-cov>=2.8.1'
            ]
        },
    packages=['choose_activity'],
    entry_points={
        'console_scripts': [
            'choose_activity = choose_activity.__main__:main'
        ]
    },
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        ],
    )
