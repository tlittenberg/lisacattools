# -*- coding: utf-8 -*-
# lisacattools - A small example package for using LISA catalogs
# Copyright (C) 2020 - 2025 - James I. Thorpe, Tyson B. Littenberg, Jean-Christophe Malapert
# This file is part of lisacattools <https://github.com/tlittenberg/lisacattools>
# SPDX-License-Identifier: Apache-2.0

"""Some Utilities."""
from loguru import logger
import os
import time
import tracemalloc
from functools import partial
from functools import wraps

from enum import IntEnum

class LogLevel(IntEnum):
    TRACE = 5
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class UtilsMonitoring(object):
    """Some Utilities."""


    @staticmethod
    def log_io(level="INFO"):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                logger.log(level, f"➡️> {func.__qualname__} called with args={args}, kwargs={kwargs}")
                result = func(*args, **kwargs)
                logger.log(level, f"<⬅️ {func.__qualname__} returned {result}")
                return result
            return wrapper
        return decorator


    @staticmethod
    def time_spent(func=None, level="DEBUG", threshold_in_ms=1000):
        """
        Decorator to measure the execution time of a function.

        Parameters
        ----------
        func : callable or None
            Function to decorate.
        level : str
            Log level for normal execution time.
        threshold_in_ms : int
            Threshold in milliseconds to trigger a warning.
        """
        if func is None:
            return partial(UtilsMonitoring.time_spent, level=level, threshold_in_ms=threshold_in_ms)

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed_ms = (time.time() - start) * 1000

            logger.log(level, f"⏱ {func.__qualname__} executed in {elapsed_ms:.2f} ms")

            if elapsed_ms > threshold_in_ms:
                logger.warning(f"⚠️ {func.__qualname__} took too long: {elapsed_ms:.2f} ms")

            return result

        return wrapper

    @staticmethod
    def size(func=None, level="INFO"):
        """
        Decorator to log the number of records loaded from a file.

        Parameters
        ----------
        func : callable or None
            Function to decorate.
        level : str
            Log level to use (default: "INFO").
        """
        if func is None:
            return partial(UtilsMonitoring.size, level=level)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Supposons que le deuxième argument est un chemin de fichier
            filename = os.path.basename(args[1]) if len(args) > 1 else "unknown"

            logger.log(level, f"📂 Loading file '{filename}'")

            result = func(*args, **kwargs)

            nb_records = None
            if isinstance(result, (list, dict)):
                nb_records = len(result)
            elif hasattr(result, "shape"):
                nb_records = result.shape
            else:
                logger.warning(f"❗ Unable to determine size of result from '{filename}' (type: {type(result)})")

            if nb_records is not None:
                logger.info(f"✅ File '{filename}' loaded with {nb_records} records")

            return result

        return wrapper

    @staticmethod
    def measure_memory(func=None, level="DEBUG"):
        """
        Decorator to measure memory usage of a function.

        Parameters
        ----------
        func : callable or None
            Function to decorate.
        level : str
            Log level to use (default: "DEBUG").
        """
        if func is None:
            return partial(UtilsMonitoring.measure_memory, level=level)

        @wraps(func)
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            result = func(*args, **kwargs)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            logger.log(
                level,
                f"🧠 Memory usage for '{func.__qualname__}': "
                f"Current = {current / 1_000_000:.3f} MB, "
                f"Peak = {peak / 1_000_000:.3f} MB"
            )
            return result

        return wrapper
