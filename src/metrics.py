def percentage_error(measured, theoretical):
    """
    Calculate the absolute percentage error between
    a measured value and a theoretical value.
    """

    if theoretical == 0:
        raise ValueError("Theoretical value cannot be zero.")

    return abs(measured - theoretical) / abs(theoretical) * 100