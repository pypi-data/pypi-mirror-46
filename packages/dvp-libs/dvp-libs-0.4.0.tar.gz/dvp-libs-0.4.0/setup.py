import setuptools

PYTHON_SRC = 'src/main/python'

install_requires = [
  "dvp-common == 0.4.0",
  "protobuf ==3.6.1",
]

setuptools.setup(name='dvp-libs',
                 version='0.4.0',
                 install_requires=install_requires,
                 package_dir={'': PYTHON_SRC},
                 packages=setuptools.find_packages(PYTHON_SRC),
)
