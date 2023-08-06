import prmt


def should_bump_version(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='BUMP VERSION number?\n',
        default=default,
        fmt=fmt,
    )
