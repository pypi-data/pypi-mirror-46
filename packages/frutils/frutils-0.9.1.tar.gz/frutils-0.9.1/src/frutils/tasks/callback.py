# -*- coding: utf-8 -*-
import abc
import logging
import os
import sys

import click
import six
import stevedore
from colorama import Fore, Style
from halo import Halo

from frutils import get_terminal_size

log = logging.getLogger("frutils")


CURSOR_UP_ONE = "\x1b[1A"
ERASE_LINE = "\x1b[2K"

BOLD = "\033[1m"
UNBOLD = "\033[0m"

ARC_DOWN_RIGHT = u"\u256d"
ARC_UP_RIGHT = u"\u2570"
ARC_UP_LEFT = u"\u256f"
VERTICAL_RIGHT = u"\u251C"
VERTICAL_LEFT = u"\u2528"
VERTICAL = u"\u2502"
HORIZONTAL = u"\u2500"
END = u"\u257C"
ARROW = u"\u279B"
OK = u"\u2713"
ARROR_RESULT = u"\u257C"


def output_to_terminal(line, nl=True, no_output=False):

    if no_output:
        return

    click.echo(line.encode("utf-8"), nl=nl)


def delete_last_line(no_display=False):

    if no_display:
        return

    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)


def load_callback(callback_name, callback_config=None):
    """Loading a freckles callback extension.

    Returns:
      frutils.tasks.callback.TasksCallback: the callback object
    """

    if callback_config is None:
        callback_config = {}

    log2 = logging.getLogger("stevedore")
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter("task plugin plugin error -> %(message)s"))
    out_hdlr.setLevel(logging.DEBUG)
    log2.addHandler(out_hdlr)
    log2.setLevel(logging.INFO)

    log.debug("Loading freckles callback...")

    mgr = stevedore.driver.DriverManager(
        namespace="frutils.callbacks",
        name=callback_name,
        invoke_on_load=True,
        invoke_kwds=callback_config,
    )
    log.debug(
        "Registered plugins: {}".format(", ".join(ext.name for ext in mgr.extensions))
    )

    return mgr.driver


def colorize_status(status, ignore_errors=False):

    if status == "ok":
        result = Fore.GREEN + status + Style.RESET_ALL
    elif status == "no change" or status == "unchanged":
        result = Fore.GREEN + status + Style.RESET_ALL
    elif status == "skipped":
        result = Fore.YELLOW + status + Style.RESET_ALL
    elif status == "failed":
        if not ignore_errors:
            result = Fore.RED + status + Style.RESET_ALL
        else:
            result = Fore.YELLOW + "{} (ignored)".format(status) + Style.RESET_ALL
    else:
        result = status

    return result


@six.add_metaclass(abc.ABCMeta)
class TasksCallback(object):
    def __init__(self):

        pass

    def task_paused(self):

        pass

    def task_resumed(self):

        pass


class TasksCallbackSilent(TasksCallback):
    def __init__(self, **kwargs):

        pass

    def task_started(self, task):

        pass

    def task_finished(self, task):

        pass


