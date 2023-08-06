# -*- coding: utf-8 -*-
import logging
from collections import Sequence

from six import string_types
from treelib import Tree

from frutils.tasks.callback import TasksCallbackPlain

log = logging.getLogger("frutils")


class Tasks(object):
    def __init__(
        self,
        title,
        category=None,
        msg=None,
        reference=None,
        target=None,
        callbacks=None,
        desc=None,
        data=None,
        is_utility_task=False,
    ):

        self.title = title
        if category is None:
            category = "default"
        self.category = category
        if msg is None:
            msg = self.title
        self.msg = msg
        self.reference = reference
        if target is None:
            target = "localhost"
        self.target = target
        if desc is None:
            desc = "n/a"
        self.desc = desc
        if callbacks is None:
            callbacks = [TasksCallbackPlain()]
        if not isinstance(callbacks, Sequence):
            callbacks = [callbacks]
        self._callbacks = callbacks
        self.is_utility_task = is_utility_task

        if data is None:
            data = {}
        self._data = data

        self._tree = Tree()
        self._root_task = None
        self._current_task = None

        self._highest_task_id = 0

        self._finished = False

        self._paused = False

    @property
    def tree(self):
        return self._tree

    @property
    def current_task(self):

        if self._current_task is None:
            return self.root_task

        return self._current_task

    @property
    def paused(self):

        return self._paused

    @property
    def root_task(self):

        if self._root_task is not None:
            return self._root_task

        return self.start()

    def start(self):

        if self._root_task is not None:
            raise Exception("Tasks already started.")

        task = TaskDetail(
            task_id=0,
            parent_id=-1,
            tasks=self,
            task_name=self.title,
            category=self.category,
            msg=self.msg,
            reference=self.reference,
            ignore_errors=False,
            detail_level=0,
            data=self._data,
        )
        self._root_task = self._tree.create_node(
            tag=self.title, identifier=0, data=task
        ).data

        self._current_task = self._root_task

        for cb in self._callbacks:
            cb.task_started(self._current_task)

        return self._root_task

    @property
    def finished(self):

        return self._finished

    def finish(self):

        if not self._finished:
            if not self.root_task.finished:

                self.root_task.finish()
                # self.root_task.finish()

            # for cb in self._callbacks:
            #     cb.task_finished(self.root_task)

        self._finished = True

    def pause(self):

        self._paused = True
        for cb in self._callbacks:
            cb.task_paused()

    def resume(self):

        self._paused = False
        for cb in self._callbacks:
            cb.task_resumed()

    def task_started(
        self,
        parent_task_detail,
        task_name,
        category=None,
        msg=None,
        reference=None,
        ignore_errors=False,
        detail_level=0,
        data=None,
    ):

        parent_node = self._tree.get_node(parent_task_detail.id)
        self._highest_task_id = self._highest_task_id + 1
        task_details = TaskDetail(
            task_id=self._highest_task_id,
            parent_id=parent_task_detail.id,
            tasks=self,
            task_name=task_name,
            category=category,
            msg=msg,
            reference=reference,
            ignore_errors=ignore_errors,
            detail_level=detail_level,
            data=data,
        )

        task = self._tree.create_node(
            tag=task_name,
            identifier=self._highest_task_id,
            data=task_details,
            parent=parent_node,
        )

        self._current_task = task.data

        for cb in self._callbacks:
            cb.task_started(task.data)

        return task.data

    def _process_finished_state(self, task_details):

        all_childs = self._tree.children(task_details.id)
        success_childs = True
        skipped_childs = True
        changed_childs = False
        for c in all_childs:
            child = c.data
            if not child.finished:
                state = self._process_finished_state(child)
                child._set_finished_state(
                    success=state["success"],
                    changed=state["changed"],
                    skipped=state["skipped"],
                )
                child._finished = True
            if child.success not in [True, None]:
                if child.ignore_errors:
                    success_childs = True
                else:
                    success_childs = False
            if child.skipped not in [True, None]:
                skipped_childs = False
            if child.changed not in [False]:
                changed_childs = True

        success = task_details._success
        if success is None:
            success = success_childs
        skipped = task_details._skipped
        if skipped is None:
            skipped = skipped_childs
        changed = task_details._changed
        if changed is None:
            changed = changed_childs

        return {"success": success, "skipped": skipped, "changed": changed}

    def register_task_finished(self, task_detail):

        while self._current_task != task_detail:

            state = self._process_finished_state(self.current_task)
            self.current_task._set_finished_state(
                success=state["success"],
                changed=state["changed"],
                skipped=state["skipped"],
            )
            self.current_task._finished = True
            for cb in self._callbacks:
                cb.task_finished(self.current_task)

            self._current_task = self.get_task_detail(self.current_task._parent_id)

        state = self._process_finished_state(self.current_task)
        self.current_task._set_finished_state(
            success=state["success"], changed=state["changed"], skipped=state["skipped"]
        )
        self.current_task._finished = True

        for cb in self._callbacks:
            cb.task_finished(self.current_task)

        parent = self._tree.parent(task_detail.id)
        if parent is None:
            return None

        self._current_task = parent.data
        return parent.data

    def get_task_detail(self, task_id):

        node = self._tree.get_node(task_id)
        if not node:
            return None
        else:
            return node.data

    def get_level(self, task_detail):

        return self._tree.level(task_detail.id)


class DummyTaskDetail(object):
    def __getattr__(self, _):
        print(_)
        return self


