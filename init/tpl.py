#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

dirs_str = '''#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

from pathlib import Path

root_dir = Path(__file__).resolve().parents[1]
bin_dir = root_dir / 'bin'
conf_dir = root_dir / 'conf'
core_dir = root_dir / 'core'
db_dir = root_dir / 'db'
docs_dir = root_dir / 'docs'
init_dir = root_dir / 'init'
input_dir = root_dir / 'input'
log_dir = root_dir / 'log'
output_dir = root_dir / 'output'
res_dir = root_dir / 'res'
tests_dir = root_dir / 'tests'
'''

gitignore_str = '''# Pycache
__pycache__

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker.idea
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# personal
.vscode
.idea
core/donate.py
db/
input/
log/
output/'''

gui_str = '''#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

import contextlib
import functools
import itertools
from base64 import b64decode
from io import BytesIO
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

    def get_center_point(self, _window: Union[Window, Toplevel],
                         base_window: Union[Window, Toplevel, None]):
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
            self._toplevel.geometry(f'+{x}+{y}')
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
    def show_info(message,
                  base_window,
                  title=" ",
                  parent=None,
                  alert=False,
                  **kwargs):
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
        dialog = CenterMessageDialog(message=message,
                                     title=title,
                                     alert=alert,
                                     parent=parent,
                                     buttons=["OK:primary"],
                                     icon=Icon.info,
                                     localize=True,
                                     **kwargs)

        dialog.center_show(base_window)

    @staticmethod
    def show_warning(message,
                     base_window,
                     title=" ",
                     parent=None,
                     alert=True,
                     **kwargs):
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
    def show_error(message,
                   base_window,
                   title=" ",
                   parent=None,
                   alert=True,
                   **kwargs):
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
    def show_question(message,
                      base_window,
                      title=" ",
                      parent=None,
                      buttons=None,
                      alert=True,
                      **kwargs):
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
    def ok(message,
           base_window,
           title=" ",
           alert=False,
           parent=None,
           **kwargs):
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
    def okcancel(message,
                 base_window,
                 title=" ",
                 alert=False,
                 parent=None,
                 **kwargs):
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
    def yesno(message,
              base_window,
              title=" ",
              alert=False,
              parent=None,
              **kwargs):
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
    def yesnocancel(message,
                    base_window,
                    title=" ",
                    alert=False,
                    parent=None,
                    **kwargs):
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
    def retrycancel(message,
                    base_window,
                    title=" ",
                    alert=False,
                    parent=None,
                    **kwargs):
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
    more convenient api with additional bells and whistles """

    def __init__(
        self,
        title="ttkbootstrap",
        version='0.0.1',
        base_size=5,
        themename="litera",
        iconphoto='',
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
                this default behavior, set the value to `None` and use
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

        super().__init__(title, themename, iconphoto, size, position, minsize,
                         maxsize, resizable, hdpi, scaling, transient,
                         overrideredirect, alpha)
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
        default_font = font.nametofont('TkDefaultFont')
        text_font = font.nametofont('TkTextFont')
        fixed_font = font.nametofont('TkFixedFont')
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

    def get_center_point(self, _window: Union[Window, Toplevel],
                         base_window: Union[Window, Toplevel, None]):
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

    def center_horizontally(self,
                            _window: Union[Window, Toplevel],
                            base_window: Union[Window, Toplevel, None] = None):
        x, y = self.get_center_point(_window, base_window)
        _window.geometry(f'+{x}+{y}')

    def add_widget(self):
        """
        - means columnspan
        n int means a blank Label, width = n
        """
        menu = Menu(self)
        package_list = ['ttkbootstrap']
        menu.add_command(
            label='关于',
            command=lambda: self.show_about(package_list, layout_base=self))
        self.config(menu=menu)

        widgets_list = [[1] * 9 for _ in range(9)]
        for i, j in itertools.product(range(9), range(9)):
            if i >= j:
                widgets_list[i][j] = Label(
                    self,
                    text=f'{j + 1}*{i + 1}={(i + 1) * (j + 1)}',
                    anchor=CENTER,
                    bootstyle=(SUCCESS, INVERSE))

        self.grid_widget(widgets_list, self, self.base_size)

    @staticmethod
    def grid_widget(widgets_list: List[List[Union[Widget, str, int]]],
                    master: Union[Window, Toplevel],
                    padding: Union[int, Tuple[int, int, int, int]] = 0,
                    anchor: ANCHOR = CENTER,
                    sticky=NSEW):
        master.grid_anchor(anchor)
        max_column = len(widgets_list[0])
        assert all(len(_widgets) == max_column for _widgets in
                   widgets_list), 'the elements of each row are not equal'

        if isinstance(padding, int):
            padx = pady = ipadx = ipady = padding
        elif isinstance(padding, tuple):
            padx, pady, ipadx, ipady = padding
        else:
            raise TypeError('wrong parameter type')

        for row, _widgets in enumerate(widgets_list):
            for column, widget in enumerate(_widgets):
                if widget != '-':
                    columnspan = 1
                    for i in range(column + 1, max_column):
                        if _widgets[i] != '-':
                            break
                        columnspan += 1

                    if isinstance(widget, int):
                        widget = Label(master, width=widget)

                    try:
                        widget.grid(row=row,
                                    column=column,
                                    columnspan=columnspan,
                                    padx=padx,
                                    pady=pady,
                                    ipadx=ipadx,
                                    ipady=ipady,
                                    sticky=sticky)
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

    def show_progress(self,
                      mode='indeterminate',
                      interval=50,
                      step=1.0,
                      show_cancel_button=False,
                      cancel_function: Optional[Callable] = None):
        """mode: Literal['determinate', 'indeterminate']"""
        self.progress_toplevel = Toplevel(overrideredirect=True, topmost=True)
        self.progress_toplevel.withdraw()
        self.progress_toplevel.grab_set()

        self.progress_var = IntVar(value=0)
        progress_progressbar = Progressbar(self.progress_toplevel,
                                           mode=mode,
                                           variable=self.progress_var,
                                           length=25 * self.base_size)
        if show_cancel_button:
            cancel_button = Button(self.progress_toplevel,
                                   text=MessageCatalog.translate('cancel'),
                                   command=cancel_function)
            self.grid_widget([[progress_progressbar, cancel_button]],
                             self.progress_toplevel, (0, 0, 0, self.base_size))
        else:
            self.grid_widget([[progress_progressbar]], self.progress_toplevel,
                             (0, 0, 0, 2 * self.base_size))

        self.center_horizontally(self.progress_toplevel, self)
        self.progress_toplevel.deiconify()

        if mode == 'indeterminate':
            progress_progressbar.step(step)
            progress_progressbar.start(interval)

    def show_about(self,
                   package_list: List[str],
                   show_donate_image: bool = True,
                   donate_qr_title: str = '微信扫码赞赏作者',
                   show_update: bool = True,
                   layout_base=None):

        package_list.sort(key=lambda x: x.lower())

        self.about_toplevel = Toplevel(title='',
                                       resizable=(False, False),
                                       transient=self)
        self.about_toplevel.withdraw()
        self.about_toplevel.grab_set()
        self.about_toplevel.bind('<Escape>',
                                 lambda e: self.about_toplevel.destroy())

        about_frame = ScrolledFrame(self.about_toplevel,
                                    autohide=True,
                                    width=55 * self.base_size,
                                    height=50 * self.base_size)
        package_labels = [[
            Label(about_frame, text=i, anchor=CENTER, bootstyle=PRIMARY)
        ] for i in package_list]

        font_family = font.nametofont("TkDefaultFont").cget("family")
        widgets_list = [[
            Label(about_frame,
                  text=f'{self.title()} v{self.version}',
                  font=f'"{font_family}" 12',
                  anchor=CENTER,
                  bootstyle=PRIMARY)
        ],
                        [
                            Label(about_frame,
                                  text='funchan@msn.cn',
                                  anchor=CENTER,
                                  bootstyle=SECONDARY)
                        ], [Separator(about_frame)],
                        [
                            Label(about_frame,
                                  text='感谢Python及下列包',
                                  anchor=CENTER)
                        ]]

        if show_donate_image:
            admire_data = b'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'

            image_byte = b64decode(admire_data)
            byte_io = BytesIO(image_byte)
            image = Image.open(byte_io)
            image = image.resize((30 * self.base_size, 30 * self.base_size))
            self._donate_image = ImageTk.PhotoImage(image)

            widgets_list = widgets_list[:2] + [
                [Separator(about_frame)],
                [Label(about_frame, text=donate_qr_title, anchor=CENTER)],
                [Label(about_frame, image=self._donate_image, anchor=CENTER)]
            ] + widgets_list[2:]

        widgets_list += package_labels
        self.grid_widget(widgets_list, about_frame,
                         (0, self.base_size // 2, 0, 0))
        about_frame.grid()

        self.center_horizontally(self.about_toplevel, layout_base)
        self.about_toplevel.deiconify()

        if show_update:
            self.after(1000, self._update_dialog)

    def _update_dialog(self):
        with contextlib.suppress(Exception):
            if self.has_update:
                update_dialog = CenterMessagebox()
                ret = update_dialog.okcancel('发现新版本，是否更新？', self)
                if ret == MessageCatalog.translate('ok'):
                    install_file = self.download_update()
                    if install_file:
                        self.install_update(install_file)

    def download_update(self) -> object:
        pass

    def install_update(self, install_file):
        pass

    def wait_work_done(self,
                       thread: Thread,
                       interval: int = 100,
                       callback: Optional[Callable] = None,
                       *args,
                       **kwargs):
        if thread.is_alive():
            self.after(
                interval, lambda: self.wait_work_done(
                    thread, interval, callback, *args, **kwargs))
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

    def __init__(self,
                 title="ttkbootstrap",
                 version='0.0.1',
                 base_size=5,
                 is_grab=True,
                 base_window=None,
                 iconphoto='',
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
                 **kwargs):
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

        super().__init__(title, iconphoto, size, position, minsize, maxsize,
                         resizable, transient, overrideredirect, windowtype,
                         topmost, toolwindow, alpha, **kwargs)
        self.withdraw()

        if is_grab:
            self.grab_set()

        self.version = parse_version(version)
        self.base_size = utility.scale_size(self, base_size)

        self.add_widget()

        if position is None:
            self.center_horizontally(self, base_window)
        self.deiconify()


if __name__ == '__main__':
    app = CustomWindow('乘法表')
    app.mainloop()
'''

