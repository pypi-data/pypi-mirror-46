# coding=utf-8
import sys, curses

LBL_CURR_TASK = 'Status:'

class UI(object):
    def __init__(self):
        self.stdout = sys.stdout
        stdscr = curses.initscr()
        curses.curs_set(0) # invisible cursor
        max_y, max_x = stdscr.getmaxyx()
        stdscr.addstr('WalT server console', curses.A_BOLD | curses.A_UNDERLINE)
        stdscr.subwin(1, max_x, 2, 0).addstr(LBL_CURR_TASK, curses.A_BOLD)
        offset_x = len(LBL_CURR_TASK)+1
        self.task_label_win = stdscr.subwin(1, max_x-offset_x, 2, offset_x)
        self.task_explain_win = stdscr.subwin(4, 0)
        self.BOX_DRAWING={
            u'┼': curses.ACS_PLUS,
            u'┌': curses.ACS_ULCORNER,
            u'─': curses.ACS_HLINE,
            u'│': curses.ACS_VLINE,
            u'┐': curses.ACS_URCORNER,
            u'┘': curses.ACS_LRCORNER,
            u'└': curses.ACS_LLCORNER
        }
        stdscr.refresh()
    def cleanup(self):
        curses.endwin()
    def task_start(self, msg, explain=None):
        self.task_idx = 0
        self.task_msg = msg
        self.task_explain = explain
        if not self.task_explain:
            self.task_explain_win.erase()
    def task_running(self):
        if self.task_explain:
            self.set_win_text(self.task_explain_win, self.task_explain)
            self.task_explain = None    # display only once
        self.set_win_text(self.task_label_win, "%s %s" % \
                (self.task_msg, '|/-\\'[self.task_idx]))
        self.task_idx = (self.task_idx + 1)%4
    def set_win_text(self, win, text):
        win.erase()
        with open('/tmp/log', 'w') as log:
            for c in text:
                log.write('%s %s\n' % (repr(c), repr(self.BOX_DRAWING)))
                if c in self.BOX_DRAWING:
                    c = self.BOX_DRAWING[c]
                else:
                    c = str(c)
                win.addch(c)
        win.refresh()
    def task_done(self):
        self.set_win_text(self.task_label_win, \
                    "%s %s" % (self.task_msg, 'done'))

