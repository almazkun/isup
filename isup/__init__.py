def write_to_file(
    path_to: str,
    url: str,
    status: int,
    expected_status: int,
    elapsed: float,
) -> None:
    file_name = url.split("/")[-1]
    with open(path_to + file_name, "a+") as f:
        f.write(f"{url},{status},{expected_status},{elapsed}\n")


def check_save(path_to: str, url: str, expected_status: int = 200) -> None:
    logger.debug(f"check_save(): {url} {expected_status}")
    status, elapsed = check_url(url)
    write_to_file(path_to, url, status, expected_status, elapsed)
