# coding: UTF-8

import os
import sys

class UtilData:
    # 実行場所に依存しないように、動的にファイルパスを生成する。
    cur_dir = os.path.dirname(sys.executable)
    SETTING_FILE_PATH = cur_dir + '\\' + 'bedtimeclocksetting.csv'
    BATCH_FILE_PATH   = cur_dir + '\\' + 'bedtimeclock.vbs'
    APP_FILE_PATH     = cur_dir + '\\' + 'bedtimeclock.exe'
    BATCH_TASK_NAME = 'bedtimeclock-task'
    SETTING_KEYS = ('activate', 'batchtime', 'timetosleep', 'wakeuptime', 'sleeptime')
    DEFAULT_VALUES = ([0], [21, 0], [1, 0], [7, 0], [8, 0])
    CHECK_CONSTRAINT = (
        '[0-1]',
        '([0-9]|1[0-9]|2[0-3]):[1-5]?[0-9]',
        '([0-9]|1[0-9]|2[0-3]):[1-5]?[0-9]',
        '([0-9]|1[0-9]|2[0-3]):[1-5]?[0-9]',
        '([0-9]|1[0-9]|2[0-3]):[1-5]?[0-9]'
    )