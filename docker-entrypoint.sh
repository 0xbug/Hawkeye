#!/bin/bash
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf&&tail -f /var/log/supervisor/*