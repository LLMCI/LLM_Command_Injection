from torch.library import Library

lib = Library("aten", "FRAGMENT")

def register_old_op(name: str, schema: str, impl_str: str):
         """Registers an old version operator using impl_name as old op name."""
         lib.define(schema)
         try:
             exec(impl_str)
         except Exception as e:
             raise RuntimeError(f"Invalid upgrader string: {impl_str}") from e
         impl_lib.impl(name, locals()[name], "CompositeImplicitAutograd")

        
