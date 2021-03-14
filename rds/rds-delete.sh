#!/bin/bash -eux

aws rds delete-db-instance \
    --db-instance-identifier ${PG_INSTANCE} \
    --skip-final-snapshot \
    --delete-automated-backups