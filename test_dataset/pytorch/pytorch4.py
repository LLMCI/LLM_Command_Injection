from torch._guards import GuardBuilderBase
from typing import Any

CLOSURE_VARS = {
    "___check_type_id": check_type_id,
    "___check_obj_id": check_obj_id,
    "___current_backend": (
        lambda: torch._dynamo.eval_frame.guarded_backend_cache.current_backend
    ),
    "___lookup_backend": (
        lambda backend_obj_id: torch._dynamo.eval_frame.guarded_backend_cache.cached_backends[
            backend_obj_id
        ]
    ),
    "___skip_backend_check": (
        lambda: torch._dynamo.eval_frame.guarded_backend_cache.skip_backend_check_for_run_only_mode
    ),
    "___compile_config_hash": (
        lambda: torch._dynamo.eval_frame.get_saved_else_current_config_hash().hex()
    ),
    "___needs_nopython": (lambda: torch._dynamo.eval_frame.config_cache.nopython),
    "___odict_getitem": collections.OrderedDict.__getitem__,
    "___dict_param_key_ids": dict_param_key_ids,
    "___dict_const_keys": dict_const_keys,
    "___dict_version": dict_version,
    "___dict_contains": lambda a, b: a in b,
    "___tuple_iterator_len": tuple_iterator_len,
    "___tuple_iterator_getitem": tuple_iterator_getitem,
    "__math_isnan": math.isnan,
    "inf": float("inf"),
    "__load_module": importlib.import_module,
    "utils_device": torch.utils._device,
    "device": torch.device,
    "___from_numpy":
    # If not numpy array, piggy back on e.g. tensor guards to check type
    (lambda a: torch.as_tensor(a) if isinstance(a, (np.generic, np.ndarray)) else a),
    "torch": torch,
}


class GuardBuilder(GuardBuilderBase):
    def __init__(
        self,
        id_ref: Callable[[Any], str],
        source_ref: Callable[[Source], str],
        lookup_weakrefs: Callable[[object], ReferenceType[object]],
        local_scope: Dict[str, object],
        global_scope: Dict[str, object],
        check_fn_manager: CheckFunctionManager,
    ):
        self.id_ref = id_ref
        self.source_ref = source_ref
        self.lookup_weakrefs = lookup_weakrefs
        self.scope: Dict[str, Dict[str, object]] = {"L": local_scope, "G": global_scope}
        self.scope["__builtins__"] = builtins.__dict__.copy()
        for (
            name,
            package_module,
        ) in torch.package.package_importer._package_imported_modules.items():
            name = name.replace(">", "_").replace("<", "_").replace(".", "_dot_")
            # Write the package module into the scope so that we can import it
            self.scope["__builtins__"][name] = package_module
            # Write the demangled name to the scope so that we can use it
            self.scope[name] = package_module

    def get(self, name: str) -> Any:
        return eval(name, self.scope, CLOSURE_VARS)

