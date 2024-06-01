def _make_module(
        self, name: str, filename: Optional[str], is_package: bool, parent: str
    ):
        mangled_filename = self._mangler.mangle(filename) if filename else None
        spec = importlib.machinery.ModuleSpec(
            name,
            self,  # type: ignore[arg-type]
            origin="<package_importer>",
            is_package=is_package,
        )
        module = importlib.util.module_from_spec(spec)
        self.modules[name] = module
        module.__name__ = self._mangler.mangle(name)
        ns = module.__dict__
        ns["__spec__"] = spec
        ns["__loader__"] = self
        ns["__file__"] = mangled_filename
        ns["__cached__"] = None
        ns["__builtins__"] = self.patched_builtins
        ns["__torch_package__"] = True

        # Add this module to our private global registry. It should be unique due to mangling.
        assert module.__name__ not in _package_imported_modules
        _package_imported_modules[module.__name__] = module

        # pre-emptively install on the parent to prevent IMPORT_FROM from trying to
        # access sys.modules
        self._install_on_parent(parent, name, module)

        if filename is not None:
            assert mangled_filename is not None
            # pre-emptively install the source in `linecache` so that stack traces,
            # `inspect`, etc. work.
            assert filename not in linecache.cache  # type: ignore[attr-defined]
            linecache.lazycache(mangled_filename, ns)

            code = self._compile_source(filename, mangled_filename)
            exec(code, ns)

        return module
