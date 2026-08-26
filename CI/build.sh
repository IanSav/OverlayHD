#!/bin/sh

# Script by Persian Prince for https://github.com/OpenVisionE2
# You're not allowed to remove my copyright or reuse this script without putting this header.

setup_git() {
  git config --global user.email "bot@oe-alliance.com"
  git config --global user.name "oe-alliance python bot"
  return 0
}

commit_files() {
  git clean -fd
  rm -rf *.pyc
  rm -rf *.pyo
  rm -rf *.mo
  git checkout master
  ./CI/chmod.sh
  ./CI/dos2unix.sh
  ./CI/PEP8.sh
  ./CI/PO.sh
  return 0
}

upload_files() {
  git remote add upstream https://${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git > /dev/null 2>&1
  git push --quiet upstream master || echo "failed to push with error $?" >&2
  return 0
}

setup_git
commit_files
upload_files
