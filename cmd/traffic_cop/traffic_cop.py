# -*- coding: utf-8 -*-
"""
Created on 01-07-2015 10:52

@author: seven
"""
import os
import signal
import sys
import time

killsig = signal.SIGKILL

stop_flag = False


def cop_log(*args, **kwargs):
    print args, kwargs


def init():
    init_signals()


def sig_term(signum, frame):
    cop_log("Entering sig_term(%d)\n", signum)
    # No code here yet...
    cop_log("Leaving sig_term(%d)\n", signum)


def sig_child(signum, frame):
    cop_log("Entering sig_child(%d)\n", signum)
    # No code here yet...
    cop_log("Leaving sig_child(%d)\n", signum)


def sig_fatal(signum, frame):
    cop_log("Entering sig_fatal(%d)\n", signum)
    # No code here yet...
    cop_log("Leaving sig_fatal(%d)\n", signum)


def sig_ignore(signum, frame):
    cop_log("Entering sig_ignore(%d)\n", signum)
    # No code here yet...
    cop_log("Leaving sig_ignore(%d)\n", signum)


def set_alarm_death():
    cop_log("Entering set_alarm_death()\n")
    signal.signal(signal.SIGALRM, sig_fatal)
    cop_log("Leaving set_alarm_death()\n")


def init_signals():
    # Handle the SIGTERM and SIGINT signal:
    # We kill the process group and wait() for all children
    signal.signal(signal.SIGINT, sig_term)
    signal.signal(signal.SIGTERM, sig_term)

    # Handle the SIGCHLD signal. We simply reap all children that
    # die (which should only be spawned traffic_manager's).
    signal.signal(signal.SIGCHLD, sig_child)

    # Handle a bunch of fatal signals. We simply call abort() when
    # these signals arrive in order to generate a core.
    signal.signal(signal.SIGQUIT, sig_fatal)
    signal.signal(signal.SIGILL, sig_fatal)
    signal.signal(signal.SIGFPE, sig_fatal)
    signal.signal(signal.SIGBUS, sig_fatal)
    signal.signal(signal.SIGSEGV, sig_fatal)
    # signal.signal(signal.SIGEMT, sig_fatal)
    signal.signal(signal.SIGSYS, sig_fatal)


    # Handle the SIGALRM signal. We use this signal to make sure the
    # cop never wedges. It gets reset every time through its loop. If
    # the alarm ever expires we treat it as a fatal signal and dump
    # core, secure in the knowledge we'll get restarted.
    set_alarm_death()

    signal.signal(signal.SIGPIPE, sig_ignore)

    cop_log("Leaving init_signals()\n")


def main():
    if stop_flag:
        cop_log("Cool! I think I'll be a STOP cop!")
        killsig = signal.SIGSTOP

    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    signal.signal(signal.SIGTTOU, signal.SIG_IGN)
    signal.signal(signal.SIGTTIN, signal.SIG_IGN)

    # system call
    # os.chdir("/")
    # os.umask(0)
    # break away from terminal
    # os.setsid()

    for f in sys.stdout, sys.stderr: f.flush()
    si = file('/dev/null', 'r')
    so = file('/dev/null', 'a+', 0)
    se = file('/dev/null', 'a+', 0)
    # os.dup2(si.fileno(), sys.stdin.fileno())
    # os.dup2(so.fileno(), sys.stdout.fileno())
    # os.dup2(se.fileno(), sys.stderr.fileno())

    init()

    while True:
        time.time()

    sys.exit(0)


if __name__ == '__main__':
    main()