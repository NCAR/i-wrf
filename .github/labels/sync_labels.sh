#!/bin/bash

# Must specify 4 arguments:
#   - username
#   - authorization key

if [[ $# -ne 2 ]]; then
  echo "ERROR: `basename $0` ... must specify the GitHub username and authorization key"
  exit 1
else
  user=$1
  auth=$2
  repo=NCAR/i-wrf
  labels="`dirname $0`/labels.txt"
fi

# GitHub label URL
URL="https://api.github.com/repos/${repo}/labels"

# Output command file
CMD_FILE="`dirname $0`/sync_labels_commands.sh"
echo "#!/bin/sh -v" > ${CMD_FILE}

# Get the current repo labels
SCRIPT_DIR=`dirname $0`
TMP_FILE="labels.tmp"
CMD="${SCRIPT_DIR}/pull_labels.sh ${user} ${auth}"
echo "CALLING: ${CMD}"
${CMD} > ${TMP_FILE}

# Add new or update existing labels
while read -r line; do

  # Parse the label name
  name=`echo $line | sed -r 's/,/\n/g' | grep '"name":' | cut -d':' -f2-10 | cut -d'"' -f2`

  # Skip empty names
  if [[ ${#name} -eq 0 ]]; then
    continue
  fi

  # Check for existing label
  exists=`egrep -i "\"${name}\"" ${TMP_FILE} | wc -l`

  # POST a new label
  if [[ $exists -eq 0 ]]; then
    echo "[POST] ${repo} label ... ${name}"
    echo "curl -u \"${user}:${auth}\" -X POST \
          -H \"Accept: application/vnd.github.v3+json\" \
          -d '${line}' '${URL}'" >> ${CMD_FILE}
  # PATCH an existing label
  else
    old_name=`egrep -i "\"${name}\"" ${TMP_FILE} | sed -r 's/,/\n/g' | grep '"name":' | cut -d':' -f2-10 | cut -d'"' -f2 | sed -r 's/ /%20/g'`
    echo "[PATCH] ${repo} label ... ${old_name} -> ${name}"
    echo "curl -u \"${user}:${auth}\" -X PATCH \
          -H \"Accept: application/vnd.github.v3+json\" \
          -d '${line}' '${URL}/${old_name}'" >> ${CMD_FILE}
  fi

done < $labels

# Delete labels
while read -r line; do

  # Parse the label name
  name=`echo $line | sed -r 's/,/\n/g' | grep '"name":' | cut -d':' -f2-10 | cut -d'"' -f2`

  # Skip empty names
  if [[ ${#name} -eq 0 ]]; then
    continue
  fi

  # Check for existing label
  exists=`egrep -i "\"${name}\"" $labels | wc -l`

  # DELETE missing label
  if [[ $exists -eq 0 ]]; then
    echo "[DELETE] ${repo} label ... ${name}"
    DELETE_URL="${URL}/`echo ${name} | sed -r 's/ /%20/g'`"
    echo "curl -u \"${user}:${auth}\" -X DELETE \
          -H \"Accept: application/vnd.github.v3+json\" \
          '${DELETE_URL}'" >> ${CMD_FILE}
  fi

done < $TMP_FILE

# Cleanup
rm -f ${TMP_FILE}

# Make the run command file executable
chmod +x ${CMD_FILE}
echo "To make these changes, execute the run command file:"
echo "${CMD_FILE}"

