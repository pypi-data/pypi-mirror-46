#### Packageinfo
- This package contains common util functions & classessfor the following sections
1. Http Util
2. WebScraping utils for selenium, bs4
3. Matplotlib utils
4. Pillow, numpy utils
5. Pandas util


For more info, please checkout the repo to see examples
[balautil](http://github.com/balaprasanna/balautil)

## How to setup your own package
pip install --user --upgrade setuptools wheel

python setup.py sdist bdist_wheel
pip install --user --upgrade twine

twine upload dist/* --verbose
