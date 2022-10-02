#!/bin/sh

echo ""
echo "Create / Update language files"
echo ""
echo "Changing language files, please wait ..." 
begin=$(date +"%s")

pushd ./po &> /dev/null
./updatepot.sh
popd &> /dev/null
git add -u
git add *
git commit -m "Update POT and PO files"

echo ""
finish=$(date +"%s")
timediff=$(($finish-$begin))
echo -e "Change time was $(($timediff / 60)) minutes and $(($timediff % 60)) seconds."
echo -e "Fast changing would be less than 5 minutes."
echo ""
echo "language Done!"
echo ""
