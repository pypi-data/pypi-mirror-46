#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .settings import Settings as SETTINGS

__all__ = ['SETTINGS']

if SETTINGS.__SPECIFIED__ is True:
    
    from .punittest import PUnittest, logger
    from .testrunner import TestRunner
    from .testresult import TestResult
    
    __all__.extend(['PUnittest', 'TestRunner', 'TestResult', 'logger'])


def RELOAD_SETTINGS():
    SETTINGS.__SPECIFIED__ = True
    from importlib import reload
    import punittest
    reload(punittest)
