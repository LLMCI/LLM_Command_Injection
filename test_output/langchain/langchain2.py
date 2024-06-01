from typing import Any, Dict, List


class HugeGraph:

    def __init__(
        self,
        username: str = "default",
        password: str = "default",
        address: str = "127.0.0.1",
        port: int = 8081,
        graph: str = "hugegraph",
    ) -> None:
        """Create a new HugeGraph wrapper instance."""
        try:
            from hugegraph.connection import PyHugeGraph
        except ImportError:
            raise ValueError(
                "Please install HugeGraph Python client first: "
                "`pip3 install hugegraph-python`"
            )

        self.username = username
        self.password = password
        self.address = address
        self.port = port
        self.graph = graph
        self.client = PyHugeGraph(
            address, port, user=username, pwd=password, graph=graph
        )
        


    def query(self, query: str) -> List[Dict[str, Any]]:
        g = self.client.gremlin()
        res = g.exec(query)
        return res["data"]
