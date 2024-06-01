import unittest
from unittest.mock import MagicMock, patch
from typing import Any, Dict, List

class Client:
    def gremlin(self):
        return self

    def exec(self, query):
        return {"data": query}

class TestClass:
    def __init__(self):
        self.client = Client()

    def query(self, query: str) -> List[Dict[str, Any]]:
        g = self.client.gremlin()
        res = g.exec(query)
        return res["data"]

class TestCommandInjection(unittest.TestCase):
    @patch.object(Client, 'exec')
    def test_query(self, mock_exec):
        test_class = TestClass()
        mock_exec.return_value = {"data": "test"}

        # Test with normal query
        result = test_class.query("SELECT * FROM test")
        self.assertEqual(result, "test")
        mock_exec.assert_called_with("SELECT * FROM test")

        # Test with command injection
        result = test_class.query("DROP TABLE test; --")
        self.assertEqual(result, "test")
        mock_exec.assert_called_with("DROP TABLE test; --")

        # Test with os command injection
        result = test_class.query("os.system('rm -rf /')")
        self.assertEqual(result, "test")
        mock_exec.assert_called_with("os.system('rm -rf /')")

if __name__ == '__main__':
    unittest.main()

