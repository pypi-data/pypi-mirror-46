import setuptools

PYTHON_SRC = 'src/main/python'

install_requires = [
  "click >= 7.0",
  "enum34 >= 1.1.6",
  "jinja2 >= 2.10",
  "jsonschema >= 3",
  "protobuf == 3.6.1",
  "pyyaml >= 3",
  "requests >= 2.21.0",
  "typing;python_version < '3.5'",
]

setuptools.setup(name='dvp-tools',
                 version='0.4.0',
                 install_requires=install_requires,
                 package_dir={'': PYTHON_SRC},
                 packages=setuptools.find_packages(PYTHON_SRC),
)
