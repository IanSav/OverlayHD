#!/bin/bash
# Script to generate po files outside of the normal build process
#  
# Pre-requisite:
# The following tools must be installed on your system and accessible from path
# gawk, find, xgettext, sed, python, msguniq, msgmerge, msgattrib, msgfmt, msginit
#
# Run this script from within the po folder.
#
# Author: Pr2 for OpenPLi Team, jbleyel
# Version: 2.0
#
localgsed="sed"
findoptions=""

#
# Script only run with sed but on some distro normal sed is already sed so checking it.
#
sed --version 2> /dev/null | grep -q "GNU"
if [ $? -eq 0 ]; then
	localgsed="sed"
else
	"$localgsed" --version | grep -q "GNU"
	if [ $? -eq 0 ]; then
		printf "GNU sed found: [%s]\n" $localgsed
	fi
fi

which python
if [ $? -eq 1 ]; then
	which python3
	if [ $? -eq 1 ]; then
		printf "python not found on this system, please install it first or ensure that it is in the PATH variable.\n"
		exit 1
	fi
fi

which xgettext
if [ $? -eq 1 ]; then
	printf "xgettext not found on this system, please install it first or ensure that it is in the PATH variable.\n"
	exit 1
fi


#
# On Mac OSX find option are specific
#
if [[ "$OSTYPE" == "darwin"* ]]
	then
		# Mac OSX
		printf "Script running on Mac OSX [%s]\n" "$OSTYPE"
    	findoptions=" -s -X "
        localgsed="gsed"
fi

#
# Arguments to generate the pot and po files are not retrieved from the Makefile.
# So if parameters are changed in Makefile please report the same changes in this script.
#
# Extract the plugin language domain from __init__.py or plugin.py
PLUGIN_DOMAIN=$(grep -r "PluginLanguageDomain\s*=" .. | head -1 | $localgsed "s/.*PluginLanguageDomain\s*=\s*['\"]\\([^'\"]*\\)['\"].*/\\1/")

if [ -z "$PLUGIN_DOMAIN" ]; then
	printf "Error: Could not find PluginLanguageDomain in __init__.py or plugin.py\n"
	exit 1
fi

printf "Using plugin domain: %s\n" "$PLUGIN_DOMAIN"

# Create backup of existing pot file if it exists
if [ -f "${PLUGIN_DOMAIN}.pot" ]; then
	cp "${PLUGIN_DOMAIN}.pot" "${PLUGIN_DOMAIN}.pot.bak"
	printf "Backup created: %s.pot.bak\n" "$PLUGIN_DOMAIN"
fi

printf "Getting list of languages\n"
languages=($(ls *.po 2>/dev/null | $localgsed 's/\.po$//g'))


printf "Creating temporary file %s-py.pot\n" "$PLUGIN_DOMAIN"
find $findoptions .. -name "*.py" -exec xgettext --no-wrap -L Python --from-code=UTF-8 -k_:1 --add-comments="TRANSLATORS:" -d "$PLUGIN_DOMAIN" --package-name="$PLUGIN_DOMAIN" -s -o ${PLUGIN_DOMAIN}-py.pot {} \+
$localgsed --in-place ${PLUGIN_DOMAIN}-py.pot --expression=s/CHARSET/UTF-8/

printf "Creating temporary file %s-xml.pot\n" "$PLUGIN_DOMAIN"
which python
if [ $? -eq 0 ]; then
	find $findoptions .. -name "*.xml" -exec python xml2po.py {} \+ > ${PLUGIN_DOMAIN}-xml.pot
else
	find $findoptions .. -name "*.xml" -exec python3 xml2po.py {} \+ > ${PLUGIN_DOMAIN}-xml.pot
fi
printf "Merging pot files to create: %s.pot\n" "$PLUGIN_DOMAIN"
cat ${PLUGIN_DOMAIN}-py.pot ${PLUGIN_DOMAIN}-xml.pot | msguniq -s --no-wrap -o ${PLUGIN_DOMAIN}.pot -
printf "remove temp pot files\n"
rm ${PLUGIN_DOMAIN}-py.pot ${PLUGIN_DOMAIN}-xml.pot

# Check if only POT-Creation-Date changed
if [ -f "${PLUGIN_DOMAIN}.pot.bak" ]; then
	# Remove POT-Creation-Date lines and compare
	grep -v "^\"POT-Creation-Date:" "${PLUGIN_DOMAIN}.pot" > "${PLUGIN_DOMAIN}.pot.tmp1"
	grep -v "^\"POT-Creation-Date:" "${PLUGIN_DOMAIN}.pot.bak" > "${PLUGIN_DOMAIN}.pot.tmp2"
	
	if diff -q "${PLUGIN_DOMAIN}.pot.tmp1" "${PLUGIN_DOMAIN}.pot.tmp2" > /dev/null; then
		printf "No content changes detected (only POT-Creation-Date changed), restoring backup\n"
		mv "${PLUGIN_DOMAIN}.pot.bak" "${PLUGIN_DOMAIN}.pot"
	else
		printf "Content changes detected, keeping new pot file\n"
		rm "${PLUGIN_DOMAIN}.pot.bak"

		for lang in "${languages[@]}" ; do
			if [ -f $lang.po ]; then 
				printf "Updating existing translation file %s.po\n" $lang
				msgmerge --backup=none --no-wrap -s -U $lang.po ${PLUGIN_DOMAIN}.pot && touch $lang.po
				msgattrib --no-wrap --no-obsolete $lang.po -o $lang.po
			else
				printf "New file created: %s, please add it to github before commit\n" $lang.po
				msginit -l $lang.po -o $lang.po -i ${PLUGIN_DOMAIN}.pot --no-translator
			fi
		done

	fi
	
	# Clean up temp files
	rm -f "${PLUGIN_DOMAIN}.pot.tmp1" "${PLUGIN_DOMAIN}.pot.tmp2"
fi

printf "pot update from script finished!\n"
