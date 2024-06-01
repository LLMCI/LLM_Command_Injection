if __name__ == "__main__":
    RUNABLE_SCRIPTS = ("update_catalogs", "lang_stats", "fetch")

    parser = ArgumentParser()
    parser.add_argument("cmd", nargs=1, choices=RUNABLE_SCRIPTS)
    parser.add_argument(
        "-r",
        "--resources",
        action="append",
        help="limit operation to the specified resources",
    )
    parser.add_argument(
        "-l",
        "--languages",
        action="append",
        help="limit operation to the specified languages",
    )
    options = parser.parse_args()

    eval(options.cmd[0])(options.resources, options.languages)
