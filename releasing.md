Releasing python-canonicaljson
==============================

* bump version in `src/canonicaljson/__init__.py`
* update changelog
* Build and upload to pypi:
  * `rm -r ./**/*.egg-info`
  * `rm -r dist`
  * `python -m build`
  * `twine upload -s dist/*`
* `git tag -s v<ver>`
* `git push`
* `git push --tags`