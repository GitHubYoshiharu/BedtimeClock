# coding: UTF-8

import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import sys

from bedtimeclockdata import UtilData as ud

class App(ttk.Frame):
    def __init__(self, master, title='BedtimeClock Setting', width=300, height=650):
        super().__init__(master)
        master.title(title)
        master.geometry(f"{width}x{height}")
        master.resizable(0, 0)
        self.setting_dict = self.read_setting_file()

        ### １行目
        self.activate_frame = ttk.Frame(self, height=50)
        self.activate_frame.grid(column=0, row=0, pady=5, sticky='w')
        activate_cb = ttk.Checkbutton(
            self.activate_frame,
            name='cb',
            padding=(10),
            text='時計の表示を有効にする'
        )
        # デフォルトでは代替状態になっているので、解除する。
        activate_cb.state(['!alternate'])
        if self.setting_dict['activate'][0]==1:
            activate_cb.state(['selected'])
        activate_cb.pack(side='left')

        ### ２行目
        self.batchtime_frame = ttk.LabelFrame(self, width=300, height=50, labelanchor='nw', text='時計起動時刻')
        self.batchtime_frame.grid(column=0, row=1, pady=5)
        tk.Label(self.batchtime_frame, padx=8, text='時計を起動する\n時刻を設定します').grid(rowspan=2, column=0, row=0)
        self.create_lb(self.batchtime_frame, 'lb_h', self.setting_dict['batchtime'][0]).grid(column=1, row=0)
        tk.Label(self.batchtime_frame, text='時').grid(column=1, row=1)
        self.create_lb(self.batchtime_frame, 'lb_m', self.setting_dict['batchtime'][1]).grid(column=2, row=0)
        tk.Label(self.batchtime_frame, text='分').grid(column=2, row=1)

        ### ３行目
        self.timetosleep_frame = ttk.LabelFrame(self, width=300, height=50, labelanchor='nw', text='就寝準備時間')
        self.timetosleep_frame.grid(column=0, row=2, pady=5)
        tk.Label(self.timetosleep_frame, padx=8, text='パソコンを閉じてから\n寝るまでにかかる\n時間を設定します').grid(rowspan=2, column=0, row=0)
        self.create_lb(self.timetosleep_frame, 'lb_h', self.setting_dict['timetosleep'][0]).grid(column=1, row=0)
        tk.Label(self.timetosleep_frame, text='時').grid(column=1, row=1)
        self.create_lb(self.timetosleep_frame, 'lb_m', self.setting_dict['timetosleep'][1]).grid(column=2, row=0)
        tk.Label(self.timetosleep_frame, text='分').grid(column=2, row=1)

        ### ４行目
        self.wakeuptime_frame = ttk.LabelFrame(self, width=300, height=50, labelanchor='nw', text='起床予定時刻')
        self.wakeuptime_frame.grid(column=0, row=3, pady=5)
        tk.Label(self.wakeuptime_frame, padx=8, text='起床予定時刻を\n設定します').grid(rowspan=2, column=0, row=0)
        self.create_lb(self.wakeuptime_frame, 'lb_h', self.setting_dict['wakeuptime'][0]).grid(column=1, row=0)
        tk.Label(self.wakeuptime_frame, text='時').grid(column=1, row=1)
        self.create_lb(self.wakeuptime_frame, 'lb_m', self.setting_dict['wakeuptime'][1]).grid(column=2, row=0)
        tk.Label(self.wakeuptime_frame, text='分').grid(column=2, row=1)

        ### ５行目
        self.sleeptime_frame = ttk.LabelFrame(self, width=300, height=50, labelanchor='nw', text='睡眠予定時間')
        self.sleeptime_frame.grid(column=0, row=4, pady=5)
        tk.Label(self.sleeptime_frame, padx=8, text='睡眠予定時間を\n設定します').grid(rowspan=2, column=0, row=0)
        self.create_lb(self.sleeptime_frame, 'lb_h', self.setting_dict['sleeptime'][0]).grid(column=1, row=0)
        tk.Label(self.sleeptime_frame, text='時').grid(column=1, row=1)
        self.create_lb(self.sleeptime_frame, 'lb_m', self.setting_dict['sleeptime'][1]).grid(column=2, row=0)
        tk.Label(self.sleeptime_frame, text='分').grid(column=2, row=1)

        ### ６行目
        self.savesetting_frame = ttk.Frame(self, width=300, height=50)
        self.savesetting_frame.grid(column=0, row=5, pady=10)
        # OKボタン（設定の変更を保存し、ウィンドウを閉じる）
        self.savesetting_btn_ok = ttk.Button(self.savesetting_frame, text='OK', command=self.write_setting_file)
        self.savesetting_btn_ok.place(relx=0.65, rely=0.5, anchor='e')
        # キャンセルボタン（設定の変更を保存せずに、ウィンドウを閉じる）
        self.savesetting_btn_cancel = ttk.Button(self.savesetting_frame, text='キャンセル', command=sys.exit)
        self.savesetting_btn_cancel.place(relx=0.95, rely=0.5, anchor='e')

    def create_lb(self, target_frame, lb_name, default_value):
        ret_lb = tk.Listbox(
            target_frame,
            name=lb_name,
            exportselection=False,
            justify=tk.CENTER,
            height=5,
            width=8
        )
        itemlist = list(range(0,24)) if lb_name=='lb_h' else list(range(0,60))
        ret_lb.insert(tk.END, *itemlist)
        # デフォルト値の設定
        ret_lb.see(default_value)
        ret_lb.select_set(default_value)
        return ret_lb

    def get_child_by_name(self, frame, name):
        for child in frame.winfo_children():
            if child.winfo_name()==name:
                return child

    def get_lb_values(self, lb_frame):
        val_h = self.get_child_by_name(lb_frame, 'lb_h').curselection()[0]
        val_m = self.get_child_by_name(lb_frame, 'lb_m').curselection()[0]
        return [val_h, val_m]

    def read_form_values(self):
        ret_dict = {}
        is_activated = self.get_child_by_name(self.activate_frame, 'cb').instate(['selected'])
        ret_dict['activate']    = [1 if is_activated else 0]
        ret_dict['batchtime']   = self.get_lb_values(self.batchtime_frame)
        ret_dict['timetosleep'] = self.get_lb_values(self.timetosleep_frame)
        ret_dict['wakeuptime']  = self.get_lb_values(self.wakeuptime_frame)
        ret_dict['sleeptime']   = self.get_lb_values(self.sleeptime_frame)
        return ret_dict

    def read_setting_file(self):
        ret_dict = dict( zip(ud.SETTING_KEYS, ud.DEFAULT_VALUES) )
        # ex. 0,21:0,1:0,7:0,8:0
        if os.path.isfile(ud.SETTING_FILE_PATH):
            with open(ud.SETTING_FILE_PATH, 'r', encoding='utf_8') as fileobj:
                line = fileobj.readline().rstrip()
                for key, val in zip(ud.SETTING_KEYS, line.split(',')):
                    ret_dict[key] = [int(v) for v in val.split(':')]
        return ret_dict

    def write_setting_file(self):
        form_values_dict = self.read_form_values()

        ### バリデーションチェック 
        wakeuptime_m = form_values_dict['wakeuptime'][0]*60 + form_values_dict['wakeuptime'][1]
        # batchtimeから見て、wakeuptimeが翌日の場合（※wakeuptimeはbatchtimeよりも後だと”見なす”）。
        if form_values_dict['wakeuptime'][0] < form_values_dict['batchtime'][0]:
            wakeuptime_m += 24*60
        batchtime_m   = form_values_dict['batchtime'][0]*60 + form_values_dict['batchtime'][1]
        timetosleep_m = form_values_dict['timetosleep'][0]*60 + form_values_dict['timetosleep'][1]
        sleeptime_m   = form_values_dict['sleeptime'][0]*60 + form_values_dict['sleeptime'][1]
        if (wakeuptime_m - batchtime_m - timetosleep_m) <= 0: 
            messagebox.showerror('エラー', '時計起動時の睡眠時間が０分以下になります')
            return
        elif (wakeuptime_m - batchtime_m - timetosleep_m) <= sleeptime_m:
            ans = messagebox.askokcancel('警告', '時計起動時の睡眠時間が、睡眠予定時間以下になります。\nよろしいですか？')
            if not ans:
                return

        # タスクスケジューラに時計起動タスクを登録する。
        if form_values_dict['activate'][0]==1:
            create_cmd = 'schtasks /create /tn {0} /tr "{1} {2}" /sc daily /st {3:0>2d}:{4:0>2d} /F'
            create_cmd = create_cmd.format(
                ud.BATCH_TASK_NAME,
                ud.BATCH_FILE_PATH,
                ud.APP_FILE_PATH,
                form_values_dict['batchtime'][0],
                form_values_dict['batchtime'][1]
            )
            # "On Windows, subprocess.Popen tries to duplicate non-zero standard handles and fails if they're invalid."
            # らしい。よくわからなかったが。
            subprocess.Popen(
                create_cmd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            # タスクが登録されてない状態で削除しようとするとエラーを出力するが、動作に問題は無いので捨てる。
            subprocess.Popen(
                f'schtasks /delete /tn {ud.BATCH_TASK_NAME} /f',
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        # 設定ファイルを更新する（無い場合は作成される）。
        with open(ud.SETTING_FILE_PATH, 'w', encoding='utf_8') as fileobj:
            colon_list = [':'.join( list(map(str, form_values_dict[key])) ) for key in ud.SETTING_KEYS]
            fileobj.write( ','.join(colon_list) )
        sys.exit()

if __name__=="__main__":
    root = tk.Tk()
    app = App(master=root)
    app.pack()
    app.mainloop()