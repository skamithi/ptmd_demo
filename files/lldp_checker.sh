#!/bin/bash

# script for checking if kvm host has seen lldp from all vms
counter=0
result="lldp failed. run lldpctl manually to see what is going on"

while [ $counter -lt 20 ]; do
  lldp_output=`lldpctl -f xml | fgrep -c '</interface>'`
  echo "current count of lldp neighbors $lldp_output"
  if (( $lldp_output > 11 ))
  then
      let counter=100
      result="lldp works on all vms"
  else
    let counter=counter+1
    echo "sleep for 5 seconds"
    sleep 5
  fi
done

echo "$result"

if [[ "$result" =~ "works" ]]
then
  exit 0
fi

exit -1

