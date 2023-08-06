import setuptools

setuptools.setup(
    name="digit_recognition",
    version="0.0.6",
    py_modules=['nn_functions', 'install_network', 'digit_recognition'],
    package_dir={'': 'src'},
    author="Maximilian Mittenbuhler",
    author_email="max.mittenbuhler@student.uva.nl",
    description="Neural network for digit recognition",
    url="https://github.com/Mittenbuhler/Neural_Network.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)