launch_str = '''#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

# Author: funchan
# CreateDate: 2021-10-28 21:18:12
# Description: launcher

import os
import platform
import sys
from pathlib import Path
from subprocess import PIPE, run

root_dir = Path(__file__).resolve().parent
core_dir = root_dir / 'core'
sys.path.append(str(core_dir))


def get_venv_path():
    venv_dir = root_dir / '.venv'

    os_platform = platform.system()
    if os_platform == 'Windows':
        python_str = 'python'
        python_path = venv_dir / 'scripts' / 'python.exe'
        pip_path = venv_dir / 'scripts' / 'pip.exe'

    elif os_platform == 'Linux':
        python_str = 'python3'
        python_path = venv_dir / 'bin' / 'python3'
        pip_path = venv_dir / 'bin' / 'pip3'

    else:
        raise EnvironmentError('unsupported platform!')

    return python_str, python_path, pip_path


def set_pip(pip_path, python_path):
    cmd_list = [
        f'{pip_path} config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/',
        f'{pip_path} config set global.trusted-host pypi.tuna.tsinghua.edu.cn',
        f'{pip_path} config set global.timeout 6000',
        f'{python_path} -m pip install -U pip'
    ]

    [run(cmd, shell=True, stdout=PIPE, stderr=PIPE) for cmd in cmd_list]


def start():
    os.chdir(root_dir)
    _, venv_python_path, venv_pip_path = get_venv_path()

    if Path(sys.executable) != venv_python_path:
        run(f'{venv_python_path} {__file__}', shell=True)
        sys.exit()

    try:
        from main import main
        main()

    except ModuleNotFoundError:
        set_pip(venv_pip_path, venv_python_path)
        run(f'{venv_pip_path} install -r requirements.txt',
            shell=True,
            stdout=PIPE)

        from main import main
        main()


if __name__ == '__main__':
    start()
'''

