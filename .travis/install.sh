#!/bin/bash

set -xe

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # osx build uses a 'generic' language which doesn't come with pip
    case "${TOXENV}" in
        py38)
            # for py38, use homebrew python, which comes with pip.
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
