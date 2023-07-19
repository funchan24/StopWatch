#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

import contextlib
import functools
import itertools
import webbrowser
from threading import Thread
from tkinter import TclError, Widget
from typing import Callable, List, Optional, Tuple, Union

from pkg_resources import parse_version
from ttkbootstrap import *
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import MessageDialog
from ttkbootstrap.icons import Icon
from ttkbootstrap.localization import MessageCatalog
from ttkbootstrap.scrolled import ScrolledFrame


class CenterMessageDialog(MessageDialog):
    """A simple modal dialog class that can be used to build simple
    message dialogs.

    Displays a message and a set of buttons. Each of the buttons in the
    message window is identified by a unique symbolic name. After the
    message window is popped up, the message box awaits for the user to
    select one of the buttons. Then it returns the symbolic name of the
    selected button. Use a `Toplevel` widget for more advanced modal
    dialog designs.
    """

    def get_center_point(
        self,
        _window: Union[Window, Toplevel],
        base_window: Union[Window, Toplevel, None],
    ):
        """Get the coordinates for display in the center"""
        _window.update_idletasks()
        w_width = _window.winfo_width()
        w_height = _window.winfo_height()
        if base_window:
            b_x = base_window.winfo_x()
            b_y = base_window.winfo_y()
            b_width = base_window.winfo_width()
            b_height = base_window.winfo_height()
            x = b_x + (b_width - w_width) // 2
            y = b_y + int((b_height - w_height) * 0.382)
        else:
            s_width = self.winfo_screenwidth()
            s_height = self.winfo_screenheight()
            x = (s_width - w_width) // 2
            y = int((s_height - w_height) * 0.382)

        return max(x, 0), max(y, 0)

    def center_show(self, base_window: Union[Window, Toplevel]):
        """Show the popup dialog"""

        self._result = None
        self.build()

        self._toplevel.update_idletasks()
        x, y = self.get_center_point(self._toplevel, base_window)
        try:
            self._toplevel.geometry(f"+{x}+{y}")
        except Exception:
            master = self._toplevel.master if self._parent is None else self._parent
            x = master.winfo_rootx()
            y = master.winfo_rooty()
            self._toplevel.geometry(f"+{x}+{y}")

        self._toplevel.deiconify()
        if self._alert:
            self._toplevel.bell()

        if self._initial_focus:
            self._initial_focus.focus_force()

        self._toplevel.grab_set()
        self._toplevel.wait_window()


