def load_by_key_path(
        cls,
        key: str,
        path: str,
        linemap: Optional[List[Tuple[int, str]]] = None,
        attrs: Optional[Dict[str, Any]] = None,
    ) -> ModuleType:
        if linemap is None:
            linemap = []
        if key not in cls.cache:
            with open(path) as f:
                try:
                    code = compile(f.read(), path, "exec")
                except Exception as e:
                    raise RuntimeError(
                        f"Failed to import {path}\n{type(e).__name__}: {e}"
                    ) from None
                mod = ModuleType(f"{__name__}.{key}")
                mod.__file__ = path
                mod.key = key  # type: ignore[attr-defined]
                exec(code, mod.__dict__, mod.__dict__)
                sys.modules[mod.__name__] = mod
                # another thread might set this first
                cls.cache.setdefault(key, mod)
                # unzip into separate lines/nodes lists
                cls.linemaps[path] = list(zip(*linemap))

                if attrs is not None:
                    for k, v in attrs.items():
                        setattr(mod, k, v)

        return cls.cache[key]
