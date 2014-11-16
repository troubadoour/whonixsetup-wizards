#!/usr/bin/python

from PyQt4 import QtCore, QtGui
from subprocess import call
import os, inspect
from translations import Translations
from guimessage import GuiMessage


class WhonixRepositoryWizard(QtGui.QWizard):
    def __init__(self):
        super(WhonixRepositoryWizard, self).__init__()

        tr = Translations('whonix_repository')
        if not tr:
            ioerror = GuiMessage('not-root')
            sys.exist(127)
        # gettext like.
        self._ = tr.getText

        self.setupUi()

    def setupUi(self):
        self.resize(470, 310)
        self.setWindowTitle('Whonix Repository Wizard')
        icon = "/usr/share/icons/anon-icon-pack/whonix.ico"
        self.setWindowIcon(QtGui.QIcon(icon))

        self.pageEnable = QtGui.QWizardPage()
        self.enableText = QtGui.QLabel(self.pageEnable)
        self.enableText.setGeometry(QtCore.QRect(10, 10, 445, 150))
        self.enableText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.enableText.setWordWrap(True)
        self.enableGroup = QtGui.QGroupBox(self.pageEnable)
        self.enableGroup.setGeometry(QtCore.QRect(10, 180, 445, 60))
        self.enableButton = QtGui.QRadioButton(self.enableGroup)
        self.enableButton.setGeometry(QtCore.QRect(30, 10, 400, 21))
        self.enableButton.setChecked(True)
        self.disableButton = QtGui.QRadioButton(self.enableGroup)
        self.disableButton.setGeometry(QtCore.QRect(30, 30, 300, 21))
        self.addPage(self.pageEnable)

        self.pageRepos = QtGui.QWizardPage()
        self.repoText = QtGui.QLabel(self.pageRepos)
        self.repoText.setGeometry(QtCore.QRect(10, 10, 430, 140))
        self.repoText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.repoText.setWordWrap(True)
        self.repoGroup = QtGui.QGroupBox(self.pageRepos)
        self.repoGroup.setGeometry(QtCore.QRect(10, 150, 445, 90))
        self.repo1 = QtGui.QRadioButton(self.repoGroup)
        self.repo1.setGeometry(QtCore.QRect(30, 20, 300, 21))
        self.repo1.setChecked(True)
        self.repo2 = QtGui.QRadioButton(self.repoGroup)
        self.repo2.setGeometry(QtCore.QRect(30, 40, 300, 21))
        self.repo3 = QtGui.QRadioButton(self.repoGroup)
        self.repo3.setGeometry(QtCore.QRect(30, 60, 300, 21))
        self.addPage(self.pageRepos)

        self.pageFinish = QtGui.QWizardPage()
        self.finishText = QtGui.QLabel(self.pageFinish)
        self.finishText.setGeometry(QtCore.QRect(10, 10, 445, 140))
        self.finishText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.finishText.setWordWrap(True)
        self.addPage(self.pageFinish)

        message = self._('enabletext')
        self.enableText.setText(message)
        message = self._('repotext')
        self.repoText.setText(message)
        message = self._('enablebutton_text')
        self.enableButton.setText(message)
        message = self._('disablebutton_text')
        self.disableButton.setText(message)
        message = self._('finish_enabled')
        self.finish_text_disabled = message
        message = self._('finish_disabed')
        self.finish_text_enabled = message
        message = self._('finish_failed')
        self.finish_text_failed = message

        self.repoGroup.setTitle("Repository")
        self.repo1.setText("Whonix Stable Repository")
        self.repo2.setText("Whonix Testers Repository")
        self.repo3.setText("Whonix Developers Repository")

        # The event handler polls nextId() several times for the same page.
        # Send command once only.
        self.oneShot = True

        self.button(QtGui.QWizard.BackButton).clicked.connect(self.BackButton_clicked)

        self.exec_()

    # re-arm command.
    def BackButton_clicked(self):
        if not self.oneShot:
            self.oneShot = True

    # overload QWizard.nextId()
    def nextId(self):
        if self.currentId() < 2:
            if self.enableButton.isChecked():
                return self.currentId() + 1
            elif self.disableButton.isChecked():
                if self.oneShot:
                    command = 'whonix_repository --disable'
                    exit_code = call(command, shell=True)
                    mypath = inspect.getfile(inspect.currentframe())
                    if exit_code == 0:
                        self.finishText.setText(self.finish_text_disabled)
                        message = 'INFO %s: Ok, exit code of "%s" was %s.' % ( mypath, command, exit_code )
                    else:
                        error = '<p>ERROR %s: exit code of \"%s\" was %s.</p>' % ( mypath, command, exit_code )
                        finish_text_failed =  error + self.finish_text_failed
                        self.finishText.setText(finish_text_failed)
                        message = error
                    command = 'echo ' + message
                    call(command, shell=True)
                    self.oneShot = False
                return self.currentId() + 2
        elif self.currentId() == 2:
            if self.repo1.isChecked():
                codename = ' --codename stable'
            elif self.repo2.isChecked():
                codename = ' --codename testers'
            elif self.repo3.isChecked():
                codename = ' --codename developers'
            if self.oneShot:
                command = 'whonix_repository --enable' + codename
                exit_code = call(command, shell=True)
                mypath = inspect.getfile(inspect.currentframe())
                if exit_code == 0:
                    self.finishText.setText(self.finish_text_enabled)
                    message = "INFO %s: Ok, exit code of \"%s\" was %s." % ( mypath, command, exit_code )
                else:
                    error = '<p>ERROR %s: exit code of \"%s\" was %s.</p>' % ( mypath, command, exit_code )
                    finish_text_failed =  error + self.finish_text_failed
                    self.finishText.setText(finish_text_failed)
                    message = error
                command = 'echo ' + message
                call(command, shell=True)
                self.oneShot = False
            return -1
        else:
            return -1


#if __name__ == "__main__":
def main():
    import sys
    app = QtGui.QApplication(sys.argv)

    # root check.
    if os.getuid() != 0:
        print 'ERROR: This must be run as root!\nUse "kdesudo".'
        not_root = GuiMessage('not_root')
        sys.exit(1)

    wizard = WhonixRepositoryWizard()

    sys.exit()

if __name__ == "__main__":
    main()