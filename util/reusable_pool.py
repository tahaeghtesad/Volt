import logging
import time
from multiprocessing.pool import ThreadPool


class ReusablePool:
    """
    Manage Reusable objects for use by Client objects.
    """

    def __init__(self, size, constructor, clean_up):
        start = time.time()
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initiating instances...')
        with ThreadPool(size) as tp:
            self._reusables = tp.map(constructor, range(size))
            self._clean_up = clean_up
        self.logger.info(f'Instances initiated. Took {time.time() - start} (s).')

    def acquire(self):
        self.logger.info('Acquiring an instance.')
        return self._reusables.pop()

    def release(self, reusable):
        self.logger.info('Releasing an instance.')
        self._clean_up(reusable)
        self._reusables.append(reusable)
