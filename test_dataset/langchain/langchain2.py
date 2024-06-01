from typing import Any, Dict, List


def query(self, query: str) -> List[Dict[str, Any]]:
        g = self.client.gremlin()
        res = g.exec(query)
        return res["data"]
