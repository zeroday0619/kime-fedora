#!/bin/sh

set -e
set -x

export VERSION=2.5.6

if [[ ! -r "src/kime-v$VERSION.tar.gz" ]]; then
    echo "Download kime-v$VERSION.tar.gz"
    wget https://github.com/Riey/kime/archive/refs/tags/v$VERSION.tar.gz
    mv v$VERSION.tar.gz src/kime-v$VERSION.tar.gz
fi

cd src
fedpkg --release f36 mockbuild --enable-network
