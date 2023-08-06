import setuptools

setuptools.setup(
    name="digit_recognition",
    version="0.0.7",
    py_modules=['digit_recognition'],
    #package_dir={'': 'src'},
    author="Maximilian Mittenbuhler",
    author_email="max.mittenbuhler@student.uva.nl",
    description="Neural network for digit recognition",
    url="https://github.com/Mittenbuhler/Neural_Network.git",
    install_requires=['numpy', 'idx2numpy', 'urllib3', 'Pillow', ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'digit_recognition = digit_recognition:run_gui'
        ]
    },
)

# 'numpy', 'urllib3', , 'PIL', 'idx2numpy'