log_str = '''#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class Logger(object):

    def __init__(self,
                 log_dir: Path,
                 log_file_name: str = None,
                 show_level=logging.INFO,
                 maxBytes=5 * 1024 * 1024,
                 backupCount=5):

        self.log_dir = log_dir
        self.log_file_name = log_file_name
        self.show_level = show_level
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        self.formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)s>>%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        self.filehandlers = {}
        self.steamhandler = None

    def __create_handler(self, log_level: int):
        if log_level not in self.filehandlers.keys():
            if self.log_file_name:
                log_file = self.log_dir / f'{self.log_file_name} - {logging.getLevelName(log_level)}.log'
            else:
                log_file = self.log_dir / f'{logging.getLevelName(log_level)}.log'

            filehandler = RotatingFileHandler(log_file,
                                              encoding='utf-8',
                                              maxBytes=self.maxBytes,
                                              backupCount=self.backupCount)

            filehandler.setFormatter(self.formatter)
            filehandler.setLevel(log_level)
            self.filehandlers[log_level] = filehandler

        if not self.steamhandler:
            steamhandler = logging.StreamHandler()
            steamhandler.setFormatter(self.formatter)
            steamhandler.setLevel(self.show_level)
            self.steamhandler = steamhandler

    def __log(self, flag, message):
        logger = logging.getLogger(flag)
        log_level = logging._nameToLevel[flag.upper()]
        logger.setLevel(log_level)

        self.__create_handler(log_level)
        logger.addHandler(self.filehandlers[log_level])
        logger.addHandler(self.steamhandler)

        logger.log(log_level, message)

    def debug(self, message):
        self.__log('debug', message)

    def info(self, message):
        self.__log('info', message)

    def warning(self, message):
        self.__log('warning', message)

    def error(self, message):
        self.__log('error', message)

    def critical(self, message):
        self.__log('critical', message)
'''

