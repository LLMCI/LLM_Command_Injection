def new(
    name: Annotated[str, typer.Argument(help="The name of the folder to create")],
    with_poetry: Annotated[
        bool,
        typer.Option("--with-poetry/--no-poetry", help="Don't run poetry install"),
    ] = False,
):
    """
    Creates a new template package.
    """
    computed_name = name if name != "." else Path.cwd().name
    destination_dir = Path.cwd() / name if name != "." else Path.cwd()

    # copy over template from ../package_template
    project_template_dir = Path(__file__).parents[1] / "package_template"
    shutil.copytree(project_template_dir, destination_dir, dirs_exist_ok=name == ".")

    package_name_split = computed_name.split("/")
    package_name = (
        package_name_split[-2]
        if len(package_name_split) > 1 and package_name_split[-1] == ""
        else package_name_split[-1]
    )
    module_name = re.sub(
        r"[^a-zA-Z0-9_]",
        "_",
        package_name,
    )

    # generate app route code
    chain_name = f"{module_name}_chain"
    app_route_code = (
        f"from {module_name} import chain as {chain_name}\n\n"
        f'add_routes(app, {chain_name}, path="/{package_name}")'
    )

    # replace template strings
    pyproject = destination_dir / "pyproject.toml"
    pyproject_contents = pyproject.read_text()
    pyproject.write_text(
        pyproject_contents.replace("__package_name__", package_name).replace(
            "__module_name__", module_name
        )
    )

    # move module folder
    package_dir = destination_dir / module_name
    shutil.move(destination_dir / "package_template", package_dir)

    # update init
    init = package_dir / "__init__.py"
    init_contents = init.read_text()
    init.write_text(init_contents.replace("__module_name__", module_name))

    # replace readme
    readme = destination_dir / "README.md"
    readme_contents = readme.read_text()
    readme.write_text(
        readme_contents.replace("__package_name__", package_name).replace(
            "__app_route_code__", app_route_code
        )
    )

    # poetry install
    if with_poetry:
        subprocess.run(["poetry", "install"], cwd=destination_dir)
