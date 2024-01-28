#!/bin/bash

# Database Connection Details
DB_HOST="your_database_host"
DB_NAME="your_database_name"
DB_USER="your_database_user"
DB_PASSWORD="your_database_password"

# Backup Directory
BACKUP_DIR="/path/to/backups"

# Create a timestamp for the backup file
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# Backup Command
BACKUP_COMMAND="pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME -Fc -f $BACKUP_DIR/$DB_NAME_$TIMESTAMP.dump"

# Run the backup command
$BACKUP_COMMAND

# Check if the backup was successful
if [ $? -eq 0 ]; then
  echo "Backup successful: $BACKUP_DIR/$DB_NAME_$TIMESTAMP.dump"
else
  echo "Backup failed"
fi