class TasksCallbackPlain(TasksCallback):
    def __init__(self, **kwargs):

        self._parent_task_open = False
        self._detail_level = 10
        self._debug = kwargs.get("debug", False)

    def task_started(self, task):

        if task.detail_level > self._detail_level:
            return

        if not self._debug:
            padding = "  " * task.level
            if self._parent_task_open:
                click.echo()
            output_to_terminal(u"{}- {}".format(padding, task.msg), nl=False)
            self._parent_task_open = True
        else:
            padding = "-" * task.level
            output_to_terminal(
                u"-{} STARTING ({}): {}".format(padding, task.id, task.msg), nl=True
            )

    def task_finished(self, task):

        if task.detail_level > self._detail_level:
            return

        if task.success:
            if task.skipped is True:
                status = "skipped"
            else:
                if task.changed is True:
                    status = "ok"
                else:
                    status = "no change"
        else:
            status = "failed"

        status = colorize_status(status, task.ignore_errors)

        if not self._debug:
            if not self._parent_task_open:
                return

            output_to_terminal(u" -> {}".format(status))
            self._parent_task_open = False
        else:
            padding = "-" * task.level
            output_to_terminal(
                u"-{} FINISHED {} ({}) -> {}".format(
                    padding, task.msg, task.id, status
                ),
                nl=True,
            )

        # if not task.success:
        #     reindent_level = (2 * (task.level+2))
        #     if task.get_messages():
        #         if "\n" not in task.get_messages().strip():
        #             click.echo(reindent("msg: {}".format(task.get_messages().strip()), reindent_level))
        #         else:
        #             click.echo(reindent(u"msg:", reindent_level))
        #             click.echo(reindent(task.get_messages(), reindent_level+2))
        #     if task.get_error_messages():
        #         if "\n" not in task.get_error_messages().strip():
        #             click.echo(reindent("error: {}".format(task.get_error_messages().strip()), reindent_level))
        #         else:
        #             click.echo(reindent(u"error:", reindent_level))
        #             click.echo(reindent(task.get_error_messages(), reindent_level+2))

    def task_paused(self):

        click.echo()

    def task_resumed(self):

        pass


PROFILE_MAP = {"full": {"show_skipped": True, "show_no_change": True, "show_msg": True}}


def get_callback_config_value(key, config, default, profile_name=None):

    if config.get(key, None) is not None:
        return config[key]

    if profile_name is not None:
        profile = PROFILE_MAP.get(profile_name, None)
        if profile is not None:
            if profile.get(key, None) is not None:
                return profile[key]

    return default


