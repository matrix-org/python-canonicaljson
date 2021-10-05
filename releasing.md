Releasing python-canonicaljson
==============================

* bump version in `canonicaljson.py`
* update changelog
* update debian changelog:
  * Add new entry: `dch -v <ver>`
  * Mark as released: `dch --distribution stable -r`
* Build and upload to pypi:
  * `rm -r dist`
  * `python setup.py sdist bdist_wheel`
  * `twine upload -s dist/*`
* `git tag -s v<ver>`
* `git push`
* `git push --tags`