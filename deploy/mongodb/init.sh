#!/bin/bash
set -e
echo 'Initializing a fresh instance'
mongo <<EOF
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