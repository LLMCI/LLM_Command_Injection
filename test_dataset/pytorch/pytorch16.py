def dynamic_getattr(self, tx, name):
        if not self.source:
            raise NotImplementedError()
            
        scope = {"L": tx.output.local_scope, "G": tx.output.global_scope}
        try:
            _input_associated_real_value = eval(self.source.name(), scope)
        except Exception as exc:
            raise NotImplementedError() from exc
