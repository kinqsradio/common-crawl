import subprocess

def restore_database(dump_file_path, database_name, username, host='localhost', port=5433, pg_restore_path='/path/to/pg_restore'):
    try:
        # Construct the pg_restore command
        command = [
            pg_restore_path,
            '--host', host,
            '--port', str(port),
            '--username', username,
            '--dbname', database_name,
            '--clean',  # Drop database objects before recreating them
            '--no-owner',  # Do not restore ownership
            '--no-password',  # Do not prompt for password (assumes PGPASSWORD is set or .pgpass is configured)
            dump_file_path
        ]

        # Run the command
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
        print("Database restored successfully.")
    except subprocess.CalledProcessError as e:
        print("Error during database restoration:", e.stderr)


dump_file_path = 'db_backup_20240624.1.sql'
database_name = 'nineprimes'
username = 'anhdang'
pg_restore_path = '/Applications/Postgres.app/Contents/Versions/latest/bin/pg_restore'

restore_database(dump_file_path, database_name, username, pg_restore_path=pg_restore_path)
