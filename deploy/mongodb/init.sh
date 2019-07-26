#!/bin/bash
set -e
echo 'Initializing a fresh instance'
mongo <<EOF
use admin
db.adminCommand({setParameter: 1, internalQueryExecMaxBlockingSortBytes: 52428800})
use hawkeye
db.createUser({
  user:  '$ROOT_USERNAME',
  pwd:   '$ROOT_PASSWORD',
  roles: [{
    role: 'readWrite',
    db: 'hawkeye'
  }]
})
EOF