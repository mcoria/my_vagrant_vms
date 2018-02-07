#!/bin/sh
# Create Central Inventory
output=`id`
UserID=`echo $output | cut -f1 -d ' ' | cut -f2 -d '=' | cut -f1 -d '('`
if [ "$UserID" != "0" ]; then
   echo "This script must be executed as root" 
   exit 1 
fi
INV=/u01/oraInventory
GRP=vagrant
INVPTRDIR=/etc

echo "Setting the inventory to $INV"
echo "Setting the group name to $GRP"

if [ -d $INVPTRDIR ]; then
chmod 755 $INVPTRDIR;
else
mkdir -p $INVPTRDIR;
fi

INVPTR=${INVPTRDIR}/oraInst.loc
INVLOC=$INV

PTRDIR="`dirname $INVPTR`";

# Create the software inventory location pointer file
if [ ! -d "$PTRDIR" ]; then
 mkdir -p $PTRDIR;
fi
echo "Creating the Oracle inventory pointer file ($INVPTR)";
echo    inventory_loc=$INVLOC > $INVPTR
echo    inst_group=$GRP >> $INVPTR
chmod 644 $INVPTR

# Create the inventory directory if it doesn't exist
if [ ! -d "$INVLOC" ];then
 echo "Creating the Oracle inventory directory ($INVLOC)";
 mkdir -p $INVLOC;
fi

echo "Changing permissions of $INV to 770.";
chmod -R g+rw,o-rwx $INV;
if [ $? != 0 ]; then
 echo "OUI-35086:WARNING: chmod of $INV to 770 failed!";
fi

echo "Changing groupname of $INV to $GRP.";
chgrp -R $GRP $INV;
if [ $? != 0 ]; then
 echo "OUI-10057:WARNING: chgrp of $INV to $GRP failed!";
fi
echo "The execution of the script is complete"
