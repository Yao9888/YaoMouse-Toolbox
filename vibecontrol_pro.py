import tkinter as tk
import customtkinter as ctk
import cv2
import numpy as np
import json
import os
import time
import threading
from PIL import Image, ImageTk, ImageGrab
from pynput import mouse, keyboard
import pyautogui
from queue import Queue

pyautogui.PAUSE = 0

class VibeControlPro:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("YaoMouse Toolbox")
        self.root.geometry("1100x700")
        ctk.set_appearance_mode("dark")
        
        self.tasks_dir = "./tasks"
        if not os.path.exists(self.tasks_dir):
            os.makedirs(self.tasks_dir)
            
        self.stop_event = threading.Event()
        self.monitoring_active = False
        self.clicker_active = False
        
        self.setup_ui()
        self.setup_listeners()
        
    def setup_ui(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="VibeControl Pro", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo.pack(pady=20)
        
        self.btn_visual = ctk.CTkButton(self.sidebar, text="视觉触发任务", command=lambda: self.show_frame("visual"))
        self.btn_visual.pack(pady=10, padx=20)
        
        self.btn_clicker = ctk.CTkButton(self.sidebar, text="极速点击器", command=lambda: self.show_frame("clicker"))
        self.btn_clicker.pack(pady=10, padx=20)
        
        self.btn_recorder = ctk.CTkButton(self.sidebar, text="路径录制器", command=lambda: self.show_frame("recorder"))
        self.btn_recorder.pack(pady=10, padx=20)
        
        self.main_area = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.frames = {}
        self.setup_visual_frame()
        self.setup_clicker_frame()
        self.setup_recorder_frame()
        
        self.show_frame("visual")

    def setup_visual_frame(self):
        frame = ctk.CTkFrame(self.main_area)
        self.frames["visual"] = frame
        
        lbl = ctk.CTkLabel(frame, text="视觉触发自动化", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.pack(pady=10)
        
        self.visual_task_name = ctk.CTkEntry(frame, placeholder_text="任务名称")
        self.visual_task_name.pack(pady=5, padx=20, fill="x")
        
        btn_snap = ctk.CTkButton(frame, text="1. 截取触发图像", command=self.start_screenshot_tool)
        btn_snap.pack(pady=10)
        
        btn_record = ctk.CTkButton(frame, text="2. 录制动作序列", command=self.start_action_recorder)
        btn_record.pack(pady=10)
        
        btn_save = ctk.CTkButton(frame, text="3. 保存视觉任务", command=self.save_visual_task)
        btn_save.pack(pady=10)
        
        self.visual_list = tk.Listbox(frame, bg="#2b2b2b", fg="white", borderwidth=0, highlightthickness=0)
        self.visual_list.pack(pady=10, padx=20, fill="both", expand=True)
        self.refresh_visual_list()
        
        self.btn_monitor = ctk.CTkButton(frame, text="开始监控屏幕", fg_color="green", command=self.toggle_monitoring)
        self.btn_monitor.pack(pady=10)

    def setup_clicker_frame(self):
        frame = ctk.CTkFrame(self.main_area)
        self.frames["clicker"] = frame
        
        lbl = ctk.CTkLabel(frame, text="极速自动点击器", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.pack(pady=10)
        
        self.click_freq = ctk.CTkEntry(frame, placeholder_text="点击频率 (毫秒)")
        self.click_freq.insert(0, "100")
        self.click_freq.pack(pady=5, padx=20)
        
        self.click_button = ctk.CTkOptionMenu(frame, values=["left", "right"])
        self.click_button.set("left")
        self.click_button.pack(pady=5, padx=20)
        
        self.btn_toggle_clicker = ctk.CTkButton(frame, text="启动点击器", command=self.toggle_clicker)
        self.btn_toggle_clicker.pack(pady=20)

    def setup_recorder_frame(self):
        frame = ctk.CTkFrame(self.main_area)
        self.frames["recorder"] = frame
        
        lbl = ctk.CTkLabel(frame, text="独立路径录制器", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.pack(pady=10)
        
        self.macro_name = ctk.CTkEntry(frame, placeholder_text="宏名称")
        self.macro_name.pack(pady=5, padx=20, fill="x")
        
        self.loop_count = ctk.CTkEntry(frame, placeholder_text="循环次数 (0 为无限)")
        self.loop_count.insert(0, "1")
        self.loop_count.pack(pady=5, padx=20)
        
        btn_rec = ctk.CTkButton(frame, text="开始录制宏", command=self.record_standalone_macro)
        btn_rec.pack(pady=10)
        
        btn_play = ctk.CTkButton(frame, text="播放选中的宏", command=self.play_standalone_macro)
        btn_play.pack(pady=10)
        
        self.macro_list = tk.Listbox(frame, bg="#2b2b2b", fg="white", borderwidth=0, highlightthickness=0)
        self.macro_list.pack(pady=10, padx=20, fill="both", expand=True)
        self.refresh_macro_list()

    def show_frame(self, name):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def setup_listeners(self):
        self.kb_listener = keyboard.Listener(on_press=self.on_key_press)
        self.kb_listener.start()

    def on_key_press(self, key):
        if key == keyboard.Key.esc:
            self.kill_switch()

    def kill_switch(self):
        self.stop_event.set()
        self.clicker_active = False
        self.monitoring_active = False
        if hasattr(self, 'btn_toggle_clicker'):
            self.btn_toggle_clicker.configure(text="启动点击器", fg_color="blue")
        if hasattr(self, 'btn_monitor'):
            self.btn_monitor.configure(text="开始监控屏幕", fg_color="green")
        print("全局紧急停止已激活 (ESC)")

    def start_screenshot_tool(self):
        self.snip_win = tk.Toplevel(self.root)
        self.snip_win.attributes("-alpha", 0.3)
        self.snip_win.attributes("-fullscreen", True)
        self.snip_win.attributes("-topmost", True)
        self.snip_win.config(cursor="cross")
        
        self.canvas = tk.Canvas(self.snip_win, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        self.canvas.bind("<ButtonPress-1>", self.on_snip_button_press)
        self.canvas.bind("<B1-Motion>", self.on_snip_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_snip_button_release)

    def on_snip_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red', width=2)

    def on_snip_move(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_snip_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        self.snip_win.destroy()
        
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        
        if x2 - x1 < 5 or y2 - y1 < 5: return
        
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.last_trigger_img = img
        img.save(os.path.join(self.tasks_dir, "temp_trigger.png"))

    def start_action_recorder(self):
        self.recorded_sequence = []
        self.recording = True
        
        def on_click(x, y, button, pressed):
            if pressed and self.recording:
                self.recorded_sequence.append({"type": "click", "x": x, "y": y, "button": str(button), "time": time.time()})
        
        self.mouse_listener = mouse.Listener(on_click=on_click)
        self.mouse_listener.start()
        
        self.rec_info = tk.Toplevel(self.root)
        self.rec_info.geometry("300x120")
        self.rec_info.attributes("-topmost", True)
        ctk.CTkLabel(self.rec_info, text="正在录制动作...\n点击鼠标记录位置\n完成后按 ESC 停止").pack(expand=True)

    def save_visual_task(self):
        name = self.visual_task_name.get()
        if not name or not hasattr(self, 'last_trigger_img'): return
        
        img_path = os.path.join(self.tasks_dir, f"{name}_trigger.png")
        self.last_trigger_img.save(img_path)
        
        task = {
            "task_name": name,
            "trigger_img": img_path,
            "sequence": self.recorded_sequence,
            "threshold": 0.95
        }
        
        with open(os.path.join(self.tasks_dir, f"{name}.json"), "w") as f:
            json.dump(task, f)
        self.refresh_visual_list()

    def refresh_visual_list(self):
        self.visual_list.delete(0, tk.END)
        for f in os.listdir(self.tasks_dir):
            if f.endswith(".json") and not f.endswith(".macro"):
                self.visual_list.insert(tk.END, f)

    def refresh_macro_list(self):
        self.macro_list.delete(0, tk.END)
        for f in os.listdir(self.tasks_dir):
            if f.endswith(".macro"):
                self.macro_list.insert(tk.END, f)

    def toggle_monitoring(self):
        if not self.monitoring_active:
            self.monitoring_active = True
            self.stop_event.clear()
            self.btn_monitor.configure(text="停止监控", fg_color="red")
            threading.Thread(target=self.monitor_loop, daemon=True).start()
        else:
            self.monitoring_active = False
            self.btn_monitor.configure(text="开始监控屏幕", fg_color="green")

    def monitor_loop(self):
        while self.monitoring_active and not self.stop_event.is_set():
            # 实时加载任务，确保新保存的任务能被识别
            tasks = []
            for f in os.listdir(self.tasks_dir):
                if f.endswith(".json") and not f.endswith(".macro"):
                    try:
                        with open(os.path.join(self.tasks_dir, f), "r") as file:
                            tasks.append(json.load(file))
                    except: continue
            
            if not tasks:
                time.sleep(1)
                continue

            screen = np.array(ImageGrab.grab())
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
            
            for task in tasks:
                if not self.monitoring_active or self.stop_event.is_set(): break
                trigger = cv2.imread(task["trigger_img"], 0)
                if trigger is None: continue
                
                res = cv2.matchTemplate(screen_gray, trigger, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                
                if max_val >= task["threshold"]:
                    print(f"匹配成功: {task['task_name']} (置信度: {max_val:.2f})")
                    self.execute_sequence(task["sequence"])
                    time.sleep(1) # 防止重复触发
            time.sleep(0.1)

    def execute_sequence(self, sequence):
        for action in sequence:
            if self.stop_event.is_set(): break
            if action["type"] == "click":
                pyautogui.click(action["x"], action["y"])
            elif action["type"] == "key":
                pyautogui.press(action["key"])

    def toggle_clicker(self):
        if not self.clicker_active:
            self.clicker_active = True
            self.stop_event.clear()
            self.btn_toggle_clicker.configure(text="停止点击器", fg_color="red")
            threading.Thread(target=self.clicker_loop, daemon=True).start()
        else:
            self.clicker_active = False
            self.btn_toggle_clicker.configure(text="启动点击器", fg_color="blue")

    def clicker_loop(self):
        try:
            freq = int(self.click_freq.get()) / 1000.0
        except:
            freq = 0.1
        btn = self.click_button.get()
        while self.clicker_active and not self.stop_event.is_set():
            pyautogui.click(button=btn)
            time.sleep(freq)

    def record_standalone_macro(self):
        self.standalone_sequence = []
        self.recording_standalone = True
        
        def on_click(x, y, button, pressed):
            if pressed and self.recording_standalone:
                self.standalone_sequence.append({"type": "click", "x": x, "y": y, "button": str(button), "time": time.time()})
        
        def on_press(key):
            if self.recording_standalone:
                if key == keyboard.Key.esc:
                    self.recording_standalone = False
                    return False
                try: k = key.char
                except: k = str(key)
                self.standalone_sequence.append({"type": "key", "key": k, "time": time.time()})

        self.m_l = mouse.Listener(on_click=on_click)
        self.k_l = keyboard.Listener(on_press=on_press)
        self.m_l.start()
        self.k_l.start()
        
        self.rec_win = tk.Toplevel(self.root)
        self.rec_win.geometry("300x100")
        self.rec_win.attributes("-topmost", True)
        ctk.CTkLabel(self.rec_win, text="正在录制宏...\n按 ESC 键停止录制").pack(expand=True)
        
        def check_finished():
            if not self.recording_standalone:
                self.rec_win.destroy()
                self.m_l.stop()
                self.save_standalone_macro()
            else:
                self.root.after(100, check_finished)
        
        self.root.after(100, check_finished)

    def save_standalone_macro(self):
        name = self.macro_name.get()
        if not name or not self.standalone_sequence: return
        path = os.path.join(self.tasks_dir, f"{name}.macro")
        with open(path, "w") as f:
            json.dump(self.standalone_sequence, f)
        self.refresh_macro_list()

    def play_standalone_macro(self):
        selection = self.macro_list.curselection()
        if not selection: return
        name = self.macro_list.get(selection[0]).replace(".macro", "")
        path = os.path.join(self.tasks_dir, f"{name}.macro")
        
        with open(path, "r") as f:
            macro = json.load(f)
            
        try:
            loops = int(self.loop_count.get())
        except:
            loops = 1
        self.stop_event.clear()
        threading.Thread(target=self.play_loop, args=(macro, loops), daemon=True).start()

    def play_loop(self, macro, loops):
        count = 0
        while (loops == 0 or count < loops) and not self.stop_event.is_set():
            for i, action in enumerate(macro):
                if self.stop_event.is_set(): break
                if i > 0:
                    delay = action["time"] - macro[i-1]["time"]
                    if delay > 0: time.sleep(delay)
                
                if action["type"] == "click":
                    pyautogui.click(action["x"], action["y"])
                elif action["type"] == "key":
                    # 处理特殊按键字符串
                    key_str = action["key"]
                    if "Key." in key_str:
                        key_str = key_str.replace("Key.", "")
                    pyautogui.press(key_str)
            count += 1
            print(f"宏播放完成: 第 {count} 次")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VibeControlPro()
    app.run()
