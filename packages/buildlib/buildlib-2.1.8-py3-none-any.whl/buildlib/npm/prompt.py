import prmt


def should_push(
    dst: str,
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question=f'Do you want to PUSH package to {dst}?\n',
        default=default,
        fmt=fmt,
    )
