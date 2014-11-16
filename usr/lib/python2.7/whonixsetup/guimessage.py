#!/usr/bin/python

from PyQt4 import QtGui
from translations import Translations


class GuiMessage(QtGui.QMessageBox):
    def __init__(self, name):
        super(GuiMessage, self).__init__()

        tr = Translations('not_root')

        self.icon = tr.section.get('icon')

        self._ = tr.getText

        self.initUI()

    def initUI(self):
        self.setWindowIcon(QtGui.QIcon("/usr/share/icons/anon-icon-pack/whonix.ico"))

        self.setIcon(getattr(QtGui.QMessageBox, self.icon))

        self.setWindowTitle(self._('title'))

        self.setText(self._('message'))

        self.exec_()
