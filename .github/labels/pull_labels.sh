#!/bin/sh

# Must specify 2 arguments:
#   - username
#   - authorization key

if [[ $# -ne 2 ]]; then
  echo "ERROR: `basename $0` ... must specify the GitHub username and authorization key"
  exit 1
else
  user=$1
  auth=$2
  repo=NCAR/i-wrf
fi

# Pull and format existing records for existing labels
curl -u "${user}:${auth}" -H "Accept: application/vnd.github.v3+json" \
"https://api.github.com/repos/${repo}/labels?page=1&per_page=100" | \
egrep  '"name":|"color":|"description":|{|}' | \
tr -d '\n' | sed -r 's/ +/ /g' | sed 's/}/}\n/g' | sed 's/,* {/{/g'

