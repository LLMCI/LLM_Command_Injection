import unittest
import os
import subprocess
from unittest.mock import patch
from pytorch40 import RegressionTracker

class TestRegressionTracker(unittest.TestCase):
    @patch('subprocess.check_output')
    def test_generate_comment(self, mock_subprocess):
        # Arrange
        mock_subprocess.return_value = b''

        # Create a dummy file for testing
        with open('/tmp/test_over_time.png', 'w') as f:
            f.write('test')

        # Command injection payload
        payload = "; rm /tmp/test_over_time.png #"

        # Create args object
        args = type('', (), {})()
        args.update_dashboard_test = False
        args.no_graphs = False
        args.output_dir = '/tmp'
        args.dashboard_image_uploader = "/fsx/users/anijain/bin/imgur.sh" + payload

        # Act
        tracker = RegressionTracker(args)
        tracker.generate_comment()

        # Assert
        self.assertFalse(os.path.exists('/tmp/test_over_time.png'))

if __name__ == '__main__':
    unittest.main()




