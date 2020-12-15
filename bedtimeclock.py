# coding: UTF-8

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import time
import os
import sys
import re

from bedtimeclockdata import UtilData as ud

class App(ttk.Frame):
    BG_COLOR = '#282828'
    WIN_WIDTH = 380 
    WIN_HEIGHT = 200

    def __init__(self, master, setting_dict, title='BedtimeClock'):
        super().__init__(master)
        master.title(title)
        # ディスプレイの右上に表示する。
        win_x = self.winfo_screenwidth() - App.WIN_WIDTH
        master.geometry(f"{App.WIN_WIDTH}x{App.WIN_HEIGHT}+{win_x}+0")
        master.resizable(0, 0)
        # 常にディスプレイの最前面に表示する。
        master.attributes("-topmost", True)
        self.setting_dict = setting_dict

        # 起床日時が現在日時から見て同じ日か翌日かを判定する。
        now = datetime.datetime.now()
        if self.setting_dict['wakeuptime'][0] < now.hour:
            self.wakeuptime = now.replace(hour=self.setting_dict['wakeuptime'][0], minute=self.setting_dict['wakeuptime'][1]) + datetime.timedelta(days=1)
        else:
            self.wakeuptime = now.replace(hour=self.setting_dict['wakeuptime'][0], minute=self.setting_dict['wakeuptime'][1])

        self.cvs = tk.Canvas(root, width=App.WIN_WIDTH, height=App.WIN_HEIGHT, background=App.BG_COLOR)
        self.cvs.pack()
        self.init_UI()

    def init_UI(self):
        bedtime = datetime.datetime.now() + datetime.timedelta(hours=self.setting_dict['timetosleep'][0], minutes=self.setting_dict['timetosleep'][1])
        bedtime_str = '{0:0>2d}:{1:0>2d}'.format(bedtime.hour, bedtime.minute)
        sleeptime = self.wakeuptime - bedtime
        # 小数点以下を切り捨てる。
        sleeptime_seconds = int( sleeptime.total_seconds() )
        sleeptime_h = sleeptime_seconds // 3600
        sleeptime_m = (sleeptime_seconds % 3600) // 60
        sleeptime_str = '{0}時間 {1}分'.format(sleeptime_h, sleeptime_m)
        wakeuptime_str = '{0:0>2d}:{1:0>2d}'.format(self.setting_dict['wakeuptime'][0], self.setting_dict['wakeuptime'][1])

        self.cvs.create_rectangle(0, 0, App.WIN_WIDTH, App.WIN_HEIGHT, outline=App.BG_COLOR, fill=App.BG_COLOR)
        self.cvs.create_text(70, 40, text='就寝時刻', font=('', 20), fill='white')
        self.bedtime_str_id = self.cvs.create_text(220, 40, text=bedtime_str, font=('', 50), fill='#4C9EEB')
        self.cvs.create_text(70, 100, text='↓', font=('', 34), fill='#EA3323')
        self.cvs.create_text(140, 100, text='睡眠時間', font=('', 17), fill='white')
        self.sleeptime_str_id = self.cvs.create_text(280, 100, text=sleeptime_str, font=('', 24), fill='#4C9EEB')
        self.cvs.create_text(70, 160, text='起床時刻', font=('', 20), fill='white')
        self.wakeuptime_str_id = self.cvs.create_text(220, 160, text=wakeuptime_str, font=('', 50), fill='#4C9EEB')
        self.cvs.update()
        # 初回呼び出しを登録する。
        self.after(1000, self.update_UI)

    def update_UI(self):
        bedtime = datetime.datetime.now() + datetime.timedelta(hours=self.setting_dict['timetosleep'][0], minutes=self.setting_dict['timetosleep'][1])
        bedtime_str = '{0:0>2d}:{1:0>2d}'.format(bedtime.hour, bedtime.minute)
        sleeptime = self.wakeuptime - bedtime
        # 小数点以下を切り捨てる。
        sleeptime_seconds = int( sleeptime.total_seconds() )
        # 睡眠時間は負になり得ない。
        if sleeptime_seconds < 0:
            sys.exit()
        sleeptime_h = sleeptime_seconds // 3600
        sleeptime_m = (sleeptime_seconds % 3600) // 60
        sleeptime_str = '{0}時間 {1}分'.format(sleeptime_h, sleeptime_m)
        wakeuptime_str = '{0:0>2d}:{1:0>2d}'.format(self.setting_dict['wakeuptime'][0], self.setting_dict['wakeuptime'][1])

        # 睡眠時間が短くなるほど、文字列を危険色に変えていく。
        ideal_sleeptime = datetime.timedelta(hours=self.setting_dict['sleeptime'][0], minutes=self.setting_dict['sleeptime'][1])
        diff = ideal_sleeptime - sleeptime
        sleeptime_str_color = None
        if diff.total_seconds() <= 3600*1:
            sleeptime_str_color = '#4C9EEB'
        elif diff.total_seconds() <= 3600*2:
            sleeptime_str_color = '#ECDF2B'
        else:
            sleeptime_str_color = '#EA3323'

        # テキストは使い回す方が圧倒的に軽い。
        self.cvs.itemconfigure(self.bedtime_str_id, text=bedtime_str)
        self.cvs.itemconfigure(self.sleeptime_str_id, text=sleeptime_str, fill=sleeptime_str_color)
        self.cvs.itemconfigure(self.wakeuptime_str_id, text=wakeuptime_str)
        self.cvs.update()
        # １秒ごとに画面を更新する。
        self.after(1000, self.update_UI)

def read_setting_file():
    if os.path.isfile(ud.SETTING_FILE_PATH):
        with open(ud.SETTING_FILE_PATH, 'r', encoding='utf_8') as fileobj:
            line = fileobj.readline().rstrip()
            csv_list = line.split(',')
            # 設定の項目数が一致しているかどうかを検査する。
            if len(csv_list)!=len(ud.SETTING_KEYS):
                messagebox.showerror('エラー', '設定の項目数が一致しません')
                raise ValueError('num of setting values are not correct.')
            setting_vals = list()
            for val, pat in zip(csv_list, ud.CHECK_CONSTRAINT):
                # 設定値が制約を満たしているかどうかを検査する。
                if re.fullmatch(pat, val) is None:
                    messagebox.showerror('エラー', '設定値が不正です')
                    raise ValueError('setting value is not correct.')
                setting_vals.append([int(v) for v in val.split(':')])
        return dict( zip(ud.SETTING_KEYS, setting_vals) )
    else:
        messagebox.showerror('エラー', '設定ファイルが見つかりません')
        raise FileNotFoundError('"bedtimeclocksetting.csv" file is not found.')

if __name__=="__main__":
    dic = None
    try:
        dic = read_setting_file()
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit()
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit()
    root = tk.Tk()
    app = App(master=root, setting_dict=dic)
    app.pack()
    app.mainloop()