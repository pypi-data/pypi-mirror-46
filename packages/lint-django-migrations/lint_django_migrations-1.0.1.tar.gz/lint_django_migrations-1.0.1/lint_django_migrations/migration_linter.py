from __future__ import print_function

import hashlib
import logging
import os

from django.core.management import call_command

from .sql_analyser import analyse_sql_statements
from .state import State
from .utils import get_migration_abspath
from django.db.migrations.loader import MigrationLoader

logger = logging.getLogger(__name__)

DJANGO_APPS_WITH_MIGRATIONS = ("admin", "auth", "contenttypes", "sessions")


class MigrationLinter:
    state_path = ".migration_state"

    def __init__(self, include_apps=None, interactive=False, force_update=False, check_only=False):
        self.state = State(self.state_path)
        self.state.load()
        self.interactive = interactive
        self.force_update = force_update
        self.check_only = check_only
        self.include_apps = include_apps

    def lint_all_migrations(self):
        migrations = self._gather_all_migrations()

        # Lint those migrations
        sorted_migrations = sorted(
            migrations, key=lambda migration: (migration.app_label, migration.name)
        )
        for m in sorted_migrations:
            if self.include_apps and m.app_label in self.include_apps:
                continue

            success = self.lint_migration(m)
            if not success:
                return False

        self.state.save()
        return True

    def lint_migration(self, migration):
        app_label = migration.app_label
        migration_name = migration.name

        migration_hash = self.get_migration_hash(app_label, migration_name)

        if (
            migration_name in self.state[app_label]
            and self.state[app_label][migration_name]["migration_hash"]
            == migration_hash
        ):
            return True

        print("({0}, {1})... ".format(app_label, migration_name), end="")
        try:
            sql_statements = self.get_sql(app_label, migration_name)
        except Exception as e:
            errors = [
                {
                    "err_msg": str(e),
                    "code": "SQL_RETRIEVE_ERROR",
                    "table": None,
                    "column": None,
                }
            ]
        else:
            errors = analyse_sql_statements(sql_statements)

        if self.check_only:
            return False

        forced = False
        if errors:
            print("ERR")
            self.print_errors(errors)

            if self.interactive:
                print(f"Migration determined to be backwards incompatible")
                response = input('Do you disagree? Type "yes" to allow migration: ')
                if response != "yes":
                    return False

                forced = True
            elif self.force_update:
                forced = True
            else:
                return False
        else:
            print("OK")

        self.state[app_label][migration_name] = dict(
            migration_name=migration_name,
            migration_hash=migration_hash,
            migration_forced="migration_forced" if forced else "",
        )

        return True

    @staticmethod
    def get_migration_hash(app_label, migration_name):
        hash_md5 = hashlib.md5()
        with open(get_migration_abspath(app_label, migration_name), "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @staticmethod
    def print_errors(errors):
        for err in errors:
            error_str = "\t{0}".format(err["err_msg"])
            if err["table"]:
                error_str += " (table: {0}".format(err["table"])
                if err["column"]:
                    error_str += ", column: {0}".format(err["column"])
                error_str += ")"
            print(error_str)

    def get_sql(self, app_label, migration_name):
        dev_null = open(os.devnull, "w")
        sql_statement = call_command(
            "sqlmigrate", app_label, migration_name, stdout=dev_null
        )
        return sql_statement.splitlines()

    @staticmethod
    def _gather_all_migrations():
        migration_loader = MigrationLoader(connection=None, load=False)
        migration_loader.load_disk()

        # Prune Django apps
        for (app_label, _), migration in migration_loader.disk_migrations.items():
            if app_label not in DJANGO_APPS_WITH_MIGRATIONS:
                yield migration
