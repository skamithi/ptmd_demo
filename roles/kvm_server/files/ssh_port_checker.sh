#!/bin/bash
counter=0
result="ssh disabled"
if [ -z "$1" ]
then
  echo "hostname argument required. Example ssh_port_checker.sh 10.1.1.1"
  exit
fi

while [ $counter -lt 10 ]; do
  telnet_output=`echo quit | telnet $1 22 2>/dev/null | grep Connected`
  case "$telnet_output" in
    *Connected*)
      let counter=11
      result="ssh enabled"
      ;;
  esac
  let counter=counter+1
done
echo $result
