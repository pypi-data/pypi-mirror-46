#!/usr/bin/env python3
from IPython.core.magic import register_line_cell_magic
import ipywidgets as ip
import subprocess as sub
import pty
import tty
from select import select
import os
import sys
import re
from IPython.core.display import HTML, display, Javascript
from threading import Thread
from time import sleep

def bashin(cmd):
    textinput = ['']

    def settext(tf):
        textinput[0] = tf.value
        tf.value = ''

    pid = [-1]
    killed = [False]
    sig = [2]

    def kill_proc(button):
        if pid[0] >= 0:
            try:
                ret = os.killpg(pid[0],sig[0])
            except ProcessLookupError as pe:
                # Process is already dead, stop
                # trying to kill it
                pid[0] = -1
                return
            killed[0] = True
            if sig[0] == 2:
                sig[0] = 9

    status = ip.Label(value="Status: Running, Input:")
    textw = ip.Text()
    textw.on_submit(settext)
    outw = ip.Output()
    killb = ip.Button(description="Kill")
    killb.on_click(kill_proc)
    hb = ip.HBox([status,textw,killb])
    display(ip.VBox([hb,outw]))

    killed[0] = False
    m, s = pty.openpty()
    # For some reason, os.kill does not work.
    # Therefore we use setsid to make a process
    # group and use os.killpg
    proc = sub.Popen(cmd,
                     preexec_fn=os.setsid,
                     stdout=s,
                     stderr=s,
                     stdin=s,
                     bufsize=1,
                     close_fds=True)
    os.close(s)
    pid[0] = proc.pid
    n = 0
    with outw:
        while True:
             n += 1
             r, w, e = select([m],[],[],.5)
             if len(r) == 0 or n == 50:
                 # Unless this sleep statement executes,
                 # input text or buttons cannot be
                 # processed.
                 sleep(.01)
                 n = 0
             if killed[0]:
                 print(" ** Killed **")
                 break
             elif m in r:
                 try:
                    o = os.read(m,1)
                    sys.stdout.write(o)
                 except OSError as oe:
                    pass
             elif len(textinput[0])>0:
                 n=os.write(m,textinput[0].encode('ASCII')+b'\n')
                 textinput[0] = ''
             elif proc.poll() is None:
                 pass
             else:
                 break
    textw.disabled = True
    killb.disabled = True
    status.value = "Status: Done, Input:"

@register_line_cell_magic
def jbash(line,cell=None):
    tf = None
    if cell is None or cell.strip()=="":
        line = line.strip()
        if line == "bash":
            cmd = ["bash"]
        else:
            cmd = ["bash","-c",line]
    else:
        tf = os.environ["HOME"]+"/.temp_shell_%d.sh" % os.getpid()
        with open(tf,"w") as fd:
            print(cell,file=fd)
        cmd = ["bash",tf]
    t = Thread(target=bashin,args=(cmd,))
    t.start()

def load_ipython_extension(shell):
    shell.register_magic_function(jbash,'line_cell')
    #shell.register_magics(jbash)
