def generate_nth_fibonacci(n):
    """Generate the nth Fibonacci number.

    The sequence F_n of Fibonacci numbers is defined by the recurrence relation:
    F_n = F_{n-1} + F_{n-2}, with F_0 = 0 and F_1 = 1

    Parameters:
        n (int): the nth integer in the sequence to calculate

    Returns:
        the value of the nth integer in the Fibonacci sequence

    """
    if not isinstance(n, int):
        raise ValueError('n must be an integer')

    if n < 0:
        raise ValueError('Cannot generate fibonacci number for negative n')

    if n == 0 or n == 1:
        return n
    return generate_nth_fibonacci(n - 1) + generate_nth_fibonacci(n - 2)
