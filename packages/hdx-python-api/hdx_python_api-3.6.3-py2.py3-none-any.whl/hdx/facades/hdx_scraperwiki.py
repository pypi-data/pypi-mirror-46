# -*- coding: utf-8 -*-
"""Facade that handles ScraperWiki and calls project main function"""
import logging
import sys
from typing import Callable

import scraperwiki
from hdx.utilities.easy_logging import setup_logging

from hdx.facades import logging_kwargs, simple

logger = logging.getLogger(__name__)
setup_logging(**logging_kwargs)


def facade(projectmainfn, **kwargs):
    # type: (Callable[[], None], Any) -> bool
    """Facade that handles ScraperWiki and calls project main function

    Args:
        projectmainfn (() -> None): main function of project
        **kwargs: configuration parameters to pass to HDX Configuration class

    Returns:
        bool: True = success, False = failure
    """

    try:
        #
        # Setting up configuration
        #
        simple.facade(projectmainfn, **kwargs)

    except Exception as e:
        logger.critical(e, exc_info=True)
        scraperwiki.status('error', 'Run failed: %s' % sys.exc_info()[0])
        return False
    logger.info('Run completed successfully.\n')
    scraperwiki.status('ok')
    return True
