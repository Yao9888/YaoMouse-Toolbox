import tkinter as tk
from tkinter import filedialog, messagebox
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

class YaoMouseToolbox:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("YaoMouse Toolbox")
        self.root.geometry("1150x750")
        ctk.set_appearance_mode("dark")
        
        self.tasks_dir = os.path.abspath("./tasks")
        if not os.path.exists(self.tasks_dir):
            os.makedirs(self.tasks_dir)
            
        self.stop_event = threading.Event()
        self.monitoring_active = False
        self.clicker_active = False
        
        # Recording state
        self.is_recording = False
        self.recorded_events = []
        self.start_record_time = 0
        
        self.setup_ui()
        self.setup_listeners()
        
    def setup_ui(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self.root, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="YaoMouse Toolbox", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo.pack(pady=30)
        
        self.btn_visual = ctk.CTkButton(self.sidebar, text="视觉触发任务", command=lambda: self.show_frame("visual"))
        self.btn_visual.pack(pady=10, padx=20)
        
        self.btn_clicker = ctk.CTkButton(self.sidebar, text="增强型点击器", command=lambda: self.show_frame("clicker"))
        self.btn_clicker.pack(pady=10, padx=20)
        
        self.btn_recorder = ctk.CTkButton(self.sidebar, text="全功能录制器", command=lambda: self.show_frame("recorder"))
        self.btn_recorder.pack(pady=10, padx=20)
        
        self.btn_settings = ctk.CTkButton(self.sidebar, text="路径与设置", command=lambda: self.show_frame("settings"))
        self.btn_settings.pack(pady=10, padx=20)
        
        # Main Area
        self.main_area = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.frames = {}
        self.setup_visual_frame()
        self.setup_clicker_frame()
        self.setup_recorder_frame()
        self.setup_settings_frame()
        
        self.show_frame("visual")

    def setup_visual_frame(self):
        frame = ctk.CTkFrame(self.main_area)
        self.frames["visual"] = frame
        
        lbl = ctk.CTkLabel(frame, text="视觉触发自动化 (支持全键鼠回放)", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.pack(pady=10)
        
        # Task Creation
        create_box = ctk.CTkFrame(frame)
        create_box.pack(pady=10, padx=20, fill="x")
        
        self.visual_task_name = ctk.CTkEntry(create_box, placeholder_text="新任务名称")
        self.visual_task_name.pack(side="left", pady=10, padx=10, expand=True, fill="x")
        
        btn_snap = ctk.CTkButton(create_box, text="1. 截取图像", width=100, command=self.start_screenshot_tool)
        btn_snap.pack(side="left", padx=5)
        
        btn_record = ctk.CTkButton(create_box, text="2. 录制动作", width=100, command=self.start_full_recorder)
        btn_record.pack(side="left", padx=5)
        
        btn_save = ctk.CTkButton(create_box, text="3. 保存", width=80, command=self.save_visual_task)
        btn_save.pack(side="left", padx=5)
        
        # Task List
        list_box = ctk.CTkFrame(frame)
        list_box.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.visual_list = tk.Listbox(list_box, bg="#1e1e1e", fg="white", borderwidth=0, highlightthickness=0, font=("Arial", 11))
        self.visual_list.pack(side="left", pady=10, padx=10, fill="both", expand=True)
        
        scroll = ctk.CTkScrollbar(list_box, command=self.visual_list.yview)
        scroll.pack(side="right", fill="y")
        self.visual_list.configure(yscrollcommand=scroll.set)
        
        # Actions
        action_box = ctk.CTkFrame(frame)
        action_box.pack(pady=10, padx=20, fill="x")
        
        btn_del = ctk.CTkButton(action_box, text="删除选中", fg_color="#c0392b", hover_color="#e74c3c", command=lambda: self.delete_task("visual"))
        btn_del.pack(side="left", padx=10, pady=10)
        
        btn_import = ctk.CTkButton(action_box, text="导入任务", command=lambda: self.import_task("visual"))
        btn_import.pack(side="left", padx=10, pady=10)
        
        self.btn_monitor = ctk.CTkButton(action_box, text="开始监控屏幕", fg_color="#27ae60", hover_color="#2ecc71", command=self.toggle_monitoring)
        self.btn_monitor.pack(side="right", padx=10, pady=10)
        
        self.refresh_visual_list()

    def setup_clicker_frame(self):
        frame = ctk.CTkFrame(self.main_area)
        self.frames["clicker"] = frame
        
        lbl = ctk.CTkLabel(frame, text="增强型极速点击器", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.pack(pady=10)
        
        config_box = ctk.CTkFrame(frame)
        config_box.pack(pady=20, padx=40, fill="both")
        
        # Row 1: Button and Type
        r1 = ctk.CTkFrame(config_box, fg_color="transparent")
        r1.pack(pady=10, fill="x")
        ctk.CTkLabel(r1, text="点击按键:").pack(side="left", padx=10)
        self.click_button = ctk.CTkOptionMenu(r1, values=["左键 (Left)", "右键 (Right)", "中键 (Middle)"])
        self.click_button.set("左键 (Left)")
        self.click_button.pack(side="left", padx=10)
        
        ctk.CTkLabel(r1, text="点击类型:").pack(side="left", padx=10)
        self.click_type = ctk.CTkOptionMenu(r1, values=["单次点击", "双击", "三击"])
        self.click_type.set("单次点击")
        self.click_type.pack(side="left", padx=10)
        
        # Row 2: Frequency and Randomness
        r2 = ctk.CTkFrame(config_box, fg_color="transparent")
        r2.pack(pady=10, fill="x")
        ctk.CTkLabel(r2, text="固定频率 (ms):").pack(side="left", padx=10)
        self.click_freq = ctk.CTkEntry(r2, width=100)
        self.click_freq.insert(0, "100")
        self.click_freq.pack(side="left", padx=10)
        
        ctk.CTkLabel(r2, text="随机偏移 (ms):").pack(side="left", padx=10)
        self.click_random = ctk.CTkEntry(r2, width=100)
        self.click_random.insert(0, "0")
        self.click_random.pack(side="left", padx=10)
        
        # Row 3: Hold time
        r3 = ctk.CTkFrame(config_box, fg_color="transparent")
        r3.pack(pady=10, fill="x")
        ctk.CTkLabel(r3, text="按下时长 (ms):").pack(side="left", padx=10)
        self.click_hold = ctk.CTkEntry(r3, width=100)
        self.click_hold.insert(0, "10")
        self.click_hold.pack(side="left", padx=10)
        
        self.btn_toggle_clicker = ctk.CTkButton(frame, text="启动点击器", height=50, font=ctk.CTkFont(size=15, weight="bold"), command=self.toggle_clicker)
        self.btn_toggle_clicker.pack(pady=30)
        
        ctk.CTkLabel(frame, text="提示: 启动后按 ESC 键可立即停止", text_color="gray").pack()

    def setup_recorder_frame(self):
        frame = ctk.CTkFrame(self.main_area)
        self.frames["recorder"] = frame
        
        lbl = ctk.CTkLabel(frame, text="全功能动作录制器 (键鼠+精确时间)", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.pack(pady=10)
        
        # Macro Creation
        create_box = ctk.CTkFrame(frame)
        create_box.pack(pady=10, padx=20, fill="x")
        
        self.macro_name = ctk.CTkEntry(create_box, placeholder_text="宏名称")
        self.macro_name.pack(side="left", pady=10, padx=10, expand=True, fill="x")
        
        self.loop_count = ctk.CTkEntry(create_box, placeholder_text="循环 (0=无限)", width=100)
        self.loop_count.insert(0, "1")
        self.loop_count.pack(side="left", padx=5)
        
        btn_rec = ctk.CTkButton(create_box, text="开始录制", width=100, command=self.start_full_recorder)
        btn_rec.pack(side="left", padx=5)
        
        btn_save = ctk.CTkButton(create_box, text="保存宏", width=80, command=self.save_macro)
        btn_save.pack(side="left", padx=5)
        
        # Macro List
        list_box = ctk.CTkFrame(frame)
        list_box.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.macro_list = tk.Listbox(list_box, bg="#1e1e1e", fg="white", borderwidth=0, highlightthickness=0, font=("Arial", 11))
        self.macro_list.pack(side="left", pady=10, padx=10, fill="both", expand=True)
        
        scroll = ctk.CTkScrollbar(list_box, command=self.macro_list.yview)
        scroll.pack(side="right", fill="y")
        self.macro_list.configure(yscrollcommand=scroll.set)
        
        # Actions
        action_box = ctk.CTkFrame(frame)
        action_box.pack(pady=10, padx=20, fill="x")
        
        btn_del = ctk.CTkButton(action_box, text="删除选中", fg_color="#c0392b", hover_color="#e74c3c", command=lambda: self.delete_task("macro"))
        btn_del.pack(side="left", padx=10, pady=10)
        
        btn_import = ctk.CTkButton(action_box, text="导入宏", command=lambda: self.import_task("macro"))
        btn_import.pack(side="left", padx=10, pady=10)
        
        btn_play = ctk.CTkButton(action_box, text="播放选中宏", fg_color="#2980b9", hover_color="#3498db", command=self.play_macro)
        btn_play.pack(side="right", padx=10, pady=10)
        
        self.refresh_macro_list()

    def setup_settings_frame(self):
        frame = ctk.CTkFrame(self.main_area)
        self.frames["settings"] = frame
        
        lbl = ctk.CTkLabel(frame, text="路径与全局设置", font=ctk.CTkFont(size=18, weight="bold"))
        lbl.pack(pady=20)
        
        path_box = ctk.CTkFrame(frame)
        path_box.pack(pady=10, padx=40, fill="x")
        
        ctk.CTkLabel(path_box, text="当前任务保存路径:").pack(pady=5)
        self.path_entry = ctk.CTkEntry(path_box)
        self.path_entry.insert(0, self.tasks_dir)
        self.path_entry.pack(pady=5, padx=20, fill="x")
        
        btn_change = ctk.CTkButton(path_box, text="更改路径", command=self.change_tasks_dir)
        btn_change.pack(pady=10)
        
        info_box = ctk.CTkFrame(frame)
        info_box.pack(pady=20, padx=40, fill="both", expand=True)
        ctk.CTkLabel(info_box, text="使用说明:\n1. 视觉触发: 截图 -> 录制 -> 保存 -> 监控。\n2. 录制器: 录制时会捕捉所有鼠标点击、滚动和键盘按键。\n3. 紧急停止: 任何时候按 ESC 键都会立即停止所有自动化操作。\n4. 时间间隔: 播放时会严格遵守录制时的时间间隔。", justify="left").pack(pady=20, padx=20)

    def show_frame(self, name):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def setup_listeners(self):
        # Global ESC listener
        self.kb_listener = keyboard.Listener(on_press=self.on_global_key)
        self.kb_listener.start()

    def on_global_key(self, key):
        if key == keyboard.Key.esc:
            self.kill_switch()

    def kill_switch(self):
        self.stop_event.set()
        self.clicker_active = False
        self.monitoring_active = False
        self.is_recording = False
        
        # Reset UI buttons
        self.root.after(0, lambda: self.btn_toggle_clicker.configure(text="启动点击器", fg_color="#3b8ed0"))
        self.root.after(0, lambda: self.btn_monitor.configure(text="开始监控屏幕", fg_color="#27ae60"))
        print("全局紧急停止已激活 (ESC)")

    # --- Task Management ---
    def refresh_visual_list(self):
        self.visual_list.delete(0, tk.END)
        if not os.path.exists(self.tasks_dir): return
        for f in os.listdir(self.tasks_dir):
            if f.endswith(".vtask"):
                self.visual_list.insert(tk.END, f)

    def refresh_macro_list(self):
        self.macro_list.delete(0, tk.END)
        if not os.path.exists(self.tasks_dir): return
        for f in os.listdir(self.tasks_dir):
            if f.endswith(".macro"):
                self.macro_list.insert(tk.END, f)

    def delete_task(self, type):
        lb = self.visual_list if type == "visual" else self.macro_list
        selection = lb.curselection()
        if not selection: return
        
        filename = lb.get(selection[0])
        if messagebox.askyesno("确认删除", f"确定要删除 {filename} 吗?"):
            path = os.path.join(self.tasks_dir, filename)
            try:
                # If visual task, also delete trigger image
                if type == "visual":
                    with open(path, "r") as f:
                        data = json.load(f)
                        if os.path.exists(data.get("trigger_img", "")):
                            os.remove(data["trigger_img"])
                os.remove(path)
                if type == "visual": self.refresh_visual_list()
                else: self.refresh_macro_list()
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {e}")

    def import_task(self, type):
        ext = ".vtask" if type == "visual" else ".macro"
        file_path = filedialog.askopenfilename(filetypes=[(f"{type} files", f"*{ext}")])
        if not file_path: return
        
        try:
            import shutil
            dest = os.path.join(self.tasks_dir, os.path.basename(file_path))
            shutil.copy(file_path, dest)
            
            # If visual, try to find the associated image
            if type == "visual":
                with open(dest, "r") as f:
                    data = json.load(f)
                    img_src = data.get("trigger_img", "")
                    if os.path.exists(img_src):
                        img_dest = os.path.join(self.tasks_dir, os.path.basename(img_src))
                        shutil.copy(img_src, img_dest)
                        data["trigger_img"] = img_dest
                        with open(dest, "w") as fw:
                            json.dump(data, fw)
            
            if type == "visual": self.refresh_visual_list()
            else: self.refresh_macro_list()
            messagebox.showinfo("成功", "导入完成")
        except Exception as e:
            messagebox.showerror("错误", f"导入失败: {e}")

    def change_tasks_dir(self):
        new_dir = filedialog.askdirectory()
        if new_dir:
            self.tasks_dir = new_dir
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, self.tasks_dir)
            self.refresh_visual_list()
            self.refresh_macro_list()

    # --- Screenshot Tool ---
    def start_screenshot_tool(self):
        self.snip_win = tk.Toplevel(self.root)
        self.snip_win.attributes("-alpha", 0.3)
        self.snip_win.attributes("-fullscreen", True)
        self.snip_win.attributes("-topmost", True)
        self.snip_win.config(cursor="cross")
        
        self.canvas = tk.Canvas(self.snip_win, cursor="cross", bg="grey")
        self.canvas.pack(fill="both", expand=True)
        
        self.start_x = self.start_y = None
        self.rect = None
        
        self.canvas.bind("<ButtonPress-1>", self.on_snip_press)
        self.canvas.bind("<B1-Motion>", self.on_snip_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_snip_release)

    def on_snip_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red', width=2)

    def on_snip_move(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_snip_release(self, event):
        end_x, end_y = event.x, event.y
        self.snip_win.destroy()
        
        x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
        x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)
        
        if x2 - x1 < 5 or y2 - y1 < 5: return
        
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.last_trigger_img = img
        img.save(os.path.join(self.tasks_dir, "temp_trigger.png"))
        messagebox.showinfo("截图成功", "触发图像已截取")

    # --- Advanced Recorder ---
    def start_full_recorder(self):
        # 1. Create Overlay first for countdown
        if hasattr(self, 'rec_overlay') and self.rec_overlay.winfo_exists():
            self.rec_overlay.destroy()
            
        self.rec_overlay = tk.Toplevel(self.root)
        self.rec_overlay.geometry("400x220")
        self.rec_overlay.attributes("-topmost", True)
        self.rec_overlay.overrideredirect(True)
        
        # Center on screen
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.rec_overlay.geometry(f"400x220+{int(sw/2-200)}+{int(sh/2-110)}")
        
        # High contrast prominent background (Yellow/Gold)
        self.overlay_frame = ctk.CTkFrame(self.rec_overlay, border_width=5, border_color="black", fg_color="#f1c40f")
        self.overlay_frame.pack(fill="both", expand=True)
        
        self.status_label = ctk.CTkLabel(self.overlay_frame, text="准备录制...", font=("Arial", 28, "bold"), text_color="black")
        self.status_label.pack(pady=(30, 10))
        
        self.countdown_label = ctk.CTkLabel(self.overlay_frame, text="3", font=("Arial", 60, "bold"), text_color="black")
        self.countdown_label.pack(pady=10)
        
        # Start countdown sequence
        self.run_countdown(3)

    def run_countdown(self, count):
        if count > 0:
            self.countdown_label.configure(text=str(count))
            self.root.after(1000, lambda: self.run_countdown(count - 1))
        else:
            self.initiate_recording()

    def initiate_recording(self):
        self.recorded_events = []
        self.is_recording = True
        self.start_record_time = time.perf_counter()
        
        # Update UI to recording state
        self.status_label.configure(text="正在录制宏")
        self.countdown_label.pack_forget()
        
        self.rec_count_label = ctk.CTkLabel(self.overlay_frame, text="已捕捉动作: 0", font=("Arial", 16, "bold"), text_color="black")
        self.rec_count_label.pack(pady=10)
        
        ctk.CTkLabel(self.overlay_frame, text="[ 按 ESC 键停止录制 ]", font=("Arial", 14, "bold"), text_color="black").pack(pady=5)
        
        def on_click(x, y, button, pressed):
            if not self.is_recording: return False
            self.recorded_events.append({
                "type": "mouse_click",
                "button": str(button).split(".")[-1],
                "pressed": pressed,
                "x": x, "y": y,
                "time": time.perf_counter() - self.start_record_time
            })
            self.update_rec_count()

        def on_scroll(x, y, dx, dy):
            if not self.is_recording: return False
            self.recorded_events.append({
                "type": "mouse_scroll",
                "x": x, "y": y, "dx": dx, "dy": dy,
                "time": time.perf_counter() - self.start_record_time
            })
            self.update_rec_count()

        def on_press(key):
            if not self.is_recording: return False
            if key == keyboard.Key.esc:
                self.stop_recording()
                return False
            try: k = key.char
            except: k = str(key)
            self.recorded_events.append({
                "type": "key_event",
                "action": "press",
                "key": k,
                "time": time.perf_counter() - self.start_record_time
            })
            self.update_rec_count()

        def on_release(key):
            if not self.is_recording: return False
            if key == keyboard.Key.esc: return False
            try: k = key.char
            except: k = str(key)
            self.recorded_events.append({
                "type": "key_event",
                "action": "release",
                "key": k,
                "time": time.perf_counter() - self.start_record_time
            })
            self.update_rec_count()

        self.m_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
        self.k_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.m_listener.start()
        self.k_listener.start()

    def update_rec_count(self):
        if hasattr(self, 'rec_count_label'):
            self.rec_count_label.configure(text=f"已捕捉动作: {len(self.recorded_events)}")

    def update_rec_count(self):
        if hasattr(self, 'rec_count_label'):
            self.rec_count_label.configure(text=f"已捕捉动作: {len(self.recorded_events)}")

    def stop_recording(self):
        self.is_recording = False
        if hasattr(self, 'rec_overlay'):
            self.rec_overlay.destroy()
        if hasattr(self, 'm_listener'): self.m_listener.stop()
        if hasattr(self, 'k_listener'): self.k_listener.stop()
        messagebox.showinfo("录制完成", f"共捕捉到 {len(self.recorded_events)} 个动作事件")

    def save_visual_task(self):
        name = self.visual_task_name.get()
        if not name or not hasattr(self, 'last_trigger_img') or not self.recorded_events:
            messagebox.showwarning("警告", "请确保填写名称、截取图像并录制动作")
            return
        
        img_path = os.path.join(self.tasks_dir, f"{name}_trigger.png")
        self.last_trigger_img.save(img_path)
        
        task = {
            "task_name": name,
            "trigger_img": img_path,
            "sequence": self.recorded_events,
            "threshold": 0.95
        }
        
        with open(os.path.join(self.tasks_dir, f"{name}.vtask"), "w") as f:
            json.dump(task, f)
        self.refresh_visual_list()
        messagebox.showinfo("成功", "视觉任务已保存")

    def save_macro(self):
        name = self.macro_name.get()
        if not name or not self.recorded_events:
            messagebox.showwarning("警告", "请填写宏名称并录制动作")
            return
        
        path = os.path.join(self.tasks_dir, f"{name}.macro")
        with open(path, "w") as f:
            json.dump(self.recorded_events, f)
        self.refresh_macro_list()
        messagebox.showinfo("成功", "宏录制已保存")

    # --- Playback Engine ---
    def play_macro(self):
        selection = self.macro_list.curselection()
        if not selection: return
        filename = self.macro_list.get(selection[0])
        path = os.path.join(self.tasks_dir, filename)
        
        with open(path, "r") as f:
            macro = json.load(f)
            
        try:
            loops = int(self.loop_count.get())
        except: loops = 1
        
        self.stop_event.clear()
        threading.Thread(target=self.playback_loop, args=(macro, loops), daemon=True).start()

    def playback_loop(self, macro, loops=1):
        count = 0
        while (loops == 0 or count < loops) and not self.stop_event.is_set():
            start_play_time = time.perf_counter()
            for event in macro:
                if self.stop_event.is_set(): break
                
                # Precise Timing
                target_time = event["time"]
                while (time.perf_counter() - start_play_time) < target_time:
                    if self.stop_event.is_set(): break
                    time.sleep(0.001)
                
                if self.stop_event.is_set(): break
                self.execute_event(event)
            
            count += 1
            if loops != 1: print(f"循环完成: {count}/{loops if loops > 0 else '∞'}")
            time.sleep(0.1)

    def execute_event(self, event):
        try:
            if event["type"] == "mouse_click":
                btn = event["button"]
                if event["pressed"]:
                    pyautogui.mouseDown(event["x"], event["y"], button=btn)
                else:
                    pyautogui.mouseUp(event["x"], event["y"], button=btn)
            
            elif event["type"] == "mouse_scroll":
                # pyautogui scroll is different, pynput gives dx, dy
                pyautogui.scroll(event["dy"] * 100, x=event["x"], y=event["y"])
            
            elif event["type"] == "key_event":
                key = event["key"]
                if "Key." in key: key = key.replace("Key.", "")
                
                if event["action"] == "press":
                    pyautogui.keyDown(key)
                else:
                    pyautogui.keyUp(key)
        except Exception as e:
            print(f"执行事件失败: {e}")

    # --- Clicker Engine ---
    def toggle_clicker(self):
        if not self.clicker_active:
            self.clicker_active = True
            self.stop_event.clear()
            self.btn_toggle_clicker.configure(text="停止点击器", fg_color="#c0392b")
            threading.Thread(target=self.enhanced_clicker_loop, daemon=True).start()
        else:
            self.clicker_active = False
            self.btn_toggle_clicker.configure(text="启动点击器", fg_color="#3b8ed0")

    def enhanced_clicker_loop(self):
        import random
        try:
            base_freq = int(self.click_freq.get()) / 1000.0
            rand_offset = int(self.click_random.get()) / 1000.0
            hold_time = int(self.click_hold.get()) / 1000.0
        except:
            base_freq, rand_offset, hold_time = 0.1, 0, 0.01
            
        btn_map = {"左键 (Left)": "left", "右键 (Right)": "right", "中键 (Middle)": "middle"}
        btn = btn_map.get(self.click_button.get(), "left")
        
        type_map = {"单次点击": 1, "双击": 2, "三击": 3}
        clicks = type_map.get(self.click_type.get(), 1)
        
        while self.clicker_active and not self.stop_event.is_set():
            for _ in range(clicks):
                pyautogui.mouseDown(button=btn)
                time.sleep(hold_time)
                pyautogui.mouseUp(button=btn)
                if clicks > 1: time.sleep(0.05) # Small gap for multi-clicks
            
            # Wait for next interval
            wait = base_freq + random.uniform(-rand_offset, rand_offset)
            time.sleep(max(0.001, wait))

    # --- Monitoring Engine ---
    def toggle_monitoring(self):
        if not self.monitoring_active:
            self.monitoring_active = True
            self.stop_event.clear()
            self.btn_monitor.configure(text="停止监控", fg_color="#c0392b")
            threading.Thread(target=self.monitor_loop, daemon=True).start()
        else:
            self.monitoring_active = False
            self.btn_monitor.configure(text="开始监控屏幕", fg_color="#27ae60")

    def monitor_loop(self):
        while self.monitoring_active and not self.stop_event.is_set():
            tasks = []
            if os.path.exists(self.tasks_dir):
                for f in os.listdir(self.tasks_dir):
                    if f.endswith(".vtask"):
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
                
                if max_val >= task.get("threshold", 0.95):
                    print(f"视觉匹配成功: {task['task_name']}")
                    self.playback_loop(task["sequence"], loops=1)
                    time.sleep(2) # Cooldown
            time.sleep(0.2)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = YaoMouseToolbox()
    app.run()