class TaskWrap(object):
    def __init__(self, parent_task, task_name, msg=None, ignore_errors=False):

        self._parent_task = parent_task
        self._task_detail = parent_task.add_subtask(
            task_name=task_name, msg=msg, ignore_errors=ignore_errors
        )

        self.success = None
        self.skipped = None
        self.changed = None
        self.ignore_errors = ignore_errors
        self.msg = None
        self.error_msg = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):

        if exc_type:
            self.success = False
            if self.error_msg is not None:
                if isinstance(self.error_msg, string_types):
                    self.error_msg = [self.error_msg]
                self.error_msg.append(str(exc_value))
            else:
                self.error_msg = str(exc_value)

        if self.success is None:
            self.success = True
        if self.changed is None:
            self.changed = True
        if self.skipped is None:
            self.skipped = False

        self._task_detail.finish(
            success=self.success,
            changed=self.changed,
            skipped=self.skipped,
            msg=self.msg,
            error_msg=self.error_msg,
        )

        if exc_type:
            raise exc_value


class TaskDetail(object):
    def __init__(
        self,
        task_id,
        parent_id,
        tasks,
        task_name,
        category=None,
        msg=None,
        reference=None,
        ignore_errors=False,
        detail_level=0,
        data=None,
    ):

        self._id = task_id
        self._parent_id = parent_id
        self._task_name = task_name
        self._tasks = tasks
        if category is None:
            category = "default"
        self.category = category
        if msg is None:
            msg = "executing task '{}'".format(task_name)
        self.msg = msg
        self.reference = reference
        self.ignore_errors = ignore_errors
        self.detail_level = detail_level
        if data is None:
            data = {}
        self._data = data
        self._finished = False
        self._skipped = None
        self._changed = None
        self._success = None
        self._result = None

        self._messages = {}
        self._error_messages = {}

    def subtask(self, task_name, msg=None, ignore_errors=False):
        return TaskWrap(
            parent_task=self, task_name=task_name, msg=msg, ignore_errors=ignore_errors
        )

    def __eq__(self, other):

        return self.id == other.id

    @property
    def id(self):
        return self._id

    @property
    def parent(self):

        self._tasks.get_task_detail(self._parent_id)

    @property
    def task_name(self):

        return self._task_name

    @property
    def level(self):

        return self._tasks.get_level(self)

    @property
    def finished(self):
        return self._finished

    @property
    def success(self):

        if not self._finished:
            raise Exception("Task not finished yet")

        return self._success

    @success.setter
    def success(self, success):

        self._success = success
        if self.parent and success is False and not self.ignore_errors:
            self.parent.success = False

    @property
    def skipped(self):

        if not self._finished:
            raise Exception("Task not finished yet")

        return self._skipped

    @skipped.setter
    def skipped(self, skipped):

        self._skipped = skipped
        if self.parent and not self._skipped:
            self.parent.skipped = False

    @property
    def changed(self):

        if not self._finished:
            raise Exception("Task not finished yet")

        return self._changed

    @changed.setter
    def changed(self, changed):

        self._changed = changed
        if self.parent and changed is True:
            self.parent.changed = True

    @property
    def result(self):

        if not self._finished:
            raise Exception("Task not finished yet")

        return self._result

    @property
    def data(self):

        return self._data

    def get_messages(self, detail_level=1):

        msgs = []
        for level in sorted(self._messages.keys()):
            if level <= detail_level:
                temp = self._messages.get(level, None)
                if temp:
                    msgs.extend(temp)
        if not msgs:
            return ""
        return "\n".join(msgs)

    def get_error_messages(self, detail_level=1):

        msgs = []
        for level in sorted(self._error_messages.keys()):
            if level <= detail_level:
                temp = self._error_messages.get(level, None)
                if temp:
                    msgs.extend(temp)
        if not msgs:
            return ""
        return "\n".join(msgs)

    def add_result_msg(self, msg, detail_level=1):

        if isinstance(msg, string_types):
            msg = [msg]

        # TODO: add timestamp?
        for m in msg:
            self._messages.setdefault(detail_level, []).append(str(m))

    def add_result_error(self, error_msg, detail_level=1):

        if isinstance(error_msg, string_types):
            error_msg = [error_msg]

        for m in error_msg:
            self._error_messages.setdefault(detail_level, []).append(str(m))

    def _set_finished_state(
        self,
        success=None,
        skipped=None,
        changed=None,
        msg=None,
        error_msg=None,
        result=None,
    ):

        if self._finished:
            raise Exception("Task already finished.")

        if msg is not None:
            if isinstance(msg, string_types):
                self.add_result_msg(msg)
            elif isinstance(msg, Sequence):
                for m in msg:
                    self.add_result_msg(m)
            else:
                raise Exception("Invalid type '{}' for msg: {}".format(type(msg), msg))
        if error_msg is not None:
            if isinstance(error_msg, string_types):
                self.add_result_error(error_msg)
            elif isinstance(error_msg, Sequence):
                for m in error_msg:
                    self.add_result_error(m)
            else:
                raise Exception(
                    "Invalid type '{}' for error_msg: {}".format(type(msg), msg)
                )

        self.success = success
        self.skipped = skipped
        self.changed = changed
        self._result = result

    def pause(self):

        self._tasks.pause()

    def resume(self):

        self._tasks.resume()

    def finish(
        self,
        success=None,
        skipped=None,
        changed=None,
        msg=None,
        error_msg=None,
        result=None,
    ):

        self._set_finished_state(
            success=success,
            skipped=skipped,
            changed=changed,
            msg=msg,
            error_msg=error_msg,
            result=result,
        )

        parent = self._tasks.register_task_finished(self)
        return parent

    def add_subtask(
        self,
        task_name,
        category=None,
        msg=None,
        reference=None,
        ignore_errors=False,
        detail_level=0,
        data=None,
    ):

        child = self._tasks.task_started(
            self,
            task_name,
            category=category,
            msg=msg,
            reference=reference,
            ignore_errors=ignore_errors,
            detail_level=detail_level,
            data=data,
        )
        return child
