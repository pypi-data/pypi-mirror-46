#!/usr/bin/env python3
from IPython.core.magic import register_line_magic
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

textw = None
status = None
outw = None
killb = None
textinput = ''
pid = -1
killed = False

def kill_proc(button):
    global pid, killed
    if pid >= 0:
        sig = 2
        try:
            ret = os.killpg(pid,2)
        except ProcessLookupError as pe:
            return
        killed = True
        pid = -1

def settext(tf):
    global textinput
    textinput = tf.value
    tf.value = ''

def display_widgets():
    global outw, killb, status, textw
    status = ip.Label(value="Status: Running, Input:")
    textw = ip.Text()
    textw.on_submit(settext)
    outw = ip.Output()
    killb = ip.Button(description="Kill")
    killb.on_click(kill_proc)
    hb = ip.HBox([status,textw,killb])
    display(ip.VBox([hb,outw]))

def showtext(txt):
    print(txt,end='')

def bashin(cmd):
    global textinput, pid, killed, outw, killb, textw, status
    display_widgets()
    killed = False
    m, s = pty.openpty()
    # For some reason, os.kill does not work.
    # Therefore we use setsid to make a process
    # group and use os.killpg
    proc = sub.Popen(cmd,
                     preexec_fn=os.setsid,
                     stdout=s,
                     stderr=s,
                     stdin=s,
                     bufsize=0,
                     close_fds=True)
    pid = proc.pid
    n = 0
    with outw:
        while True:
             n += 1
             r, w, e = select([m],[m],[],.5)
             if len(r) == 0 or n == 50:
                 sleep(.01)
                 n = 0
             if killed:
                 showtext(" ** Killed **")
                 break
             elif m in r:
                 o = os.read(m,1)
                 sys.stdout.write(o)
             elif len(textinput)>0:
                 n=os.write(m,textinput.encode('ASCII')+b'\n')
                 textinput = ''
             elif proc.poll() is None:
                 pass
             else:
                 break
    textw.disabled = True
    killb.disabled = True
    status.value = "Status: Done, Input:"

@register_line_magic
def jbash(cmd):
    cmd = cmd.strip()
    if cmd == "bash":
        cmd = ["bash"]
    else:
        cmd = ["bash","-c",cmd.strip()]
    t = Thread(target=bashin,args=(cmd,))
    t.start()

def load_ipython_extension(shell):
    shell.register_magic_function(jbash,'line')
