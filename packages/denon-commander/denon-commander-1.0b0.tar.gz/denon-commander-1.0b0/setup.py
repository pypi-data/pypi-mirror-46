import setuptools

setuptools.setup(
    name="denon-commander",
    version="1.0beta",
    author="Aleksander Psuj",
    author_email="xfatal1337@gmail.com",
    description="Manage your denon device from console",
    url="https://github.com/xFatal/Denon-Commander",
    install_requires=['denonavr'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['denon-commander=denoncommander:main'],
    }
)
