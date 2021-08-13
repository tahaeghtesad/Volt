import logging
import time
from multiprocessing.pool import ThreadPool


class ReusablePool:
    """
    Manage Reusable objects for use by Client objects.
    """

    def __init__(self, size, constructor, clean_up):
        # start = time.time()
        self.logger = logging.getLogger(__name__)
        # self.logger.info('Initiating instances...')
        # with ThreadPool(size) as tp:
        #     self._reusables = tp.map(constructor, range(size))
        #     self._clean_up = clean_up
        # self.logger.info(f'Instances initiated. Took {time.time() - start} (s).')
        self.constructor = constructor
        self.clean_up = clean_up
        self.created = 0
        self.deleted = 0

    def acquire(self):
        self.logger.info(f'Acquiring an instance. Running: {self.created - self.deleted}')
        self.created += 1
        return self.constructor(self.created)

    def release(self, reusable):
        self.logger.info(f'Releasing an instance. Running: {self.created - self.deleted}')
        self.deleted += 1
        # self._clean_up(reusable)
        # self._reusables.append(reusable)
        reusable.close()
