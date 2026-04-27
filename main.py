import json
import random
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window

# กำหนดฟอนต์ไทย (เปลี่ยนชื่อไฟล์ตามที่คุณมี)
FONT_NAME = "tahoma.ttf" 

Builder.load_string(f"""
<MainMenu>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        canvas.before:
            Color:
                rgba: 0.94, 0.95, 0.96, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        BoxLayout:
            id: logo_container
            size_hint_y: None
            height: 100
            padding: 10

        Label:
            text: "Datadog Exam Simulator"
            font_size: '26sp'
            bold: True
            color: 0.39, 0.17, 0.65, 1
            font_name: '{FONT_NAME}'
            size_hint_y: None
            height: 50
        
        ScrollView:
            BoxLayout:
                id: menu_buttons
                orientation: 'vertical'
                spacing: 10
                size_hint_y: None
                height: self.minimum_height

        Label:
            text: "Developed by NTT Thailand Limited 2026"
            font_size: '12sp'
            color: 0.6, 0.6, 0.6, 1
            size_hint_y: None
            height: 40

<QuizScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0.94, 0.95, 0.96, 1
            Rectangle:
                pos: self.pos
                size: self.size

        # Header
        BoxLayout:
            size_hint_y: None
            height: 60
            padding: 10
            canvas.before:
                Color:
                    rgba: 0.39, 0.17, 0.65, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                id: lbl_score
                text: ""
                bold: True
                font_name: '{FONT_NAME}'
            Label:
                id: lbl_timer
                text: ""
                color: 1, 0.8, 0, 1
                bold: True

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                padding: 20
                spacing: 20
                size_hint_y: None
                height: self.minimum_height
                
                Label:
                    id: lbl_q
                    text: ""
                    color: 0, 0, 0, 1
                    font_size: '18sp'
                    font_name: '{FONT_NAME}'
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None

                BoxLayout:
                    id: choices_container
                    orientation: 'vertical'
                    spacing: 10
                    size_hint_y: None
                    height: self.minimum_height

                Label:
                    id: lbl_explain
                    text: ""
                    color: 0.2, 0.2, 0.2, 1
                    font_name: '{FONT_NAME}'
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None

        Button:
            id: btn_submit
            text: "Submit"
            size_hint_y: None
            height: 70
            font_name: '{FONT_NAME}'
            background_normal: ''
            background_color: 0.42, 0.35, 0.88, 1
            on_release: root.on_submit_click()
""")

class MainMenu(Screen):
    def on_enter(self):
        self.setup_ui()

    def setup_ui(self):
        self.ids.menu_buttons.clear_widgets()
        # Resume Logic (v7.3)
        if os.path.exists("save_data.json"):
            btn = Button(text="🔄 Resume Last Session", size_hint_y=None, height=70, 
                         background_color=get_color_from_hex("#e67e22"), font_name=FONT_NAME)
            btn.bind(on_release=self.resume_progress)
            self.ids.menu_buttons.add_widget(btn)

        modes = [("1. Fundamentals", "founda", "#6a5acd"), ("2. Log Management", "log", "#5e2a9b"), 
                 ("3. APM & Tracing", "apm", "#2ecc71"), ("4. Cloud SIEM", "cloud", "#3498db")]
        
        for text, m, color in modes:
            btn = Button(text=text, size_hint_y=None, height=65, 
                         background_color=get_color_from_hex(color), font_name=FONT_NAME)
            btn.bind(on_release=lambda x, mode=m: self.start_quiz(mode))
            self.ids.menu_buttons.add_widget(btn)

    def start_quiz(self, mode):
        app = App.get_running_app()
        app.quiz_config = {"mode": mode, "is_resume": False}
        self.manager.current = 'quiz'

    def resume_progress(self, instance):
        app = App.get_running_app()
        app.quiz_config = {"is_resume": True}
        self.manager.current = 'quiz'

class QuizScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        config = app.quiz_config
        if config.get("is_resume"):
            self.resume_logic()
        else:
            self.start_logic(config["mode"])

    def start_logic(self, mode):
        # Logic การโหลดไฟล์และการสุ่ม (ยกมาจากโค้ดคุณ)
        file_map = {"founda": "funda_pool.json", "log": "log_pool.json", "apm": "apm_pool.json", "cloud": "cloud_pool.json"}
        with open(file_map[mode], 'r', encoding='utf-8') as f:
            self.pool = json.load(f)
        self.questions = random.sample(self.pool, min(len(self.pool), 75))
        self.current_q = 0
        self.score = 0
        self.wrong_questions = []
        self.category_mistakes = {}
        self.load_q()

    def load_q(self):
        q_data = self.questions[self.current_q]
        # Shuffle Logic ของคุณ
        if 'shuffled_options' not in q_data:
            opts = list(q_data['options'])
            random.shuffle(opts)
            q_data['shuffled_options'] = opts
        
        self.ids.lbl_q.text = f"Question {self.current_q+1}\n\n{q_data['q']}"
        self.ids.choices_container.clear_widgets()
        self.ids.lbl_explain.text = ""
        self.ids.btn_submit.text = "Submit"
        self.ids.btn_submit.background_color = get_color_from_hex("#6a5acd")
        
        self.check_boxes = []
        for opt in q_data['shuffled_options']:
            box = BoxLayout(size_hint_y=None, height=50)
            chk = CheckBox(size_hint_x=None, width=50, group='c' if len(q_data.get('answer', []))==1 else None)
            lbl = Label(text=opt, color=(0,0,0,1), font_name=FONT_NAME, text_size=(Window.width-100, None))
            box.add_widget(chk); box.add_widget(lbl)
            self.ids.choices_container.add_widget(box)
            self.check_boxes.append(chk)

    def on_submit_click(self):
        if "Next" in self.ids.btn_submit.text:
            self.current_q += 1
            if self.current_q < len(self.questions): self.load_q()
            else: self.manager.current = 'menu' # หรือไปหน้าสรุป
        else:
            self.check_answer()

    def check_answer(self):
        # Logic ตรวจคะแนนและ Save Progress (v7.3) ยกมาจากที่คุณส่งมา
        self.ids.btn_submit.text = "Next Question ➔"
        self.ids.btn_submit.background_color = get_color_from_hex("#28a745")
        # บันทึกความคืบหน้า
        self.save_progress()

    def save_progress(self):
        data = {"current_q": self.current_q, "score": self.score, "questions": self.questions}
        with open("save_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

class DatadogApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(QuizScreen(name='quiz'))
        return sm

if __name__ == '__main__':
    DatadogApp().run()
