# Copyright (C) 2019 Michał Góral.
#
# This file is part of TWC
#
# TWC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TWC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TWC. If not, see <http://www.gnu.org/licenses/>.

import asyncio
import concurrent.futures
import itertools
import attr

from prompt_toolkit.layout.screen import Point
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window, ScrollOffsets
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import to_formatted_text

import twc.markup as markup
import twc.twutils as twutils
import twc.signals as signals
from twc.commands import event_to_controller
from twc.locale import tr
from twc.utils import pprint, eprint
from .completions import task_add, task_modify, annotations

_HEADING_MARKER = ('[heading]', '')
_NL = ('', '\n')


@attr.s
class _CacheEntry:
    _text = attr.ib(None)
    _task = attr.ib(None)
    _fmt = attr.ib(None)

    @property
    def text(self):
        if self._text:
            return self._text
        if self._task and self._fmt:
            text = self._fmt.format_map(self._task)
            self._text = markup.parse_html(text)
            return self._text
        return ''

    @property
    def task(self):
        return self._task

    def invalidate(self):
        # Only invalidate when we'll be able to reconstruct cache
        if self._fmt and self._task:
            self._text = None


class TaskDetails:
    def __init__(self, task, tw, cfg):
        self.task = task
        self.tw = tw
        self.cfg = cfg

        result = twutils.execute_command(self.tw, 'info', flt=self.task)
        self.text = result.verified_out()
        self._pos = 0

        self.control = FormattedTextControl(
            self._get_text_fragments,
            get_cursor_position=lambda: Point(0, self.pos),
            key_bindings=self.keys(),
            focusable=True,
            show_cursor=False)

        self.window = Window(
            content=self.control,
            scroll_offsets=ScrollOffsets(top=1, bottom=1),
            wrap_lines=True)

    def keys(self):
        kb = KeyBindings()

        @self.cfg.command_handler('cancel', kb)
        @event_to_controller
        def _(controller):
            if controller.stack and controller.stack[-1] is self:
                controller.pop()

        @self.cfg.command_handler('scroll-down', kb)
        def _(event):
            info = self.window.render_info
            height = info.window_height
            vs = info.vertical_scroll

            # substract 1 due to scroll offsets
            self.pos = vs + height - 1

        @self.cfg.command_handler('scroll-up', kb)
        def _(event):
            info = self.window.render_info
            vs = info.vertical_scroll

            # don't add 1 due to scroll offsets
            self.pos = vs

        @self.cfg.command_handler('jump-begin', kb)
        def _(event):
            self.pos = 0

        @self.cfg.command_handler('jump-end', kb)
        def _(event):
            self.pos = len(self.text) - 1

        return kb

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, val):
        if 0 <= val < len(self.text):
            self._pos = val

    def _get_text_fragments(self):
        result = []
        for line in self.text:
            ft = to_formatted_text(line)
            result.extend(ft)
            result.append(_NL)
        return result

    def __pt_container__(self):
        return self.window


def extract(block, tw):
    tasks = twutils.filter_tasks(block.filter, tw)
    twutils.sort_tasks(tasks, block.sort)

    if block.limit is not None:
        tasks = tasks[:block.limit]

    return twutils.group_tasks(tasks)


def _process_tasks(tasks, fmt):
    markups = []
    for task in twutils.dfs(list(tasks.values())):
        indent = ' ' * task.depth * 2
        entry_fmt = indent + fmt

        entry = _CacheEntry(task=task, fmt=entry_fmt)
        markups.append(entry)
    return markups


def _process_block(block, tw):
    cache = []
    heading = [_HEADING_MARKER] + markup.parse_html(block.title)
    cache.append(_CacheEntry(text=heading))

    tasks = extract(block, tw)
    task_cache = _process_tasks(tasks, block.fmt)
    cache.extend(task_cache)
    return cache


def _process_blocks(blocks, tw):
    cache = []
    for block in blocks:
        cache.extend(_process_block(block, tw))
    return cache


def _process_blocks_concurrently(blocks, tw):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(_process_block, block, tw)
                   for block in blocks]

    concurrent.futures.wait(futures)
    cache = []
    for fut in futures:
        cache.extend(fut.result())
    return cache


