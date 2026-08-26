#!/bin/sh
echo ""

pushd $(dirname "$0")/../po
./updatepot.sh
popd

git add -u
git add *
git commit -m "PO/POT update"

echo "PO Update Done!"
echo ""
