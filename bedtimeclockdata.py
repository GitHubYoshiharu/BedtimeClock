# coding: UTF-8

import os

class UtilData:
    # 実行場所に依存しないように、動的にファイルパスを生成する。
    cur_dir = os.path.dirname( os.path.abspath(__file__) )
    SETTING_FILE_PATH = cur_dir + '\\' + 'bedtimeclocksetting.csv'
    BATCH_FILE_PATH   = cur_dir + '\\' + 'bedtimeclock.vbs'
    APP_FILE_PATH     = cur_dir + '\\' + 'bedtimeclock.py'
    BATCH_TASK_NAME = 'bedtimeclock-task'
    SETTING_KEYS = ('activate', 'batchtime', 'timetosleep', 'wakeuptime', 'sleeptime')