class AgendaView:
    def __init__(self, tw, cfg):
        self.tw = tw
        self.cfg = cfg
        self.cpos = 0
        self._pos = -1
        self._searchstr = None
        self._cache = []
        self._current = None
        self._agendas = list(self.cfg.agendas.keys())

        # signals
        self.agenda_changed = signals.signal('agenda_changed')
        self.scrolled = signals.signal('scrolled')

        self.control = FormattedTextControl(
            self._get_text_fragments,
            get_cursor_position=lambda: Point(0, self.cpos),
            key_bindings=self.keys(),
            focusable=True,
            show_cursor=False)

        self.window = Window(
            content=self.control,
            scroll_offsets=ScrollOffsets(top=1, bottom=1))

    # pylint: disable=too-many-statements
    def keys(self):
        kb = KeyBindings()

        @self.cfg.command_handler('next-agenda', kb)
        def _(event):
            if len(self._agendas) > 1:
                idx = self._agendas.index(self._current)
                idx = (idx + 1) % len(self._agendas)
                self.reset_agenda(self._agendas[idx])

        @self.cfg.command_handler('prev-agenda', kb)
        def _(event):
            if len(self._agendas) > 1:
                idx = self._agendas.index(self._current)
                idx = (idx + -1) % len(self._agendas)
                self.reset_agenda(self._agendas[idx])

        @self.cfg.command_handler('add-task', kb)
        @event_to_controller
        def _(controller):
            asyncio.ensure_future(self._add(controller))

        @self.cfg.command_handler('modify-task', kb)
        @event_to_controller
        def _(controller):
            asyncio.ensure_future(self._modify(controller))

        @self.cfg.command_handler('annotate', kb)
        @event_to_controller
        def _(controller):
            asyncio.ensure_future(self._annotate(controller))

        @self.cfg.command_handler('denotate', kb)
        @event_to_controller
        def _(controller):
            asyncio.ensure_future(self._denotate(controller))

        @self.cfg.command_handler('toggle-completed', kb)
        @event_to_controller
        def _(controller):
            self._toggle_complete(controller)

        @self.cfg.command_handler('delete-task', kb)
        @event_to_controller
        def _(controller):
            self._delete(controller)

        @self.cfg.command_handler('synchronize', kb)
        @event_to_controller
        def _(controller):
            asyncio.ensure_future(self._sync(controller))

        @self.cfg.command_handler('activate', kb)
        @event_to_controller
        def _(controller):
            task = self.current_task
            if not task:
                return

            details = TaskDetails(task, self.tw, self.cfg)
            controller.push(details)

        @self.cfg.command_handler('cancel', kb)
        @event_to_controller
        def _(controller):
            controller.commandline.clear()

        @self.cfg.command_handler('refresh-agenda', kb)
        @event_to_controller
        def _(controller):
            self.refresh()
            pprint(tr('Agenda refreshed'))

        @self.cfg.command_handler('undo', kb)
        @event_to_controller
        def _(controller):
            self.tw.undo()
            pprint(tr('Changes reverted'))
            self.refresh()

        @self.cfg.command_handler('scroll-down', kb)
        def _(event):
            self.scroll(1)

        @self.cfg.command_handler('scroll-up', kb)
        def _(event):
            self.scroll(-1)

        @self.cfg.command_handler('next-block', kb)
        def _(event):
            self.scroll(1)
            while not self.is_heading(self.pos - 1) and self.scroll(1):
                pass

        @self.cfg.command_handler('prev-block', kb)
        def _(event):
            self.scroll(-1)
            while not self.is_heading(self.pos - 1) and self.scroll(-1):
                pass

        @self.cfg.command_handler('jump-begin', kb)
        def _(event):
            self._reset_pos()
            self.scroll(1)

        @self.cfg.command_handler('jump-end', kb)
        def _(event):
            self.pos = len(self._cache)
            self.scroll(-1)

        @self.cfg.command_handler('search', kb)
        @event_to_controller
        def _(controller):
            if self.cfg.settings.incsearch:
                asyncio.ensure_future(self._incsearch(controller))
            else:
                asyncio.ensure_future(self._search(controller))

        @self.cfg.command_handler('find-next', kb)
        @event_to_controller
        def _(controller):
            if self._searchstr:
                pos = self.find(self._searchstr, forward=True, curr_line=False)
                if pos is not None:
                    self.pos = pos
                else:
                    eprint(tr('Not found: {}').format(self._searchstr))

        @self.cfg.command_handler('find-prev', kb)
        @event_to_controller
        def _(controller):
            if self._searchstr:
                pos = self.find(self._searchstr, forward=False, curr_line=False)
                if pos is not None:
                    self.pos = pos
                else:
                    eprint(tr('Not found: {}').format(self._searchstr))

        return kb

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, val):
        if val != self._pos:
            self._pos = val
            if 0 <= self._pos < len(self._cache):
                self.scrolled.emit(val)

    def refresh(self):
        curr_task = self.current_task
        self.reset_agenda(keep_pos=True)

        for i, ce in enumerate(self._cache):
            if ce.task and ce.task == curr_task:
                self.pos = i
                break
        else:
            if not self.is_task(self.pos) and not self.scroll(-1):
                self._reset_pos()

    def reset_agenda(self, name=None, keep_pos=False):
        self._cache = []

        if name:
            self._current = name

        if not keep_pos:
            self._reset_pos()

        agenda = self.current_agenda
        if len(agenda.blocks) > 2:
            self._cache = _process_blocks_concurrently(agenda.blocks, self.tw)
        else:
            self._cache = _process_blocks(agenda.blocks, self.tw)

        self.agenda_changed.emit(self._current)

    @property
    def current_task(self):
        if self.is_task(self.pos):
            return self._cache[self.pos].task
        return None

    @property
    def current_agenda(self):
        if self._current:
            return self.cfg.agendas[self._current]
        return None

    def scroll(self, step):
        '''Scroll current `pos` in any direction, omitting headings.'''
        if step == 0:
            return True

        pos = self.pos
        while True:
            pos += step

            # Nothing more awaits us in that direction. Revert to the
            # original pos
            if (step < 0 and pos < 0) or \
                    (step > 0 and pos >= len(self._cache)):
                return False

            if self.is_task(pos):
                self.pos = pos
                return True

    @property
    def _current_cache(self):
        return self._cache[self.pos]

    async def _add(self, controller):
        controller.commandline.command = 'add'
        controller.commandline.set_help(tr('New task +tag proj:foo'))

        with controller.focused(controller.commandline):
            command = await controller.commandline.read_command(
                compl=task_add(self.tw))

        if not command:
            return

        result = twutils.execute_command(self.tw, 'add', command)
        if not result.report_failure():
            pprint(tr('Created new task'))
            self.refresh()

    async def _modify(self, controller):
        task = self.current_task
        if not task:
            return

        controller.commandline.command = 'modify'
        controller.commandline.set_help(tr('Change description +tag proj:foo'))

        with controller.focused(controller.commandline):
            args = await controller.commandline.read_command(
                compl=task_modify(task, self.tw))

        if not args:
            return

        result = twutils.execute_command(self.tw, 'modify', args, flt=task)
        if not result.report_failure():
            self.refresh()

    async def _annotate(self, controller):
        task_cache = self._current_cache
        task = task_cache.task
        if not task:
            return

        controller.commandline.command = 'annotate'
        controller.commandline.set_help(tr('New annotation'))

        with controller.focused(controller.commandline):
            annotation = await controller.commandline.read_command()

        if not annotation:
            return

        task.t.add_annotation(annotation)
        task_cache.invalidate()

    async def _denotate(self, controller):
        task_cache = self._current_cache
        task = task_cache.task
        if not task:
            return

        if not task.t['annotations']:
            return

        controller.commandline.command = 'denotate'
        controller.commandline.set_help(tr('Text of existing annotation'))

        task_annotations = annotations(task)
        with controller.focused(controller.commandline):
            annotation = await controller.commandline.read_command(
                compl=task_annotations)

        if not annotation:
            return

        if annotation not in task_annotations:
            eprint(tr('Task not annotated with "{}"').format(annotation))
            return

        task.t.remove_annotation(annotation)
        task_cache.invalidate()

    def _toggle_complete(self, controller):
        task_cache = self._current_cache
        task = task_cache.task
        if not task:
            return

        if task.t.completed or task.t.deleted:
            twutils.execute_command(
                self.tw, 'modify', 'status:pending', flt=task)
            task.t.refresh()
        else:
            task.t.done()
            task.t.save()
        task_cache.invalidate()

    def _delete(self, controller):
        task_cache = self._current_cache
        task = task_cache.task
        if not task:
            return

        task.t.delete()
        task.t.save()
        task_cache.invalidate()

    async def _sync(self, controller):
        pprint(tr('Tasks synchronizing...'))

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, twutils.execute_command, self.tw, 'sync')

        if not result.successful:
            stderr = '\n'.join(result.stderr_no_overrides)
            eprint(stderr)
        else:
            pprint(tr('Synchronization finished successfully. Please refresh.'))
        controller.app.invalidate()

    async def _search(self, controller):
        controller.commandline.command = 'search'

        with controller.focused(controller.commandline):
            searchstr = await controller.commandline.read_command(prompt='/')

        if searchstr:
            self._searchstr = searchstr
            pos = self.find(self._searchstr)
            if pos is not None:
                self.pos = pos
            else:
                eprint(tr('Not found: {}').format(self._searchstr))

    async def _incsearch(self, controller):
        controller.commandline.command = 'search'

        pos_before_search = self.pos
        found = False

        def _find(searched):
            nonlocal found

            pos = self.find(searched)
            if pos is not None:
                self.pos = pos
                found = True
            else:
                self.pos = pos_before_search
                found = False

        with controller.focused(controller.commandline):
            controller.commandline.text_changed.connect(_find)
            searchstr = await controller.commandline.read_command(prompt='/')
            controller.commandline.text_changed.disconnect(_find)

        if not searchstr:
            self.pos = pos_before_search
        else:
            self._searchstr = searchstr
            if not found:
                eprint(tr('Not found: {}').format(self._searchstr))

    @property
    def size(self):
        return len(self._cache)

    def is_task(self, pos):
        return (0 <= pos < len(self._cache)
                and self._cache[pos]
                and self._cache[pos].task)

    def is_heading(self, pos):
        return (0 <= pos < len(self._cache)
                and self._cache[pos]
                and self._cache[pos].text
                and self._cache[pos].text[0] == _HEADING_MARKER)

    def find(self, searched, forward=True, curr_line=True):
        # curr_line includes current line in search: only adds/substracts
        # lines to startpos when it's False. It's used by incsearch, when
        # we don't want to jump to the next match when current line still holds
        # one.
        line_add = int(not curr_line)

        if forward:
            startpos = self.pos + line_add
            if 0 >= startpos >= len(self._cache):
                startpos = 0

            search_range = itertools.chain(
                range(startpos, len(self._cache)),
                range(0, startpos))
        else:
            startpos = self.pos - line_add
            if 0 >= startpos >= len(self._cache):
                startpos = len(self._cache) - 1

            search_range = itertools.chain(
                range(startpos, 0, -1),
                range(len(self._cache) - 1, startpos, -1))

        settings = self.cfg.settings
        ignorecase = settings.ignorecase
        if ignorecase and settings.smartcase and not searched.islower():
            ignorecase = False

        if ignorecase:
            searched = searched.lower()

        for pos in search_range:
            ce = self._cache[pos]
            if not self.is_task(pos) or not ce.text:
                continue

            for _, text in ce.text:
                if ignorecase:
                    text = text.lower()
                if searched in text:
                    return pos
        return None

    def _reset_pos(self):
        # Carefully selected integer :)
        self.pos = -1
        self.cpos = 0

    def _get_text_fragments(self):
        result = []

        cpos_add = 0

        for i, entry in enumerate(self._cache):
            task = entry.task
            ft = entry.text

            # Additional newline before heading needs special treatment with
            # prompt_toolkit's cursor position, as it introduces inconsistency
            # with self.pos. Cache doesn't have bare-newline entries.
            if not task and self.is_heading(i):
                result.append(_NL)
                cpos_add += 1

            if task and task['status'] in ('completed', 'deleted'):
                ft = to_formatted_text(ft, style='class:comment')

            if i == self.pos:
                self.cpos = i + cpos_add
                ft = to_formatted_text(ft, style='class:highlight')

            result.extend(ft)
            result.append(_NL)

        return result

    def __pt_container__(self):
        return self.window
