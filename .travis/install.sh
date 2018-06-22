#!/bin/bash

set -xe

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # osx build uses a 'generic' language which doesn't come with pip
    case "${TOXENV}" in
        py27)
            # for py27, use the system python
            sudo `dirname $0`/get-pip.py
            sudo pip install tox
            ;;
        py36)
            # for py36, use homebrew python, which comes with pip.
            # see also https://docs.brew.sh/Homebrew-and-Python
            brew upgrade python
            pip3 install tox
            ;;
        *)
            echo "TOXENV ${TOXENV} not supported on osx" >&2
            exit 1
            ;;
    esac
else
    pip install tox
fi
