import logging

from kidx_nlu.test import main

logger = logging.getLogger(__name__)

if __name__ == '__main__':  # pragma: no cover
    logger.warning("Calling `kidx_nlu.evaluate` is deprecated. "
                   "Please use `kidx_nlu.test` instead.")
    main()
