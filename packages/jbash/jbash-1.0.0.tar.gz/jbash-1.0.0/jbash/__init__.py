#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys
import select
import termios
import tty
import pty
from subprocess import Popen
from IPython.core.magic import register_line_magic

# Module written with help from this web page:
# https://stackoverflow.com/questions/9673730/interacting-with-bash-from-python

# Note:
# sbrandt:~$ cat ~/.ipython/profile_default/startup/load_extensions.py
# get_ipython().run_line_magic('load_ext','interact')

@register_line_magic
def ibash(line):
    line = line.strip()
    wait = 0.5
    g = re.match(r'^\s*([\d\.]+)\s+(.*)',line)
    if g:
        wait = float(g.group(1))
        line = g.group(2)
    command = ["bash","-c",line]
    if line in ["bash",""]:
        command = ["bash"]

    # open pseudo-terminal to interact with subprocess
    master_fd, slave_fd = pty.openpty()
    tty.setraw(slave_fd)

    # use os.setsid() make it run in a new process group,
    # or bash job control will not be enabled and an
    # annoying warning message will be printed at shell
    # startup.
    p = Popen(command,
              preexec_fn=os.setsid,
              stdin=slave_fd,
              stdout=slave_fd,
              stderr=slave_fd,
              bufsize=0,
              universal_newlines=True)

    os.close(slave_fd)

    buf = ''
    while True:
        r, w, e = select.select([master_fd], [], [], wait)
        if master_fd in r:
            try:
                o = os.read(master_fd, 1)
                buf += o.decode('ASCII')
            except OSError as oe:
                if p.poll() is not None:
                    # This happens if exit is
                    # called from within a shell.
                    break
        elif len(buf) > 0:
            if p.poll() is None:
                try:
                    d = input(buf)+'\n'
                except KeyboardInterrupt as ke:
                    break
                except EOFError as ee:
                    break
                buf = ''
                os.write(master_fd,d.encode('ASCII'))
            else:
                break

    print(buf,end='')

def load_ipython_extension(shell):
    shell.register_magic_function(ibash, 'line')
