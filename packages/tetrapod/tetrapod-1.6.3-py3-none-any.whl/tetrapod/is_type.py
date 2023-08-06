def is_iter( obj ):
    """
    evaluate is the object is an iterator

    Arguments
    ---------
    obj: any type

    Returns
    -------
    bool
        True if the object is iterable
    """
    try:
        iter( obj )
        return True
    except TypeError as e:
        return False
