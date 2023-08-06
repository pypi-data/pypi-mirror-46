import unittest
from pyfakefs.fake_filesystem_unittest import Patcher
from lint_django_migrations.migration_linter import MigrationLinter


class LinterFunctionsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.patcher = Patcher()
        self.patcher.setUp()

    def tearDown(self) -> None:
        self.patcher.tearDown()

    def test_all_success(self):

        linter = MigrationLinter(
            include_apps=["app_correct"]
        )
        print(linter.lint_all_migrations())
        self.assertTrue(linter.lint_all_migrations())

    def test_invalid_migration(self):
        linter = MigrationLinter(
            include_apps=["app_add_not_null_column"]
        )
        print(linter.lint_all_migrations())
        self.assertTrue(linter.lint_all_migrations())
