#!/usr/bin/env bash

# This script resets the Django SQLite database, deletes migrations, 
# recreates the database, and seeds it from the 'seed/' directory.

set -e

if [ -f "./db.sqlite3" ]; then
    rm ./db.sqlite3
else
    echo "No SQLite database found to remove."
fi

if [ -f "./deleteMigrations.sh" ]; then
    sh ./deleteMigrations.sh
else
    echo "deleteMigrations.sh script not found."
    exit 1
fi

python manage.py makemigrations
python manage.py migrate

fixtures=$(ls seed/)
while IFS= read -r fixture; do
    echo -n "Seeding "
    echo $fixture
    python manage.py loaddata seed/$fixture
done <<< "$fixtures"