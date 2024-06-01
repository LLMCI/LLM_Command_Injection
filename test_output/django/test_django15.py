import unittest
import os
import subprocess
from unittest.mock import patch, MagicMock

class DatabaseClient:
    @staticmethod
    def settings_to_cmd_args_env(settings_dict, args):
        # Mocking the actual implementation
        return args, settings_dict

    def _clone_db(self, source_database_name, target_database_name):
        cmd_args, cmd_env = DatabaseClient.settings_to_cmd_args_env(
            self.connection.settings_dict, []
        )
        dump_cmd = [
            "mysqldump",
            *cmd_args[1:-1],
            "--routines",
            "--events",
            source_database_name,
        ]
        dump_env = load_env = {**os.environ, **cmd_env} if cmd_env else None
        load_cmd = [1,2]
        load_cmd[-1] = target_database_name

        with subprocess.Popen(
            dump_cmd, stdout=subprocess.PIPE, env=dump_env
        ) as dump_proc:
            with subprocess.Popen(
                load_cmd,
                stdin=dump_proc.stdout,
                stdout=subprocess.DEVNULL,
                env=load_env,
            ):
                # Allow dump_proc to receive a SIGPIPE if the load process exits.
                dump_proc.stdout.close()

class TestDatabaseClient(unittest.TestCase):
    @patch('subprocess.Popen')
    def test_clone_db_injection(self, mock_subprocess):
        # Arrange
        mock_subprocess.return_value = MagicMock()
        db_client = DatabaseClient()
        db_client.connection = MagicMock()
        db_client.connection.settings_dict = {}
        source_database_name = "source_db; rm -rf /"  # Command injection
        target_database_name = "target_db"

        # Act
        db_client._clone_db(source_database_name, target_database_name)

        # Assert
        self.assertTrue(mock_subprocess.called)
        call_args = mock_subprocess.call_args_list
        for call_arg in call_args:
            for arg in call_arg[0][0]:
                self.assertNotIn(";", arg)

if __name__ == '__main__':
    unittest.main()

