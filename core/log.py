#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class Logger(object):

    def __init__(self,
                 log_dir: Path,
                 log_file_name: str = None,
                 show_level=logging.INFO,
                 maxBytes=5 * 1024 * 1024,
                 backupCount=5):

        self.log_dir = log_dir
        self.log_file_name = log_file_name
        self.show_level = show_level
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        self.formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)s>>%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        self.filehandlers = {}
        self.steamhandler = None

    def __create_handler(self, log_level: int):
        if log_level not in self.filehandlers.keys():
            if self.log_file_name:
                log_file = self.log_dir / f'{self.log_file_name} - {logging.getLevelName(log_level)}.log'
            else:
                log_file = self.log_dir / f'{logging.getLevelName(log_level)}.log'

            filehandler = RotatingFileHandler(log_file,
                                              encoding='utf-8',
                                              maxBytes=self.maxBytes,
                                              backupCount=self.backupCount)

            filehandler.setFormatter(self.formatter)
            filehandler.setLevel(log_level)
            self.filehandlers[log_level] = filehandler

        if not self.steamhandler:
            steamhandler = logging.StreamHandler()
            steamhandler.setFormatter(self.formatter)
            steamhandler.setLevel(self.show_level)
            self.steamhandler = steamhandler

    def __log(self, flag, message):
        logger = logging.getLogger(flag)
        log_level = logging._nameToLevel[flag.upper()]
        logger.setLevel(log_level)

        self.__create_handler(log_level)
        logger.addHandler(self.filehandlers[log_level])
        logger.addHandler(self.steamhandler)

        logger.log(log_level, message)

    def debug(self, message):
        self.__log('debug', message)

    def info(self, message):
        self.__log('info', message)

    def warning(self, message):
        self.__log('warning', message)

    def error(self, message):
        self.__log('error', message)

    def critical(self, message):
        self.__log('critical', message)
