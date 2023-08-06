import prmt


def should_build(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question=f'Do you want to BUILD WHEEL?\n',
        default=default,
        fmt=fmt,
    )


def should_push(
    dst: str,
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question=f'Do you want to PUSH WHEEL to {dst}?\n',
        default=default,
        fmt=fmt,
    )