class CenterMessagebox:
    """This class contains various static methods that show popups with
    a message to the end user with various arrangments of buttons
    and alert options, Will appear in the center of the base_window"""

    @staticmethod
    def show_info(message, base_window, title=" ", parent=None, alert=False, **kwargs):
        """Display a modal dialog box with an OK button and an INFO
        icon.

        Parameters:

            message (str):
                A message to display in the message box.

            base_window (Union[Window, Toplevel]):
                Make the message box appear in the center of the base_window

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            alert (bool):
                Specified whether to ring the display bell.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        dialog = CenterMessageDialog(
            message=message,
            title=title,
            alert=alert,
            parent=parent,
            buttons=["OK:primary"],
            icon=Icon.info,
            localize=True,
            **kwargs,
        )

        dialog.center_show(base_window)

    @staticmethod
    def show_warning(
        message, base_window, title=" ", parent=None, alert=True, **kwargs
    ):
        """Display a modal dialog box with an OK button and a
        warning icon. Will ring the display bell.

        Parameters:

            message (str):
                A message to display in the message box.

            base_window (Union[Window, Toplevel]):
                Make the message box appear in the center of the base_window

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            alert (bool):
                Specified whether to ring the display bell.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        dialog = CenterMessageDialog(
            message=message,
            title=title,
            parent=parent,
            buttons=["OK:primary"],
            icon=Icon.warning,
            alert=alert,
            localize=True,
            **kwargs,
        )

        dialog.center_show(base_window)

    @staticmethod
    def show_error(message, base_window, title=" ", parent=None, alert=True, **kwargs):
        """Display a modal dialog box with an OK button and an
        error icon. Will ring the display bell.

        Parameters:

            message (str):
                A message to display in the message box.

            base_window (Union[Window, Toplevel]):
                Make the message box appear in the center of the base_window

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            alert (bool):
                Specified whether to ring the display bell.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        dialog = CenterMessageDialog(
            message=message,
            title=title,
            parent=parent,
            buttons=["OK:primary"],
            icon=Icon.error,
            alert=alert,
            localize=True,
            **kwargs,
        )

        dialog.center_show(base_window)

    @staticmethod
    def show_question(
        message, base_window, title=" ", parent=None, buttons=None, alert=True, **kwargs
    ):
        """Display a modal dialog box with yes, no buttons and a
        question icon. Will ring the display bell. You may also
        change the button scheme using the `buttons` parameter.

        Parameters:

            message (str):
                A message to display in the message box.

            base_window (Union[Window, Toplevel]):
                Make the message box appear in the center of the base_window

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            buttons (List[str]):
                A list of buttons to appear at the bottom of the popup
                messagebox. The buttons can be a list of strings which
                will define the symbolic name and the button text.
                `['OK', 'Cancel']`. Alternatively, you can assign a
                bootstyle to each button by using the colon to separate the
                button text and the bootstyle. If no colon is found, then
                the style is set to 'primary' by default.
                `['Yes:success','No:danger']`.

            alert (bool):
                Specified whether to ring the display bell.

            **kwargs (Dict):
                Other optional keyword arguments.

        Returns:

            Union[str, None]:
                The symbolic name of the button pressed, or None if the
                window is closed without pressing a button.
        """
        if buttons is None:
            buttons = ["No:secondary", "Yes:primary"]
        dialog = CenterMessageDialog(
            message=message,
            title=title,
            parent=parent,
            buttons=buttons,
            icon=Icon.question,
            alert=alert,
            localize=True,
            **kwargs,
        )

        dialog.center_show(base_window)
        return dialog.result

    @staticmethod
    def ok(message, base_window, title=" ", alert=False, parent=None, **kwargs):
        """Display a modal dialog box with an OK button and optional
        bell alert.

        Parameters:

            message (str):
                A message to display in the message box.

            base_window (Union[Window, Toplevel]):
                Make the message box appear in the center of the base_window

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            alert (bool):
                Specified whether to ring the display bell.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            **kwargs (Dict):
                Other optional keyword arguments.
        """
        dialog = CenterMessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            buttons=["OK:primary"],
            localize=True,
            **kwargs,
        )

        dialog.center_show(base_window)

    @staticmethod
    def okcancel(message, base_window, title=" ", alert=False, parent=None, **kwargs):
        """Displays a modal dialog box with OK and Cancel buttons and
        return the symbolic name of the button pressed.

        Parameters:

            message (str):
                A message to display in the message box.

            base_window (Union[Window, Toplevel]):
                Make the message box appear in the center of the base_window

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            alert (bool):
                Specified whether to ring the display bell.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            **kwargs (Dict):
                Other optional keyword arguments.

        Returns:

            Union[str, None]:
                The symbolic name of the button pressed, or None if the
                window is closed without pressing a button.
        """
        dialog = CenterMessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            localize=True,
            **kwargs,
        )

        dialog.center_show(base_window)
        return dialog.result

    @staticmethod
    def yesno(message, base_window, title=" ", alert=False, parent=None, **kwargs):
        """Display a modal dialog box with YES and NO buttons and return
        the symbolic name of the button pressed.

        Parameters:

            message (str):
                A message to display in the message box.

            base_window (Union[Window, Toplevel]):
                Make the message box appear in the center of the base_window

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            alert (bool):
                Specified whether to ring the display bell.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            **kwargs (Dict):
                Other optional keyword arguments.

        Returns:

            Union[str, None]:
                The symbolic name of the button pressed, or None if the
                window is closed without pressing a button.
        """
        dialog = CenterMessageDialog(
            title=title,
            message=message,
            parent=parent,
            buttons=["No", "Yes:primary"],
            alert=alert,
            localize=True,
            **kwargs,
        )

        dialog.center_show(base_window)
        return dialog.result

    @staticmethod
    def yesnocancel(
        message, base_window, title=" ", alert=False, parent=None, **kwargs
    ):
        """Display a modal dialog box with YES, NO, and Cancel buttons,
        and return the symbolic name of the button pressed.

        Parameters:

            message (str):
                A message to display in the message box.

            base_window (Union[Window, Toplevel]):
                Make the message box appear in the center of the base_window

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            alert (bool):
                Specified whether to ring the display bell.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            **kwargs (Dict):
                Optional keyword arguments.

        Returns:

            Union[str, None]:
                The symbolic name of the button pressed, or None if the
                window is closed without pressing a button.
        """
        dialog = CenterMessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            buttons=["Cancel", "No", "Yes:primary"],
            localize=True,
            **kwargs,
        )

        dialog.center_show(base_window)
        return dialog.result

    @staticmethod
    def retrycancel(
        message, base_window, title=" ", alert=False, parent=None, **kwargs
    ):
        """Display a modal dialog box with RETRY and Cancel buttons;
        returns the symbolic name of the button pressed.

        Parameters:

            message (str):
                A message to display in the message box.

            base_window (Union[Window, Toplevel]):
                Make the message box appear in the center of the base_window

            title (str):
                The string displayed as the title of the messagebox. This
                option is ignored on Mac OS X, where platform guidelines
                forbid the use of a title on this kind of dialog.

            alert (bool):
                Specified whether to ring the display bell.

            parent (Union[Window, Toplevel]):
                Makes the window the logical parent of the message box. The
                message box is displayed on top of its parent window.

            **kwargs (Dict):
                Other optional keyword arguments.

        Returns:

            Union[str, None]:
                The symbolic name of the button pressed, or None if the
                window is closed without pressing a button.
        """
        dialog = CenterMessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            buttons=["Cancel", "Retry:primary"],
            localize=True,
            **kwargs,
        )

        dialog.center_show(base_window)
        return dialog.result


class CustomWindow(Window):
    """A class that wraps the tkinter.Tk class in order to provide a
    more convenient api with additional bells and whistles"""

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
        alpha=1.0,
    ):
        """
        Parameters:

            title (str):
                The title that appears on the application titlebar.

            version (str):
                The version of the application.

            base_size (int):
                The base spacing between widgets.

            themename (str):
                The name of the ttkbootstrap theme to apply to the
                application.

            iconphoto (str):
                A path to the image used for the titlebar icon.
                Internally this is passed to the `Tk.iconphoto` method
                and the image will be the default icon for all windows.
                A ttkbootstrap image is used by default. To disable
                this default behavior, set the __value to `None` and use
                the `Tk.iconphoto` or `Tk.iconbitmap` methods directly.

            size (Tuple[int, int]):
                The width and height of the application window.
                Internally, this argument is passed to the
                `Window.geometry` method.

            position (Tuple[int, int]):
                The horizontal and vertical position of the window on
                the screen relative to the top-left coordinate.
                Internally this is passed to the `Window.geometry`
                method.

            minsize (Tuple[int, int]):
                Specifies the minimum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Window.minsize` method.

            maxsize (Tuple[int, int]):
                Specifies the maximum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Window.maxsize` method.

            resizable (Tuple[bool, bool]):
                Specifies whether the user may interactively resize the
                toplevel window. Must pass in two arguments that specify
                this flag for _horizontal_ and _vertical_ dimensions.
                This can be adjusted after the window is created by using
                the `Window.resizable` method.

            hdpi (bool):
                Enable high-dpi support for Windows OS. This option is
                enabled by default.

            scaling (float):
                Sets the current scaling factor used by Tk to convert
                between physical units (for example, points, inches, or
                millimeters) and pixels. The number argument is a
                floating point number that specifies the number of pixels
                per point on window's display.

            transient (Union[Tk, Widget]):
                Instructs the window manager that this widget is
                transient with regard to the widget master. Internally
                this is passed to the `Window.transient` method.

            overrideredirect (bool):
                Instructs the window manager to ignore this widget if
                True. Internally, this argument is passed to the
                `Window.overrideredirect(1)` method.

            alpha (float):
                On Windows, specifies the alpha transparency level of the
                toplevel. Where not supported, alpha remains at 1.0. Internally,
                this is processed as `Toplevel.attributes('-alpha', alpha)`.
        """

        super().__init__(
            title,
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
        self.withdraw()
        self.version = parse_version(version)
        self.base_size = utility.scale_size(self, base_size)
        self.has_update = None

        self.set_global_font(size=10)
        MessageCatalog.locale("zh_cn")
        self.add_widget()

        if position is None:
            self.center_horizontally(self)
        self.deiconify()

    @staticmethod
    def set_global_font(**font_options):
        default_font = font.nametofont("TkDefaultFont")
        text_font = font.nametofont("TkTextFont")
        fixed_font = font.nametofont("TkFixedFont")
        fonts = (default_font, text_font, fixed_font)

        for k, v in font_options.items():
            for _font in fonts:
                _font[k] = v

    @staticmethod
    def multi_thread(thread_name: Optional[str] = None):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                thread = Thread(target=func, args=args, kwargs=kwargs)
                thread.name = thread_name or wrapper.__name__
                thread.daemon = True
                thread.start()
                return thread

            return wrapper

        return decorator

    def get_center_point(
        self,
        _window: Union[Window, Toplevel],
        base_window: Union[Window, Toplevel, None],
    ):
        _window.update_idletasks()
        w_width = _window.winfo_width()
        w_height = _window.winfo_height()
        if base_window:
            b_x = base_window.winfo_x()
            b_y = base_window.winfo_y()
            b_width = base_window.winfo_width()
            b_height = base_window.winfo_height()
            x = b_x + (b_width - w_width) // 2
            y = b_y + int((b_height - w_height) * 0.382)
        else:
            s_width = self.winfo_screenwidth()
            s_height = self.winfo_screenheight()
            x = (s_width - w_width) // 2
            y = int((s_height - w_height) * 0.382)

        return max(x, 0), max(y, 0)

    def center_horizontally(
        self,
        _window: Union[Window, Toplevel],
        base_window: Union[Window, Toplevel, None] = None,
    ):
        x, y = self.get_center_point(_window, base_window)
        _window.geometry(f"+{x}+{y}")

    def add_widget(self):
        """
        - means columnspan
        n int means a blank Label, width = n
        """
        menu = Menu(self)
        package_list = ["ttkbootstrap"]
        menu.add_command(
            label="关于", command=lambda: self.show_about(package_list, layout_base=self)
        )
        self.config(menu=menu)

        widgets_list = [[1] * 9 for _ in range(9)]
        for i, j in itertools.product(range(9), range(9)):
            if i >= j:
                widgets_list[i][j] = Label(
                    self,
                    text=f"{j + 1}*{i + 1}={(i + 1) * (j + 1)}",
                    anchor=CENTER,
                    bootstyle=(SUCCESS, INVERSE),
                )

        self.grid_widget(widgets_list, self, self.base_size)

    @staticmethod
    def grid_widget(
        widgets_list: List[List[Union[Widget, str, int]]],
        master: Union[Window, Toplevel],
        padding: Union[int, Tuple[int, int, int, int]] = 0,
        anchor: ANCHOR = CENTER,
        sticky=NSEW,
    ):
        master.grid_anchor(anchor)
        max_column = len(widgets_list[0])
        assert all(
            len(_widgets) == max_column for _widgets in widgets_list
        ), "the elements of each row are not equal"

        if isinstance(padding, int):
            padx = pady = ipadx = ipady = padding
        elif isinstance(padding, tuple):
            padx, pady, ipadx, ipady = padding
        else:
            raise TypeError("wrong parameter type")

        for row, _widgets in enumerate(widgets_list):
            for column, widget in enumerate(_widgets):
                if widget != "-":
                    columnspan = 1
                    for i in range(column + 1, max_column):
                        if _widgets[i] != "-":
                            break
                        columnspan += 1

                    if isinstance(widget, int):
                        widget = Label(master, width=widget)

                    try:
                        widget.grid(
                            row=row,
                            column=column,
                            columnspan=columnspan,
                            padx=padx,
                            pady=pady,
                            ipadx=ipadx,
                            ipady=ipady,
                            sticky=sticky,
                        )
                    except AttributeError as e:
                        raise AttributeError(
                            f"""self.widgets_list can only contain "widget", "-" and int, got a "{widget}"."""
                        ) from e

    def disable_widget(self, _widgets: Union[Widget, List[Widget]]):
        widget_list = _widgets if isinstance(_widgets, list) else [_widgets]
        for w in widget_list:
            if w.winfo_children():
                self.disable_widget(w.winfo_children())
            else:
                with contextlib.suppress(AttributeError, TclError):
                    w.config(state=DISABLED)

    def enable_widget(self, _widgets: Union[Widget, List[Widget]]):
        widget_list = _widgets if isinstance(_widgets, list) else [_widgets]
        for w in widget_list:
            if w.winfo_children():
                self.enable_widget(w.winfo_children())
            else:
                with contextlib.suppress(AttributeError, TclError):
                    w.config(state=NORMAL)

    @staticmethod
    def hide_widget(_widgets: Union[Widget, List[Widget]]):
        widget_list = _widgets if isinstance(_widgets, list) else [_widgets]
        for w in widget_list:
            with contextlib.suppress(AttributeError, TclError):
                w.grid_remove()

    @staticmethod
    def show_widget(_widgets: Union[Widget, List[Widget]]):
        widget_list = _widgets if isinstance(_widgets, list) else [_widgets]
        for w in widget_list:
            with contextlib.suppress(AttributeError, TclError):
                w.grid()

    def show_progress(
        self,
        mode="indeterminate",
        interval=50,
        step=1.0,
        show_cancel_button=False,
        cancel_function: Optional[Callable] = None,
    ):
        """mode: Literal['determinate', 'indeterminate']"""
        self.progress_toplevel = Toplevel(overrideredirect=True, topmost=True)
        self.progress_toplevel.withdraw()
        self.progress_toplevel.grab_set()

        self.progress_var = IntVar(value=0)
        progress_progressbar = Progressbar(
            self.progress_toplevel,
            mode=mode,
            variable=self.progress_var,
            length=25 * self.base_size,
        )
        if show_cancel_button:
            cancel_button = Button(
                self.progress_toplevel,
                text=MessageCatalog.translate("cancel"),
                command=cancel_function,
            )
            self.grid_widget(
                [[progress_progressbar, cancel_button]],
                self.progress_toplevel,
                (0, 0, 0, self.base_size),
            )
        else:
            self.grid_widget(
                [[progress_progressbar]],
                self.progress_toplevel,
                (0, 0, 0, 2 * self.base_size),
            )

        self.center_horizontally(self.progress_toplevel, self)
        self.progress_toplevel.deiconify()

        if mode == "indeterminate":
            progress_progressbar.step(step)
            progress_progressbar.start(interval)

    def show_about(
        self,
        package_list: List[str],
        show_donate_image: bool = True,
        donate_qr_title: str = "微信扫码赞赏作者",
        show_update: bool = True,
        layout_base=None,
    ):
        package_list.sort(key=lambda x: x.lower())

        self.about_toplevel = Toplevel(
            title="", resizable=(False, False), transient=self
        )
        self.about_toplevel.withdraw()
        self.about_toplevel.grab_set()
        self.about_toplevel.bind("<Escape>", lambda e: self.about_toplevel.destroy())

        about_frame = ScrolledFrame(
            self.about_toplevel,
            autohide=True,
            width=55 * self.base_size,
            height=50 * self.base_size,
        )
        package_labels = [
            [Label(about_frame, text=i, anchor=CENTER, bootstyle=PRIMARY)]
            for i in package_list
        ]

        font_family = font.nametofont("TkDefaultFont").cget("family")
        widgets_list = [
            [
                Label(
                    about_frame,
                    text=f"{self.title()} v{self.version}",
                    font=f'"{font_family}" 12',
                    anchor=CENTER,
                    bootstyle=PRIMARY,
                )
            ],
            [
                Label(
                    about_frame,
                    text="funchan@msn.cn",
                    anchor=CENTER,
                    bootstyle=SECONDARY,
                )
            ],
            [Separator(about_frame)],
            [
                Label(
                    about_frame,
                    text="Thanks to Python \nand the following packages",
                    anchor=CENTER,
                    justify=CENTER,
                )
            ],
        ]

        if show_donate_image:
            donate_button = Button(
                about_frame,
                text="Buy me a coffee",
                command=self._open_donate,
                bootstyle=OUTLINE,
            )

            widgets_list = widgets_list[:2] + [[donate_button]] + widgets_list[2:]

        widgets_list += package_labels
        self.grid_widget(widgets_list, about_frame, (0, self.base_size // 2, 0, 0))
        about_frame.grid()

        self.center_horizontally(self.about_toplevel, layout_base)
        self.about_toplevel.deiconify()

        if show_update:
            self.after(1000, self._update_dialog)

    def _open_donate(self):
        webbrowser.open("https://bmc.link/funchan7")

    def _update_dialog(self):
        with contextlib.suppress(Exception):
            if self.has_update:
                update_dialog = CenterMessagebox()
                ret = update_dialog.okcancel("发现新版本，是否更新？", self)
                if ret == MessageCatalog.translate("ok"):
                    install_file = self.download_update()
                    if install_file:
                        self.install_update(install_file)

    def download_update(self) -> object:
        pass

    def install_update(self, install_file):
        pass

    def wait_work_done(
        self,
        thread: Thread,
        interval: int = 100,
        callback: Optional[Callable] = None,
        *args,
        **kwargs,
    ):
        if thread.is_alive():
            self.after(
                interval,
                lambda: self.wait_work_done(
                    thread, interval, callback, *args, **kwargs
                ),
            )
        elif callback:
            if args:
                if kwargs:
                    callback(args, kwargs)
                else:
                    callback(args)
            elif kwargs:
                callback(kwargs)
            else:
                callback()


class CustomToplevle(Toplevel, CustomWindow):
    def __init__(
        self,
        title="ttkbootstrap",
        version="0.0.1",
        base_size=5,
        is_grab=True,
        base_window=None,
        iconphoto="",
        size=None,
        position=None,
        minsize=None,
        maxsize=None,
        resizable=None,
        transient=None,
        overrideredirect=False,
        windowtype=None,
        topmost=False,
        toolwindow=False,
        alpha=1,
        **kwargs,
    ):
        """
        Parameters:

            title (str):
                The title that appears on the application titlebar.

            version (str):
                The version of the application.

            base_size (int):
                The base spacing between widgets.

            is_grab (bool):
                set grab for application.

            base_window(Tuple[None, Window, Toplevel]):
                The base window for place application window.

            iconphoto (str):
                A path to the image used for the titlebar icon.
                Internally this is passed to the `Tk.iconphoto` method.
                By default, the application icon is used.

            size (Tuple[int, int]):
                The width and height of the application window.
                Internally, this argument is passed to the
                `Toplevel.geometry` method.

            position (Tuple[int, int]):
                The horizontal and vertical position of the window on
                the screen relative to the top-left coordinate.
                Internally this is passed to the `Toplevel.geometry`
                method.

            minsize (Tuple[int, int]):
                Specifies the minimum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Toplevel.minsize` method.

            maxsize (Tuple[int, int]):
                Specifies the maximum permissible dimensions for the
                window. Internally, this argument is passed to the
                `Toplevel.maxsize` method.

            resizable (Tuple[bool, bool]):
                Specifies whether the user may interactively resize the
                toplevel window. Must pass in two arguments that specify
                this flag for _horizontal_ and _vertical_ dimensions.
                This can be adjusted after the window is created by using
                the `Toplevel.resizable` method.

            transient (Union[Tk, Widget]):
                Instructs the window manager that this widget is
                transient with regard to the widget master. Internally
                this is passed to the `Toplevel.transient` method.

            overrideredirect (bool):
                Instructs the window manager to ignore this widget if
                True. Internally, this argument is processed as
                `Toplevel.overrideredirect(1)`.

            windowtype (str):
                On X11, requests that the window should be interpreted by
                the window manager as being of the specified type. Internally,
                this is passed to the `Toplevel.attributes('-type', windowtype)`.

                See the [-type option](https://tcl.tk/man/tcl8.6/TkCmd/wm.htm#M64)
                for a list of available options.

            topmost (bool):
                Specifies whether this is a topmost window (displays above all
                other windows). Internally, this processed by the window as
                `Toplevel.attributes('-topmost', 1)`.

            toolwindow (bool):
                On Windows, specifies a toolwindow style. Internally, this is
                processed as `Toplevel.attributes('-toolwindow', 1)`.

            alpha (float):
                On Windows, specifies the alpha transparency level of the
                toplevel. Where not supported, alpha remains at 1.0. Internally,
                this is processed as `Toplevel.attributes('-alpha', alpha)`.

            **kwargs (Dict):
                Other optional keyword arguments.
        """

        super().__init__(
            title,
            iconphoto,
            size,
            position,
            minsize,
            maxsize,
            resizable,
            transient,
            overrideredirect,
            windowtype,
            topmost,
            toolwindow,
            alpha,
            **kwargs,
        )
        self.withdraw()

        if is_grab:
            self.grab_set()

        self.version = parse_version(version)
        self.base_size = utility.scale_size(self, base_size)

        self.add_widget()

        if position is None:
            self.center_horizontally(self, base_window)
        self.deiconify()


if __name__ == "__main__":
    app = CustomWindow("乘法表")
    app.mainloop()
