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
"""Module for customizing ths logs."""
import logging
from typing import Optional


class UtilsLogs:
    """Utility class for logs."""

    @staticmethod
    def addLoggingLevel(
        levelName: str, levelNum: int, methodName: Optional[str] = None
    ) -> None:
        """Add a new logging level to the `logging` module.

        Parameters
        ----------
        levelName: str
            level name of the logging
        levelNum: int
            level number related to the level name
        methodName: Optional[str]
            method for both `logging` itself and the class returned by
            `logging.Logger`

        Returns
        -------
            None

        Raises
        ------
        AttributeError
            If this levelName or methodName is already defined in the
            logger.

        """
        if not methodName:
            methodName = levelName.lower()

        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(levelNum):
                self._log(levelNum, message, args, **kwargs)

        def logToRoot(message, *args, **kwargs):
            logging.log(levelNum, message, *args, **kwargs)

        logging.addLevelName(levelNum, levelName)
        setattr(logging, levelName, levelNum)
        setattr(logging.getLoggerClass(), methodName, logForLevel)
        setattr(logging, methodName, logToRoot)


class LogRecord(logging.LogRecord):
    """Specific class to handle output in logs."""

    def getMessage(self) -> str:
        """Return the message.

        Format the message according to the type of the message.

        Returns
        -------
        str
            the message
        """
        msg = str(self.msg)
        if isinstance(self.args, dict):
            return msg.format(self.args)
        return msg % self.args if self.args else msg


class CustomColorFormatter(logging.Formatter):
    """Color formatter."""

    UtilsLogs.addLoggingLevel("TRACE", 15)
    # Reset
    color_Off = "\033[0m"  # Text Reset

    log_colors = {
        logging.TRACE: "\033[0;36m",  # cyan
        logging.DEBUG: "\033[1;34m",  # blue
        logging.INFO: "\033[0;32m",  # green
        logging.WARNING: "\033[1;33m",  # yellow
        logging.ERROR: "\033[1;31m",  # red
        logging.CRITICAL: "\033[1;41m",  # red reverted
    }

    def format(self, record: LogRecord) -> str:  # type: ignore
        """Format the log.

        Parameters
        ----------
        record: LogRecord
            the log record

        Returns
        -------
        str
            the formatted log record
        """
        record.levelname = "{}{}{}".format(
            CustomColorFormatter.log_colors[record.levelno],
            record.levelname,
            CustomColorFormatter.color_Off,
        )
        record.msg = "{}{}{}".format(
            CustomColorFormatter.log_colors[record.levelno],
            record.msg,
            CustomColorFormatter.color_Off,
        )

        # Select the formatter according to the log if several handlers are
        # attached to the logger
        my_formatter = logging.Formatter
        my_handler = None
        handlers = logging.getLogger(__name__).handlers
        for handler in handlers:
            handler_level = handler.level
            if (
                handler_level
                == logging.getLogger(__name__).getEffectiveLevel()
            ):
                my_formatter._fmt = handler.formatter._fmt
                my_handler = handler
                break
        if my_handler is not None:
            [
                logging.getLogger(__name__).removeHandler(handler)
                for handler in handlers
                if handler != my_handler
            ]
        return my_formatter.format(self, record)


class ShellColorFormatter(CustomColorFormatter):
    """Shell Color formatter."""

    def format(self, record: LogRecord) -> str:
        """Format the log.

        Parameters
        ----------
        record: LogRecord
            the log record

        Returns
        -------
        str
            the formatted log record
        """
        record.msg = "{}{}{}".format(
            CustomColorFormatter.log_colors[logging.INFO],
            record.msg,
            CustomColorFormatter.color_Off,
        )
        return record.msg
