twc
===

**TWC - TaskWarrior Controller** (previously TaskWarrior Curses) is interactive
terminal frontend for task and TODO manager - TaskWarrior.

.. image:: https://gitlab.com/mgoral/twc/raw/master/docs/img/screenshot.png
    :align: center

Features
~~~~~~~~

* agendas - display several filters on a single screen simultaneously
  (influenced by `org-mode <https:orgmode.org>`_)
* create, modify, delete, annotate tasks
* autocomplete and tab-complete writing task descriptions, annotations, tags
  etc.
* task formatting (with HTML-like markup)
* tasks and sub-tasks grouping (influenced by
  `taskwiki <https://github.com/tbabej/taskwiki>`_)
* synchronize tasks with task server
* status line showing arbitrary informations
* styling
* configurable key bindings
* search and incremental search of tasks
* search can be case-sensitive, case-insensitive or smart-case (case sensitivite
  only when there are upper case characters in searched term)

Introduction
~~~~~~~~~~~~

TWC works with a concept of "agendas" influenced and borrowed from the mighty
org-mode. Agenda is basically a view of several TaskWarrior filters (called
blocks) displayed on a single screen simultaneously. You can jump between
blocks and single tasks.

To add agenda, first create a configuration file inside
``~/.config/twc/config.py``. It is a regular Python file with exposed variable
``c`` which references a configuration object. You can add new blocks like that:

.. code:: python

    c.add_block(
        agenda='My Agenda',
        title='Next Tasks',
        filter='status:pending',
        sort='priority+,urgency-')

    c.add_block(
        agenda='My Agenda',
        title='Projects',
        filter='-WAITING and (+BLOCKING or +BLOCKED) and -INSTANCE',
        sort='project-,priority-,order+,urgency-',
        fmt='* {description}<info>{tags}</info>')

Style and colors
~~~~~~~~~~~~~~~~

TWC can be styled in any way you want. To change its colors use `c.set_style()`:

.. code:: python

    c.set_style('highlight', 'bg:ansiblue bold')
    c.set_style('error', 'fg:white bg:red')

First argument is style's name, second one is its definition.

Style examples:

- ``fg:white`` (white foreground, named color)
- ``bg:#000000`` (black background, hexadecimal notation)
- ``bg:ansiblue`` (blue background, ANSI color palette)
- ``bold italic underline blink reverse hidden`` (supported style flags)
- ``nobold noitalic noitalic`` (reverse flags)

Any style name can be used in task formatting. Some interface elements however
use specific style names.

The following styles are predefined:

- ``heading`` (default style of block headings)
- ``text``
- ``comment`` (style used for completed and deleted tasks)
- ``info`` (default style of additional informations, like list of tags)
- ``warning`` (default style of important informations)
- ``error`` (style used when displaying error messages)
- ``highlight`` (style used for highlighting current line/task)
- ``tabline`` (style used for tab line)
- ``tabsel`` (style used for currently selected tab)
- ``tab`` (style used for not selected tabs)
- ``tooltip`` (style used for various hints and tooltips)
- ``statusline`` (style used for status line)
- ``status.1`` (default style for some blocks in status line)
- ``status.2`` (other default style for some blocks in status line)

Task Format
~~~~~~~~~~~

Block's format (``fmt``) is a mix of `Python's string format
<https://docs.python.org/3/library/string.html#formatspec>`_ and HTML-like
markup.

You can use any TaskWarrior's attribute name as format's placeholder and it will
be displayed if present.

.. code:: html

    *<sr left=" ["> right="] ">{id}</sr>{description}

Some additional markup can be added to the tasks. The following tags are
available:

* ``<sr left="[", right="]>text</sr>``: surrounds text with *left* and *right*.
* ``<ind value="A">text</ind>``: if there is any text inside a tag, it will be
  replaced with *value*. It's particularily useful for indicating that some
  task's property is present, without displaying it (like long list of
  annotations):
  ``<sr left="[" right="]"><ind value="A">{annotations}</ind></sr>``

Keep in mind that no markup will be added if above tags surround empty text
(e.g. non-existent attribute).

Key bindings
~~~~~~~~~~~~

You can bind and unbind keys with ``c.bind(key, command)`` and
``c.unbind(key)``.

Key can have one of the following forms:

- ``x`` (single key)
- ``c-x`` (key with modifier (ctrl) pressed)
- ``c x`` (key sequence: press c, then press x)
- ``space tab enter`` (special key names)

Below are listed all available commands

Basic controls
++++++++++++++

