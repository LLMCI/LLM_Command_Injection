import os
import unittest
import tempfile
from unittest.mock import patch

class TestTocoFromProtos(unittest.TestCase):

    @patch('os.system')
    def test_command_injection(self, mock_system):
        # Arrange
        from TocoFromProtosTest import _run
        mock_system.return_value = 0
        sess = None
        in_tensor = None
        out_tensor = None
        should_succeed = True

        # Act
        _run(sess, in_tensor, out_tensor, should_succeed)

        # Assert
        self.assertTrue(mock_system.called)
        command = mock_system.call_args[0][0]
        self.assertIn('rm', command)

if __name__ == '__main__':
    unittest.main()

