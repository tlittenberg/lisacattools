# -*- coding: utf-8 -*-
# Copyright (C) 2020-2021 - Centre National d'Etudes Spatiales
# jean-christophe.malapert@cnes.fr
#
# This file is part of smt_crawler_lib.
#
# smt_crawler_lib is a free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301  USA
"""Some Utilities."""
import logging
import os
import time
import tracemalloc
from functools import partial
from functools import wraps


class UtilsMonitoring(object):
    """Some Utilities."""

    # pylint: disable:invalid_name
    @staticmethod
    def io(func=None, entry=True, exit=True, level=15):  # level=15
        """Monitor the input/output of a function.

        NB : Do not use this monitoring method on an __init__ if the class
        implements __repr__ with attributes

        Parameters
        ----------
        func: func
            function to monitor (default: {None})
        entry: bool
            True when the function must monitor the input (default: {True})
        exit: bool
            True when the function must monitor the output (default: {True})
        level: int
            Level from which the function must log
        Returns
        -------
        object : the result of the function
        """
        if func is None:
            return partial(
                UtilsMonitoring.io, entry=entry, exit=exit, level=level
            )

        @wraps(func)
        def wrapped(*args, **kwargs):
            name = func.__qualname__
            logger = logging.getLogger(__name__ + "." + name)

            if entry and logger.getEffectiveLevel() >= level:
                msg = f"Entering '{name}' (args={args}, kwargs={kwargs})"
                logger.log(level, msg)

            result = func(*args, **kwargs)

            if exit and logger.getEffectiveLevel() >= level:
                msg = f"Exiting '{name}' (result={result})"
                logger.log(level, msg)

            return result

        return wrapped

    @staticmethod
    def time_spend(func=None, level=logging.DEBUG, threshold_in_ms=1000):
        """Monitor the performances of a function.

        Parameters
        ----------
        func: func
            Function to monitor (default: {None})
        level: int
            Level from which the monitoring starts (default: {logging.DEBUG})
        threshold_in_ms: int
            an alert is sent at any level when the function duration >
            threshold_in_ms (default: {1000})

        Returns
        -------
        object : the result of the function
        """
        if func is None:
            return partial(UtilsMonitoring.time_spend, level=level)

        @wraps(func)
        def newfunc(*args, **kwargs):
            name = func.__class__.__name__
            logger = logging.getLogger(__name__ + "." + name)
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logger.log(
                level,
                "function [{}] finished in {:.2f} ms".format(
                    func.__qualname__, elapsed_time * 1000
                ),
            )
            if float(elapsed_time) * 1000 > threshold_in_ms:
                logger.warning(
                    "function [{}] is too long to compute : {:.2f} ms".format(
                        func.__qualname__, elapsed_time * 1000
                    )
                )
            return result

        return newfunc

    @staticmethod
    def size(func=None, level=logging.INFO):
        """Monitor the number of records in a file.

        Parameters
        ----------
        func: func
            Function to monitor (default: {None})
        level: int
            Level from which the monitoring starts (default: {logging.INFO})

        Returns
        -------
        object : the result of the function
        """
        if func is None:
            return partial(UtilsMonitoring.size, level=level)

        @wraps(func)
        def newfunc(*args, **kwargs):
            name = func.__name__
            logger = logging.getLogger(__name__ + "." + name)
            filename = os.path.basename(args[1])
            logger.log(level, "Loading file '%s'", filename)
            result = func(*args, **kwargs)
            type_result = type(result)
            if type_result in [type({}), type([])]:
                nb_records = len(result)
            else:
                try:
                    nb_records = result.shape
                except Exception:
                    nb_records = None

            if nb_records is not None:
                logger.info(
                    "File '%s' loaded with %s records",
                    filename,
                    str(nb_records),
                )
            else:
                logger.warning(
                    "Unable to load the number of records in file '%s' - "
                    "type: %s",
                    args[1],
                    type_result,
                )
            return result

        return newfunc

    @staticmethod
    def measure_memory(func=None, level=logging.DEBUG):
        """Measure the memory of the function

        Args:
            func (func, optional): Function to measure. Defaults to None.
            level (int, optional): Level of the log. Defaults to logging.INFO.

        Returns:
            object : the result of the function
        """
        if func is None:
            return partial(UtilsMonitoring.measure_memory, level=level)

        @wraps(func)
        def newfunc(*args, **kwargs):
            name = func.__class__.__name__
            logger = logging.getLogger(__name__ + "." + name)
            tracemalloc.start()
            result = func(*args, **kwargs)
            current, peak = tracemalloc.get_traced_memory()
            msg = f"""
            \033[37mFunction Name       :\033[35;1m {func.__name__}\033[0m
            \033[37mCurrent memory usage:\033[36m {current / 10 ** 6}MB\033[0m
            \033[37mPeak                :\033[36m {peak / 10 ** 6}MB\033[0m
            """
            logger.log(level, msg)
            tracemalloc.stop()
            return result

        return newfunc
