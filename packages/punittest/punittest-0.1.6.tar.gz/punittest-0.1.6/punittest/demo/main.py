#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from punittest import SETTINGS, RELOAD_SETTINGS

SETTINGS.EXCEL_TEST_SET = True
SETTINGS.RUN_TAGS = ["All"]
SETTINGS.LOG_FILE_SWITCH = True
SETTINGS.LOG_REPORT_SWITCH = True
SETTINGS.LOG_DIR = r"D:\Temp\Logs"
SETTINGS.REPORT_DIR = r"D:\Temp\Reports"
RELOAD_SETTINGS()


from punittest import TestRunner

runner = TestRunner("demo接口测试用例")
runner.run()