class TasksCallbackDefault(TasksCallback):
    def __init__(self, **kwargs):

        self._detail_level = 10
        self.last_level = 0

        self.started_tasks = {}

        profile_name = kwargs.pop("profile", None)

        self.show_skipped = get_callback_config_value(
            key="show_skipped", config=kwargs, default=False, profile_name=profile_name
        )
        self.show_no_change = get_callback_config_value(
            key="show_no_change",
            config=kwargs,
            default=False,
            profile_name=profile_name,
        )
        self.show_msg = get_callback_config_value(
            key="show_msg", config=kwargs, default=False, profile_name=profile_name
        )

    def get_task_started_string(self, task):

        current_level = task.level

        if current_level == 0:
            msg = u"{}{} {}".format(ARC_DOWN_RIGHT, END, task.msg)
        else:
            if current_level == 1:
                padding = ""
            else:
                padding = u"  {}".format(VERTICAL) * (current_level - 1)

            padding = padding + u"  {}".format(VERTICAL_RIGHT)
            msg = u"{}{}{} {}".format(VERTICAL, padding, END, task.msg)

        return msg

    def get_finished_padding(self, task):

        padding = u"  {}".format(VERTICAL) * task.level
        return padding

    def get_task_finished_status(self, task):

        if task.success:
            if task.skipped is True:
                status = "skipped"
            else:
                if task.changed is True:
                    status = "ok"
                else:
                    status = "no change"
        else:
            status = "failed"
        status = colorize_status(status, task.ignore_errors)

        msg = u"{}{}  {}{} {}".format(
            VERTICAL,
            self.get_finished_padding(task),
            ARC_UP_RIGHT,
            ARROR_RESULT,
            status,
        )

        return msg

    def get_msg_string(self, task):

        padding = self.get_finished_padding(task)

        if "\n" not in task.get_messages().strip():
            msg = "{}{}  {} msg: {}".format(
                VERTICAL, padding, VERTICAL_RIGHT, task.get_messages().strip()
            )
        else:
            msg = "{}{}  {} msg:".format(VERTICAL, padding, VERTICAL_RIGHT)

            for line in task.get_messages().strip().split("\n"):
                msg = msg + "\n{}{}  {}   {}".format(VERTICAL, padding, VERTICAL, line)

        return msg

    def get_error_msg_string(self, task):

        padding = self.get_finished_padding(task)

        if "\n" not in task.get_error_messages().strip():
            msg = "{}{}  {} {}error{}: {}".format(
                VERTICAL,
                padding,
                VERTICAL_RIGHT,
                Fore.RED,
                Style.RESET_ALL,
                task.get_error_messages().strip(),
            )
        else:

            msg = "{}{}  {} {}error{}:".format(
                VERTICAL, padding, VERTICAL_RIGHT, Fore.RED, Style.RESET_ALL
            )
            for line in task.get_error_messages().strip().split("\n"):
                msg = msg + "\n{}{}  {}   {}".format(VERTICAL, padding, VERTICAL, line)

        return msg

    def get_task_conclusion(self, task):

        if task.success:
            tasks_status = "ok"
        else:
            tasks_status = "failed"

        tasks_status = colorize_status(tasks_status)

        msg = u"{}{} {}".format(ARC_UP_RIGHT, ARROR_RESULT, tasks_status)
        return msg

    def task_started(self, task):

        if task.detail_level > self._detail_level:
            return

        msg = self.get_task_started_string(task)
        self.print_msg(task, msg)

    def print_msg(self, task, msg):
        output_to_terminal(msg)

        self.started_tasks.setdefault(task.id, []).append(msg)

    def remove_printed_lines(self, task):

        msgs = self.started_tasks.get(task.id, None)
        if msgs is None:
            return

        new_lines = 0
        for msg in msgs:
            new_lines = new_lines + 1
            new_lines = new_lines + msg.count("\n")
            width = get_terminal_size()[0]
            if len(msg) > get_terminal_size()[0]:
                extra_lines = int(len(msg) / width)
                new_lines = new_lines + extra_lines

        if new_lines < 1:
            return

        for i in range(0, new_lines):
            delete_last_line()

    def task_finished(self, task):

        if task.detail_level > self._detail_level:
            return

        try:
            if (task.success or not task.success and task.ignore_errors) and (
                task.level != 0 or task._tasks.is_utility_task
            ):
                skip = False
                if task.skipped and not self.show_skipped:
                    skip = True

                if not task.changed and not self.show_no_change:
                    skip = True

                if task.get_messages(detail_level=0) or (
                    self.show_msg and task.get_messages()
                ):
                    skip = False

                if skip:
                    self.remove_printed_lines(task)
                    return
                if self.show_msg or task.get_messages(detail_level=0):
                    if task.get_messages():
                        msg = self.get_msg_string(task)
                        self.print_msg(task, msg)

            if not task.success and (task.get_messages() or task.get_error_messages()):

                if task.get_messages():
                    msg = self.get_msg_string(task)
                    self.print_msg(task, msg)

                if task.get_error_messages():
                    msg = self.get_error_msg_string(task)
                    self.print_msg(task, msg)

            msg = self.get_task_finished_status(task)
            self.print_msg(task, msg)

        finally:

            if task.level == 0:

                if not task._tasks.is_utility_task:
                    msg = self.get_task_conclusion(task)
                    output_to_terminal(msg)
                elif task._tasks.is_utility_task and task.changed:
                    msg = self.get_task_conclusion(task)
                    output_to_terminal(msg)
                elif task._tasks.is_utility_task and not task.skipped:
                    msg = self.get_task_conclusion(task)
                    output_to_terminal(msg)
                elif task._tasks.is_utility_task and task.skipped and self.show_skipped:
                    msg = self.get_task_conclusion(task)
                    output_to_terminal(msg)
                elif (
                    task._tasks.is_utility_task
                    and not task.changed
                    and self.show_no_change
                ):
                    msg = self.get_task_conclusion(task)
                    output_to_terminal(msg)

                self.started_tasks = {}

    def task_paused(self):

        click.echo()

    def task_resumed(self):

        pass


