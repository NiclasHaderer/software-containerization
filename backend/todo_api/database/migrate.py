import importlib.util
import os
from collections.abc import Coroutine
from importlib import import_module
from inspect import isfunction, signature, getsource
from pathlib import Path
from types import ModuleType
from typing import Literal

from databases import Database

from todo_api.database import get_db

MigrationAction = Literal["migrate"] | Literal["rollback"]


def _import_module_from_string(name: str, source: str):
    # my_code = getsource(module)
    # mymodule = _import_module_from_string(name=f".migrations.v1.sadf", source=my_code)
    spec = importlib.util.spec_from_loader(name, loader=None)
    module = importlib.util.module_from_spec(spec)
    exec(source, module.__dict__)
    return module


def _get_migration_files() -> list[os.DirEntry]:
    migrations_folder = Path(__file__).parent / "migrations"
    migration_files: list[os.DirEntry] = []
    with os.scandir(str(migrations_folder)) as entries:
        for entry in entries:
            if entry.is_file() and Path(entry.path).suffix == ".py":
                migration_files.append(entry)
    migration_files.sort(key=lambda f: f.name)
    return migration_files


class MigrationEntry:
    def __init__(self, module: ModuleType, version: str):
        self.module = module
        self.version = version

    async def migrate(self, db: Database):
        result = self.module.__dict__.get("migrate")(db)
        if isinstance(result, Coroutine):
            return await result
        return result

    async def rollback(self, db: Database):
        result = self.module.__dict__.get("rollback")(db)
        if isinstance(result, Coroutine):
            return await result
        return result

    def __str__(self) -> str:
        return getsource(self.module)


def _get_migration_functions(
        files: list[os.DirEntry],
) -> list[MigrationEntry]:
    migration_functions = []
    for file in files:
        version = Path(file.name).with_suffix("").name
        module = import_module(f".migrations.{version}", package="todo_api.database")
        migration_function = module.__dict__.get("migrate")
        rollback_function = module.__dict__.get("rollback")

        if not isfunction(migration_function) or not isfunction(rollback_function):
            raise Exception(
                f"Export members 'migrate' and 'rollback' of migration {version} have to be functions"
            )

        migration_function_signature = signature(migration_function)
        rollback_function_signature = signature(rollback_function)
        if (
                len(migration_function_signature.parameters) != 1
                or len(rollback_function_signature.parameters) != 1
        ):
            raise Exception("Migration and rollback function take only one argument")

        migration_param_type = [*migration_function_signature.parameters.values()][0].annotation
        rollback_param_type = [*rollback_function_signature.parameters.values()][0].annotation
        if migration_param_type != Database or rollback_param_type != Database:
            raise Exception(
                "The type of the migration and rollback function parameter has to be of type Database"
            )

        migration_functions.append(MigrationEntry(module, version))

    return migration_functions


async def _get_migrations_to_run(
        migrations: list[MigrationEntry],
) -> list[MigrationEntry]:
    current_version = await _get_current_migration_version()
    if current_version is None:
        return migrations

    migration_index = [
        i for i in range(0, len(migrations)) if migrations[i].version == current_version
    ][0]
    return migrations[migration_index + 1:]


async def _setup_migration_table():
    db = await get_db()
    await db.execute(
        """CREATE TABLE IF NOT EXISTS migrations (version varchar(265) unique NOT NULL , action text NOT NULL)"""
    )
    first_time = await db.fetch_one("""SELECT * from migrations""") is None
    if first_time:
        await db.execute(
            """INSERT INTO migrations (version, action) VALUES ('current_version', '')"""
        )


async def _get_current_migration_version() -> str | None:
    db = await get_db()
    version = await db.fetch_one(
        """SELECT action from migrations WHERE version = 'current_version'"""
    )
    return version[0] or None


async def _update_migration_version(new_version: str):
    db = await get_db()
    await db.execute(
        """UPDATE migrations SET action = :new_version WHERE version = 'current_version'""",
        {"new_version": new_version},
    )


async def run_migrations():
    await _setup_migration_table()
    potential_migrations = _get_migration_functions(_get_migration_files())
    migrations = await _get_migrations_to_run(potential_migrations)
    db = await get_db()
    print(f"Running {len(migrations)} migrations")
    for migration in migrations:
        print(f"Running migration for version {migration.version}")
        await migration.migrate(db)
        await db.execute(
            """INSERT INTO migrations (version, action) VALUES (:version, :action)""",
            {"version": migration.version, "action": str(migration)},
        )
        await _update_migration_version(migration.version)
    print("Successfully ran all migrations")


async def run_rollback(target_version: str):
    await _setup_migration_table()
    db = await get_db()
    executed_migrations = await db.fetch_all(
        """SELECT * FROM migrations WHERE version != 'current_version' ORDER BY version"""
    )

    rollbacks_to_execute = []
    for migrationIdx in range(0, len(executed_migrations)):
        if executed_migrations[migrationIdx]['version'] == target_version:
            rollbacks_to_execute = executed_migrations[migrationIdx + 1:]
            rollbacks_to_execute.reverse()
            break

    rollbacks_to_execute = [
        MigrationEntry(
            module=_import_module_from_string(
                source=rollback["action"], name=f"migrations.{rollback['version']}"
            ),
            version=rollback["version"],
        )
        for rollback in rollbacks_to_execute
    ]
    print(f"Running {len(rollbacks_to_execute)} rollbacks")
    for rollbackIdx in range(0, len(rollbacks_to_execute)):
        rollback = rollbacks_to_execute[rollbackIdx]
        print(f"Running rollback for version {rollback.version}")
        await rollback.rollback(db)
        await db.execute("""DELETE FROM migrations WHERE version = :version""", {"version": rollback.version})
        if rollbackIdx + 1 < len(rollbacks_to_execute):
            await _update_migration_version(rollbacks_to_execute[rollbackIdx + 1].version)
        else:
            final_version = executed_migrations[len(executed_migrations) - len(rollbacks_to_execute) - 1]['version']
            await _update_migration_version(final_version)

    print("Successfully ran all rollbacks")
