from multiprocessing.pool import ThreadPool


class ReusablePool:
    """
    Manage Reusable objects for use by Client objects.
    """

    def __init__(self, size, constructor, clean_up):
        with ThreadPool(size) as tp:
            self._reusables = tp.map(constructor, range(size))
            self._clean_up = clean_up

    def acquire(self):
        return self._reusables.pop()

    def release(self, reusable):
        self._clean_up(reusable)
        self._reusables.append(reusable)