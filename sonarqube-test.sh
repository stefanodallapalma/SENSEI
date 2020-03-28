#!bin/bash

status=$(curl -s http://127.0.0.1:9000/api/system/status | jq -r '.status')

if [ $status = 'UP' ] 
then
   exit 0
else
   exit 1
fi
exit;
