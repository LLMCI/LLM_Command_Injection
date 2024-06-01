import unittest
import os

def runstring(astr, dict):
     exec(astr, dict)
        
class TestRunString(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_file.txt"
        with open(self.test_file, "w") as file:
            file.write("This is a test file")
            

    def test_runstring(self):
        # Define a command to be executed
        command = f"os.remove('{self.test_file}')"
        # Run the command using the vulnerable function
        runstring(command, {"os": os})
        # Check if the command was executed by verifying the file was removed
        self.assertFalse(os.path.exists(self.test_file))

    

if __name__ == '__main__':
    unittest.main()

