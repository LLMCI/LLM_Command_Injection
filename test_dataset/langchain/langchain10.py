def _forward_propagate(self) -> None:
        try:
            import pandas as pd
        except ImportError as e:
            raise ImportError(
                "Unable to import pandas, please install with `pip install pandas`."
            ) from e
        entity_scope = {
            entity.name: entity for entity in self.causal_operations.entities
        }
        for entity in self.causal_operations.entities:
            if entity.code == "pass":
                continue
            else:
                # gist.github.com/dean0x7d/df5ce97e4a1a05be4d56d1378726ff92
                exec(entity.code, globals(), entity_scope)
        row_values = [entity.dict() for entity in entity_scope.values()]
        self._outcome_table = pd.DataFrame(row_values)
