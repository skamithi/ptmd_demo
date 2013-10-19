#!/bin/bash

# Script for checking if SSH port is open
# Only checks that port is open. Not that actually SSH connection can occur
counter=0
result="ssh disabled"

if [ -z "$1" ]
then
  echo "hostname argument required. Example ssh_port_checker.sh 10.1.1.1"
  exit
fi

while [ $counter -lt 20 ]; do
  echo "check ssh port connection for $1"
  telnet_output=`echo quit | telnet $1 22 2>/dev/null | grep Connected`
  case "$telnet_output" in
    *Connected*)
      let counter=100
      result="ssh enabled"
      ;;
  esac
  let counter=counter+1
  echo "sleep for 5 seconds"
  sleep 5
done

echo "$result on $1"

if [[ "$result" =~ "enabled" ]]
then
  exit 0
fi

exit -1

