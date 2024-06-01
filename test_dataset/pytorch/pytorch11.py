def get_disallowed_checksums(
    binary: str,
) -> Set[str]:
    """
    Return the set of disallowed checksums from all http_archive rules
    """
    # Use bazel to get the list of external dependencies in XML format
    proc = subprocess.run(
        [binary, "query", "kind(http_archive, //external:*)", "--output=xml"],
        capture_output=True,
        check=True,
        text=True,
    )

    root = ET.fromstring(proc.stdout)

    disallowed_checksums = set()
    # Parse all the http_archive rules in the XML output
    for rule in root.findall('.//rule[@class="http_archive"]'):
        urls_node = rule.find('.//list[@name="urls"]')
        if urls_node is None:
            continue
        urls = [n.get("value") for n in urls_node.findall(".//string")]

        checksum_node = rule.find('.//string[@name="sha256"]')
        if checksum_node is None:
            continue
        checksum = checksum_node.get("value")

        if not checksum:
            continue

        if not is_required_checksum(urls):
            disallowed_checksums.add(checksum)

    return disallowed_checksums
