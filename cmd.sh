#!/bin/bash
set -e

if [ "$ENV" = 'DEV' ]; then
	echo "Running Dev Server"
	exec python "identidock.py"
else
	echo "Running Production Server"
	exec uswgi --http 0.0.0.0:9090 --wsgi-file /app/identidock.py --callable app --stats 0.0.0.0:9191
fi
