Releasing python-canonicaljson
==============================

* bump version in `canonicaljson.py`
* update changelog
* Build and upload to pypi:
  * `rm -r dist`
  * `python setup.py sdist bdist_wheel`
  * `twine upload -s dist/*`
* `git tag -s v<ver>`
* `git push`
* `git push --tags`