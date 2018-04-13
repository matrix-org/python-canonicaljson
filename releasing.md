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
* Follow instructions below to release debian packaging.

Prerequisites for debian packaging
----------------------------------

```
sudo apt-get install sbuild
sudo apt-get install ubuntu-dev-tools # for mk-sbuild
sudo sbuild-adduser $LOGNAME

newgrp sbuild
mk-sbuild stretch
```

If your kernel doesn't support `aufs`, you'll need to set `union-type=overlay`
in `/etc/schroot/chroot.d/sbuild-stretch-amd64`.

Debian release
--------------

```
# We need to build from a pristine copy of the repo (otherwise you end up with
# your whole working copy in the source tarball), so:
git clone git@github.com:matrix-org/python-canonicaljson.git -b v<ver> python-canonicaljson-clean

cd python-canonicaljson-clean
sbuild -s --arch-all -d stretch
debsign
```