class TasksCallbackAuto(TasksCallback):
    def __init__(self, **kwargs):

        super(TasksCallbackAuto, self).__init__()

        lang = os.environ["LANG"].lower()

        if "utf-8" in lang:
            if sys.stdout.isatty():
                callback = "spinner"
            else:
                callback = "plain"
        else:
            callback = "default"

        if callback == "default":
            self.callback = TasksCallbackDefault(**kwargs)
        elif callback == "spinner":
            self.callback = TasksCallbackSpinner(**kwargs)
        elif callback == "plain":
            self.callback = TasksCallbackPlain(**kwargs)
        else:
            self.callback = TasksCallbackDefault(**kwargs)

    def __getattr__(self, name):

        return getattr(self.callback, name)

    def task_paused(self):

        self.callback.task_paused()

    def task_resumed(self):

        self.callback.task_resumed()


class TasksCallbackSpinner(TasksCallbackDefault):
    def __init__(self, **kwargs):

        super(TasksCallbackSpinner, self).__init__(**kwargs)

        spinner_dict = self.get_spinner_dict()
        self.spinner = Halo(
            text="Initiating...", spinner=spinner_dict, color="grey", animation="bounce"
        )

        self.current_tasks = []
        # self.already_printed = {}

    def task_started(self, task):

        if task.detail_level > self._detail_level:
            return
        if self.current_tasks:
            self.stop_spinner()
            self.print_current_tasks()
        self.start_spinner(task)
        self.current_tasks.append(task)
        # self.already_printed[task.id] = {"task": task}

    def print_current_tasks(self):

        for t in self.current_tasks:
            self.print_msg(t, self.get_task_started_string(t))
            # output_to_terminal(self.get_task_started_string(t))

        self.current_tasks = []

    def task_finished(self, task):

        self.stop_spinner()
        self.print_current_tasks()

        try:

            if (task.success or not task.success and task.ignore_errors) and (
                task.level != 0 or task._tasks.is_utility_task
            ):

                skip = False
                if task.skipped and not self.show_skipped:
                    skip = True

                if not task.changed and not self.show_no_change:
                    skip = True

                if task.get_messages(detail_level=0):
                    skip = False

                if skip:
                    self.remove_printed_lines(task)
                    return

                if self.show_msg or task.get_messages(detail_level=0):

                    if task.get_messages():
                        msg = self.get_msg_string(task)
                        self.print_msg(task, msg)

            if not task.success and (task.get_messages() or task.get_error_messages()):

                if task.get_messages():
                    msg = self.get_msg_string(task)
                    self.print_msg(task, msg)

                if task.get_error_messages():
                    msg = self.get_error_msg_string(task)
                    self.print_msg(task, msg)

            finished_msg = self.get_task_finished_status(task)
            self.print_msg(task, finished_msg)
            # self.already_printed[task.id].setdefault("output", []).append(finished_msg)

        finally:
            if task.level == 0:
                if not task._tasks.is_utility_task or task.changed or not task.skipped:
                    msg = self.get_task_conclusion(task)
                    output_to_terminal(msg)

                self.spinner.stop()
                self.current_tasks = []
                self.started_tasks = {}

    def start_spinner(self, task=None):

        if task is not None:
            self.spinner.spinner = self.get_spinner_dict(task)
            if isinstance(task.msg, six.string_types):
                m = task.msg
            else:
                m = str(task.msg)
            self.spinner.text = m
        else:
            self.spinner.text = ""
        self.spinner.start()

    def stop_spinner(self):

        self.spinner.stop()

    def get_spinner_dict(self, task=None):

        if task is None:
            level = 0
        else:
            level = task.level

        padding = u"{}  ".format(VERTICAL) * level

        result = []

        # spinner_list = Spinners.pipe.value.get("frames")
        if level == 0:
            return "dots"
        else:
            # spinner_list = ["└", "├", "│", "┤", "┘", "┴"]
            spinner_list = [ARC_UP_RIGHT, VERTICAL, ARC_UP_LEFT, VERTICAL]

            for character in spinner_list:
                c = "{}{}".format(padding, character)
                result.append(c)

            return {"interval": 240, "frames": result}

    def task_paused(self):

        self.spinner.stop()
        click.echo()

    def task_resumed(self):

        click.echo()
        self.spinner.start()
