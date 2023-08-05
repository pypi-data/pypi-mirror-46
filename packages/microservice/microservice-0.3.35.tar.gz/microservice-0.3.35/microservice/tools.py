#!/usr/bin/env python3
import logging
import pkgutil
import sys

import migrations
from models import Migrations

from microservice.models import connection


def migrate():
    """
    Функция для проверки и применения миграций.
    """
    logging.info("Trying migrations")
    connection.execute_sql("""
        create table if not exists migrations
        (
          id   serial       not null
            constraint migrations_pk
              primary key,
          name varchar(200) not null,
          time timestamp
        );
        
        create unique index if not exists migrations_id_uindex
          on migrations (id);
    """)
    applied_migrations = [x.name for x in Migrations.select().order_by(Migrations.name).asc()]
    last_migration = applied_migrations[-1] if len(applied_migrations) > 0 else "Database is empty"
    for loader, name, _ in pkgutil.walk_packages(migrations.__path__):
        if name not in applied_migrations:
            Migration = loader.find_module(name).load_module(name).Migration

            # separate migration
            connection.execute_sql("SET STATEMENT_TIMEOUT TO 60000;")
            with connection.atomic():
                try:
                    logging.info("Applying: {}".format(name))
                    Migration()
                except Exception as e:
                    logging.error("Failed on step: {}. "
                                  "Rolling back because of error: {}".format(name, e))
                    connection.rollback()
                    exit(1)
                else:
                    last_migration = name
                    m = Migrations(name= name)
                    m.save()

    logging.info("Last migration is: {}".format(last_migration))


if __name__ == '__main__':
    _, func, *args = sys.argv
    globals()[func](*args)
    logging.info("Done")
    # TODO: переписать с использованием argparse
