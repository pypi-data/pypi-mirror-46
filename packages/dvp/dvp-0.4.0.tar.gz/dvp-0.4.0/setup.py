import setuptools

PYTHON_SRC = 'src/main/python'

install_requires = [
  "dvp-common == 0.4.0",
  "dvp-libs == 0.4.0",
  "dvp-platform == 0.4.0",
  "dvp-tools == 0.4.0",
]

setuptools.setup(name='dvp',
                 version='0.4.0',
                 install_requires=install_requires,
                 package_dir={'': PYTHON_SRC},
                 packages=setuptools.find_packages(PYTHON_SRC),
)