- ``activate`` - initiate action: enter command, show task details etc. Defaults: ``enter``
- ``cancel`` - cancel current action. Defaults: ``escape``
- ``quit`` - exit TWC. Defaults: ``q``, ``Q``, ``c-c``

Moving around
+++++++++++++

- ``scroll-down`` - scroll down current screen/highlighted task. Defaults: ``down``, ``j``
- ``scroll-up`` - scroll up current screen/highlighted task. Defaults: ``up``, ``k``
- ``prev-block`` - jump to the previous block on current agenda. Defaults: ``pageup``, ``[``
- ``jump-begin`` - jump to the first line of current screen. Defaults: ``home``, ``g g``
- ``jump-end`` - jump to the last line of current screen. Defaults: ``end``, ``G``
- ``next-agenda`` - load next agenda. Defaults: ``tab``
- ``prev-agenda`` - load previous agenda. Defaults: ``s-tab``

Searching
+++++++++

- ``search`` - initiate search. Defaults: ``/``, ``c-f``
- ``find-next`` - finds next (forward) occurence of searched term. Defaults: ``n``
- ``find-prev`` - finds previous (backward) occurence of searched term. Defaults: ``N``

Controling tasks
++++++++++++++++
- ``add-task`` - creates a new task. Defaults: ``a``
- ``modify-task`` - modifies selected task. Defaults: ``m``
- ``annotate`` - adds new annotation. Defaults: ``A``
- ``denotate`` - removes existing annotation. Defaults: ``D``
- ``toggle-completed`` - marks selected task as completed. Defaults: ``a-space``
- ``delete-task`` - deletes selected task. Defaults: ``delete``
- ``undo`` - undo last action via ``task undo``. Defaults: ``u``
- ``synchronize`` - synchronize with taskd sync server. Defaults: ``S``
- ``refresh-agenda`` - reload all blocks and tasks in current agenda. Defaults: ``R``

Command line keys
+++++++++++++++++

When command line is opened (input field at the bottom of the screen, used e.g.
when task is being modified) some additional hard-coded key bindings are
available:

- ``tab`` - open window with available completions for current word. Use
  ``tab`` and ``s-tab`` to jump between them.
- ``escape``, ``c-c`` - cancel current command.

Status line
~~~~~~~~~~~

Bottom status line can display arbitrary informations and  is configurable by
two variables: ``statusleft`` and ``statusright``. They describe format similar
to the one described in `Task Format`_ The main difference is that task
attributes are referenced by ``{task.<attribute>}`` placeholder and that there
additional placeholders available.

.. code:: python

    c.set('statusleft', '{COMMAND} {task.id}')
    c.set('statusright', '<ind value=A>{task.annotations}</ind>')

Status line placeholders
++++++++++++++++++++++++

- ``taskrc`` - path of currently used taskrc
- ``command`` - name of current command, when command line is active (e.g. add,
  modify, annotate,...)
- ``COMMAND`` - same as before, but command is UPPER CASED
- ``task.<attribute>`` - any attribute of currently highlighted task
- ``agenda.pos`` - position of highlighted item
- ``agenda.size`` - size of current agenda
- ``agenda.ppos`` - percentage position of highlighted item

Installation
~~~~~~~~~~~~

First, make sure that TaskWarrior is installed on your system. TaskWarrior is
packaged for most of Linux distributions. Please refer to TaskWarrior's
`documentation <https://taskwarrior.org/download/>`_ for details.

TWC is distributed via `pypi <https://pypi.org/project/twc/>`_. You can
install it with pip:

.. code::

    $ pip3 install --user twc

or with pip wrapper like `pipsi <https://github.com/mitsuhiko/pipsi>`_:

.. code::

    $ pipsi install --python python3 twc

TWC reads your ``taskrc``. It'll use the default one, which is usually located
in ``~/.taskrc``, but you can change it with ``-t`` switch:

.. code::

    $ twc -t ~/dotfiles/my_taskrc

Termux
~~~~~~

TWC works on `Termux <https://termux.com/>`_, although there's currently a `bug
<https://github.com/regebro/tzlocal/pull/55>`_ in tzlocal - a library
indirectly used by TWC to get local timezone information.

Before running TWC on Termux you have to export the following environment
variable:

.. code:: shell

    export TZ=$(getprop persist.sys.timezone)

Termux emulates scroll events as key presses. You can bind them for easier
navigation:

.. code:: python

    c.bind('right', 'next-agenda')
    c.bind('left', 'prev-agenda')

License
~~~~~~~

TWC was created by Michał Góral.

TWC is free software, published under the terms of GNU GPL3 or any later
version. See LICENSE file for details.
