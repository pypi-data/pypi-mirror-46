def logical_rshift(val: int, n: int):
    """Solution by NPE
    https://stackoverflow.com/a/5833119
    
    Parameters
    ----------
    val : int
        Integer to be right logical shifted
    n : int
        Number of bits to shift by
    
    Returns
    -------
    int
        Right logically shifted number
    """
    return val >> n if val >= 0 else (val + 0x100000000) >> n

