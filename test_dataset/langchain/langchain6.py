def add(
    dependencies: Annotated[
        Optional[List[str]], typer.Argument(help="The dependency to add")
    ] = None,
    *,
    api_path: Annotated[List[str], typer.Option(help="API paths to add")] = [],
    project_dir: Annotated[
        Optional[Path], typer.Option(help="The project directory")
    ] = None,
    repo: Annotated[
        List[str],
        typer.Option(help="Install templates from a specific github repo instead"),
    ] = [],
    branch: Annotated[
        List[str], typer.Option(help="Install templates from a specific branch")
    ] = [],
):
    """
    Adds the specified template to the current LangServe app.

    e.g.:
    langchain app add extraction-openai-functions
    langchain app add git+ssh://git@github.com/efriis/simple-pirate.git
    """

    parsed_deps = parse_dependencies(dependencies, repo, branch, api_path)

    project_root = get_package_root(project_dir)

    package_dir = project_root / "packages"

    create_events(
        [{"event": "serve add", "properties": dict(parsed_dep=d)} for d in parsed_deps]
    )

    # group by repo/ref
    grouped: Dict[Tuple[str, Optional[str]], List[DependencySource]] = {}
    for dep in parsed_deps:
        key_tup = (dep["git"], dep["ref"])
        lst = grouped.get(key_tup, [])
        lst.append(dep)
        grouped[key_tup] = lst

    installed_destination_paths: List[Path] = []
    installed_destination_names: List[str] = []
    installed_exports: List[LangServeExport] = []

    for (git, ref), group_deps in grouped.items():
        if len(group_deps) == 1:
            typer.echo(f"Adding {git}@{ref}...")
        else:
            typer.echo(f"Adding {len(group_deps)} templates from {git}@{ref}")
        source_repo_path = update_repo(git, ref, REPO_DIR)

        for dep in group_deps:
            source_path = (
                source_repo_path / dep["subdirectory"]
                if dep["subdirectory"]
                else source_repo_path
            )
            pyproject_path = source_path / "pyproject.toml"
            if not pyproject_path.exists():
                typer.echo(f"Could not find {pyproject_path}")
                continue
            langserve_export = get_langserve_export(pyproject_path)

            # default path to package_name
            inner_api_path = dep["api_path"] or langserve_export["package_name"]

            destination_path = package_dir / inner_api_path
            if destination_path.exists():
                typer.echo(
                    f"Folder {str(inner_api_path)} already exists. " "Skipping...",
                )
                continue
            copy_repo(source_path, destination_path)
            typer.echo(f" - Downloaded {dep['subdirectory']} to {inner_api_path}")
            installed_destination_paths.append(destination_path)
            installed_destination_names.append(inner_api_path)
            installed_exports.append(langserve_export)

    if len(installed_destination_paths) == 0:
        typer.echo("No packages installed. Exiting.")
        return

    try:
        add_dependencies_to_pyproject_toml(
            project_root / "pyproject.toml",
            zip(installed_destination_names, installed_destination_paths),
        )
    except Exception:
        # Can fail if user modified/removed pyproject.toml
        typer.echo("Failed to add dependencies to pyproject.toml, continuing...")

    try:
        cwd = Path.cwd()
        installed_destination_strs = [
            str(p.relative_to(cwd)) for p in installed_destination_paths
        ]
    except ValueError:
        # Can fail if the cwd is not a parent of the package
        typer.echo("Failed to print install command, continuing...")
    else:
        cmd = ["pip", "install", "-e"] + installed_destination_strs
        cmd_str = " \\\n  ".join(installed_destination_strs)
        install_str = f"To install:\n\npip install -e \\\n  {cmd_str}"
        typer.echo(install_str)

        if typer.confirm("Run it?"):
            subprocess.run(cmd, cwd=cwd)

    if typer.confirm("\nGenerate route code for these packages?", default=True):
        chain_names = []
        for e in installed_exports:
            original_candidate = f'{e["package_name"].replace("-", "_")}_chain'
            candidate = original_candidate
            i = 2
            while candidate in chain_names:
                candidate = original_candidate + "_" + str(i)
                i += 1
            chain_names.append(candidate)

        api_paths = [
            str(Path("/") / path.relative_to(package_dir))
            for path in installed_destination_paths
        ]

        imports = [
            f"from {e['module']} import {e['attr']} as {name}"
            for e, name in zip(installed_exports, chain_names)
        ]
        routes = [
            f'add_routes(app, {name}, path="{path}")'
            for name, path in zip(chain_names, api_paths)
        ]

        lines = (
            ["", "Great! Add the following to your app:\n\n```", ""]
            + imports
            + [""]
            + routes
            + ["```"]
        )
        typer.echo("\n".join(lines))
