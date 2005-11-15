# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


from qt import *

import yali.users
from yali.gui.ScreenWidget import ScreenWidget
from yali.gui.setupuserswidget import SetupUsersWidget
import yali.gui.context as ctx

##
# Partitioning screen.
class Widget(SetupUsersWidget, ScreenWidget):

    def __init__(self, *args):
        apply(SetupUsersWidget.__init__, (self,) + args)

        self.pass_error.hide()
        self.createButton.setEnabled(False)

        self.connect(self.pass1, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)
        self.connect(self.pass2, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)
        self.connect(self.username, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)

        self.connect(self.createButton, SIGNAL("clicked()"),
                     self.slotCreateUser)

        self.connect(self.deleteButton, SIGNAL("clicked()"),
                     self.slotDeleteUser)


    def shown(self):
        ctx.screens.prevEnabled()

    def execute(self):
        for i in range(self.userList.count()):
            u = self.userList.item(i).getUser()
            u.addUser()

    def slotTextChanged(self):

        p1 = self.pass1.text()
        p2 = self.pass2.text()

        if p2 != p1:
            self.pass_error.show()
            self.pass_error.setAlignment(QLabel.AlignCenter)
            return self.createButton.setEnabled(False)
        else:
            self.pass_error.hide()


        if self.username.text() and self.pass1.text():
            self.createButton.setEnabled(True)
        else:
            self.createButton.setEnabled(False)

    def slotCreateUser(self):
        u = yali.users.User()
        u.username = self.username.text().ascii()
        u.passwd = self.pass1.text().ascii()

        i = UserItem(self.userList, user = u)

        # clear all
        self.username.clear()
        self.pass1.clear()
        self.pass2.clear()

        self.checkUsers()


    def slotDeleteUser(self):
        self.userList.removeItem(self.userList.currentItem())
        self.checkUsers()

    def checkUsers(self):
        if self.userList.count():
            ctx.screens.nextEnabled()
        else:
            ctx.screens.nextDisabled()


class UserItem(QListBoxText):

    ##
    # @param user (yali.users.User)
    def __init__(self, parent, user):
        apply(QListBoxText.__init__, (self,parent,user.username))
        self._user = user
    
    def getUser(self):
        return self._user

