#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

# Author: funchan
# CreateDate: 2022-01-26 23:20:06
# Description: 计时器

import platform
import time
from tkinter import Widget
from typing import List, Union

import simpleaudio as sa
from dirs import *
from gui import CustomWindow
from pynput import keyboard, mouse
from ttkbootstrap import *
from ttkbootstrap.constants import *

start_time = 0


class App(CustomWindow):
    def __init__(
        self,
        title="ttkbootstrap",
        version="0.0.1",
        base_size=5,
        themename="litera",
        iconphoto="",
        size=None,
        position=None,
        minsize=None,
        maxsize=None,
        resizable=None,
        hdpi=True,
        scaling=None,
        transient=None,
        overrideredirect=False,
        alpha=1,
    ):
        super().__init__(
            title,
            version,
            base_size,
            themename,
            iconphoto,
            size,
            position,
            minsize,
            maxsize,
            resizable,
            hdpi,
            scaling,
            transient,
            overrideredirect,
            alpha,
        )

        self.top_center()
        self.wm_attributes("-topmost", True)

        self.bind_mouse()
        self.bind_key()
        self.time_text_label.bind("<ButtonPress-1>", self.start_move)
        self.time_text_label.bind("<ButtonRelease-1>", self.stop_move)
        self.time_text_label.bind("<B1-Motion>", self.on_motion)
        self.bind("<Escape>", lambda e: self.quit())
        package_list = ["Nuitka", "simpleaudio", "pynput", "ttkbootstrap"]
        self.bind("<F1>", lambda e: self.show_about(package_list, layout_base=self))

        self.after(100, self.update_state)
        self.signal = "ready"

    def add_widget(self):
        self.time_text_var = StringVar()
        self.time_text_var.set("00:00")
        self.time_number_var = IntVar()
        self.time_number_var.set(5)
        self.play_sound_var = BooleanVar()
        self.play_sound_var.set(False)
        self.count_down_var = BooleanVar()
        self.count_down_var.set(True)

        self.time_text_label = Label(
            self,
            textvariable=self.time_text_var,
            font=f'"{font.nametofont("TkDefaultFont")["family"]}" {int(3.5 * self.base_size)} bold',
            width=self.base_size,
            anchor=CENTER,
        )

        self.time_number_scale = Scale(
            self, from_=1, to=60, variable=self.time_number_var
        )
        self.count_down_checkbutton = Checkbutton(
            self, text="CD", variable=self.count_down_var
        )
        self.play_sound_checkbutton = Checkbutton(
            self, text="Sound", variable=self.play_sound_var
        )
        self.start_button = Button(self, text="Start[F5]", width=7, command=self.start)
        self.exit_button = Button(
            self, text="Exit[ESC]", command=self.quit, width=7, bootstyle=DANGER
        )

        self.widgets_list = [
            [self.time_text_label, "-"],
            [self.time_number_scale, "-"],
            [self.count_down_checkbutton, self.play_sound_checkbutton],
            [self.start_button, self.exit_button],
        ]

        self.grid_widget(
            self.widgets_list,
            self,
            (self.base_size, self.base_size, self.base_size, self.base_size // 2),
        )

    def top_center(self) -> None:
        self.withdraw()
        self.update()
        w_width = self.winfo_width()
        s_width = self.winfo_screenwidth()
        pos_x = (s_width - w_width) // 2
        pos_y = 0
        self.geometry(f"+{pos_x}+{pos_y}")
        self.deiconify()

    @CustomWindow.multi_thread()
    def bind_mouse(self):
        def on_move(x, y):
            if (
                self.winfo_x() <= x <= self.winfo_x() + self.winfo_width()
                and self.winfo_y() <= y <= self.winfo_y() + self.winfo_height()
            ):
                self.show_widget(self.winfo_children()[1:])
            else:
                self.hide_widget(self.winfo_children()[1:])

        def on_click(x, y, button, is_press):
            pass

        def on_scroll(x, y, dx, dy):
            pass

        with mouse.Listener(
            on_move=on_move, on_click=on_click, on_scroll=on_scroll
        ) as listener:
            listener.join()

    @CustomWindow.multi_thread()
    def bind_key(self):
        def on_press(key):
            global start_time

            if self.enable:
                if key == keyboard.Key.alt:
                    start_time = time.time()
                if key == keyboard.Key.f4 and time.time() - start_time < 0.5:
                    self.quit()

        def on_release(key):
            if key == keyboard.Key.f5:
                self.start()
            if key == keyboard.Key.f6:
                self._reset()

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def enable_widget(self, _widgets: Union[Widget, List[Widget]]):
        self.enable = True
        return super().enable_widget(_widgets)

    def disable_widget(self, _widgets: Union[Widget, List[Widget]]):
        self.enable = False
        return super().disable_widget(_widgets)

    def start_move(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def stop_move(self, event):
        self.start_x = None
        self.start_y = None

    def on_motion(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        x = max(self.winfo_x() + dx, 0)
        y = max(self.winfo_y() + dy, 0)
        w_width = self.winfo_width()
        w_height = self.winfo_width()
        s_width = self.winfo_screenwidth()
        s_height = self.winfo_screenheight()
        x = min(x, s_width - w_width)
        y = min(y, int(s_height - w_height - utility.scale_size(self, 50)))
        self.geometry(f"+{x}+{y}")

    @CustomWindow.multi_thread()
    def update_state(self):
        widget_list = [
            self.time_number_scale,
            self.count_down_checkbutton,
            self.play_sound_checkbutton,
        ]
        if self.signal == "ready":
            minutes = self.time_number_var.get()
            self.time_text_var.set(f"{str(minutes).zfill(2)}:00")
            self.total_count = self.time_number_var.get() * 60
            self.start_count = 0
            self.enable_widget(widget_list)
            self.exit_button.config(
                text="Exit[ESC]", command=self.quit, width=7, bootstyle=DANGER
            )
        else:
            self.disable_widget(widget_list)
            self.exit_button.config(
                text="Reset[F6]", command=self._reset, width=7, bootstyle=SUCCESS
            )

        self.after(100, self.update_state)

    def start(self):
        if self.signal == "start":
            self.signal = "pause"
            self.start_button.config(text="Start[F5]", bootstyle=(DEFAULT, OUTLINE))
            self._pause()
        else:
            self.signal = "start"
            self.start_button.config(text="Pause[F5]", bootstyle=(WARNING, OUTLINE))
            self._start()

    @staticmethod
    @CustomWindow.multi_thread()
    def beep():
        wave_path = str(res_dir / "second.wav")
        wave_obj = sa.WaveObject.from_wave_file(wave_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    def _start(self):
        if self.count_down_var.get():
            if self.total_count >= 0:
                self._countdown()
            else:
                self.after(2000, self._reset)

        elif self.start_count <= self.total_count:
            self._count()
        else:
            self.after(2000, self._reset)

    def _countdown(self):
        mm = self.total_count // 60
        ss = self.total_count - mm * 60
        self.total_count -= 1
        self.time_text_var.set(f"{mm:02d}:{ss:02d}")

        count_down = self.total_count
        if count_down < 10:
            if count_down % 2:
                self.time_text_label.config(bootstyle=DANGER)
            else:
                self.time_text_label.config(bootstyle=DEFAULT)

            if self.play_sound_var.get():
                self.beep()

        self.after_id = self.after(1000, self._start)

    def _count(self):
        mm = self.start_count // 60
        ss = self.start_count - mm * 60
        self.start_count += 1
        self.time_text_var.set(f"{mm:02d}:{ss:02d}")

        count_down = self.total_count - self.start_count
        if count_down < 10:
            if count_down % 2:
                self.time_text_label.config(bootstyle=DANGER)
            else:
                self.time_text_label.config(bootstyle=DEFAULT)

            if self.play_sound_var.get():
                self.beep()

        self.after_id = self.after(1000, self._start)

    def _pause(self):
        self.after_cancel(self.after_id)

    def _reset(self):
        self.after_cancel(self.after_id)
        self.signal = "ready"
        self.time_text_label.config(bootstyle=DEFAULT)
        self.start_button.config(text="Start[F5]", bootstyle=DEFAULT)


def main():
    if platform.system() == "Windows":
        iconphoto = res_dir / "main_32.png"
    else:
        iconphoto = res_dir / "main_256.png"

    app = App(
        title="StopWatch", version="0.1.0", iconphoto=iconphoto, overrideredirect=True
    )
    app.mainloop()


if __name__ == "__main__":
    main()