main_str = '''#!/usr/bin/env/python3
# -*- coding:utf-8 -*-

# Author: $author
# CreateDate: $createdate
# Description: $description

from dirs import *
from log import Logger

# write your code here ...


def main():
    ...


if __name__ == '__main__':
    main()
'''

readme_str = '''## $appname

*$description*

### 用法

* 双击 **start.bat** 或 **start.sh** 启动程序
* 程序运行结束，打开 **output** 目录查看运行结果

### 文件

* start.bat： Windows启动程序
* start.sh： Linux启动程序

### 目录
<table>
    <tr>
        <th>序号</th>
        <th>名称</th>
        <th>说明</th>
    </tr>
    <tr>
        <td>1</td>
        <td>.venv</td>
        <td>Python虚拟环境</td>
    </tr>
    <tr>
        <td>2</td>
        <td>bin</td>
        <td>依赖的可执行程序</td>
    </tr>
    <tr>
        <td>3</td>
        <td>conf</td>
        <td>配置信息</td>
    </tr>
    <tr>
        <td>4</td>
        <td>core</td>
        <td>核心代码</td>
    </tr>
    <tr>
        <td>5</td>
        <td>db</td>
        <td>数据库文件</td>
    </tr>
    <tr>
        <td>6</td>
        <td>docs</td>
        <td>说明文档</td>
    </tr>
    <tr>
        <td>7</td>
        <td>init</td>
        <td>程序初始化、打包</td>
    </tr>
    <tr>
        <td>8</td>
        <td>input</td>
        <td>用户输入文件</td>
    </tr>
    <tr>
        <td>9</td>
        <td>log</td>
        <td>运行日志</td>
    </tr>
    <tr>
        <td>10</td>
        <td>output</td>
        <td>运行结果</td>
    </tr>
    <tr>
        <td>11</td>
        <td>res</td>
        <td>引用资源</td>
    </tr>
    <tr>
        <td>12</td>
        <td>tests</td>
        <td>测试代码</td>
    </tr>
</table>'''

start_str_cmd = r'''@echo off

cd /d %~dp0
setlocal enabledelayedexpansion

if not exist .venv\scripts\python.exe (
    python -m venv .venv 1>nul 2>nul

    if not exist .venv\scripts\python.exe (
        echo Install Python...
        set temp_file=!Temp!\python-3.8.10.exe

        set url="https://oss.npmmirror.com/dist/python/3.8.10/python-3.8.10.exe"
        certutil -urlcache -split -f !url! !temp_file! 1>nul 2>nul

        if !errorlevel! NEQ 0 (
            set url="https://www.python.org/ftp/python/3.8.10/python-3.8.10.exe"
            certutil -urlcache -split -f !url! !temp_file! 1>nul 2>nul

            if !errorlevel! NEQ 0 (
                echo Error: Failed to download Python, Check the network!
                pause >nul
                exit
            )
        )

        if "!PROCESSOR_ARCHITECTURE!"=="AMD64" (
            set python_dir=!LocalAppData!\Programs\Python37-32
        ) else (
            set python_dir=!LocalAppData!\Programs\Python37
        )

        !temp_file! /passive /quiet PrependPath=1 TargetDir=!python_dir!
        !python_dir!\python.exe -m venv .venv 1>nul 2>nul
    )
)

.venv\scripts\python.exe launch.py'''

start_str_dash = r'''stty -echo

cd `dirname $0`

if [ ! -e ./.venv/bin/python3 ]; then
    python3 -m venv .venv
    if [ ! -e ./.venv/bin/python3 ]; then
        echo Install Python3.x and run this script again.
    fi
fi
./.venv/bin/python3 ./launch.py'''
