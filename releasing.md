Releasing python-canonicaljson to pypi
======================================

* bump version in __canonicaljson.py__
* update changelog
* ``rm -r dist``
* ``python setup.py sdist bdist_wheel``
* ``twine upload -s dist/*``
* ``git tag -s v<ver>``
* ``git push --tags``
