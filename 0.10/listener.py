#!/usr/bin/python

###############################################################
# Telegraf and kapacitor must be started only after InfluxDb 
# starts listening on the HTTP port. This listeners listens 
# for events and starts the telegraf group at appropriate time
#
# This is a listener, which listens for PROCESS_LOG events
# based on communication via a subprocess stdin and 
# @see http://supervisord.org/events.html
###############################################################

import sys, re
from supervisor.childutils import listener
from supervisor.events import notify as notifyEvent
from subprocess import call

def main():
    # Telegraf needs to start after the influxdb instance starts listening
    # otherwise telegraf is not able to connect to the database
    while True:
        headers, body = listener.wait(sys.stdin, sys.stdout)
        # 'Listening for signals' is logged once the db server starts listening
        # @see cmd/influxd/main.go
        if re.search(r'Listening for signals', body):
            call(["supervisorctl", "start", "telegraf"])
            call(["supervisorctl", "start", "kapacitor"])
            sys.exit(0)
        else:
            listener.ok(sys.stdout)

if __name__ == '__main__':
    main()