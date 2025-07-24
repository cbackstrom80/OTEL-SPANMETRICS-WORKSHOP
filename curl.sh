#!/bin/bash

# URL to curl
URL="http://0.0.0.0:89"

# Number of times to loop (set to infinite with `while true`)
LOOPS=10000

# Interval between requests (in seconds)
SLEEP_DURATION=1

for ((i=1; i<=LOOPS; i++))
do
  echo "Request #$i..."
  curl -s -w "\nHTTP Status: %{http_code}\n" "$URL"
  echo "Sleeping for $SLEEP_DURATION seconds..."
  sleep $SLEEP_DURATION
done
