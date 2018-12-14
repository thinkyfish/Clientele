import clientele

import sys
import clientele
import os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QInputDialog, QFormLayout, QApplication, QPushButton, QLabel, QDialog, QLineEdit
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QListWidgetItem
import PySide2
clientlist = []
projectlist = []


def guiexit():
    sys.exit()


def get_selected_client_item():
    items = window.client_listwidget.selectedItems()
    for i in items:
        return i


def get_client(text):
    for c in clientlist:
        print("client" + c.name() + "|" + c.dirname())
        if (text == c.name() or text == c.dirname()):
            return c


def update_name():
    item = window.client_listwidget.selectedItems()[0]
    c = get_client(item.text())
    if(c):
        text = window.contact_name_field.text()
        print("setting name:" + text)
        c.set_name(text)
        load_clients()
        item2 = window.client_listwidget.findItems(
            c.name(), PySide2.QtCore.Qt.MatchFixedString)[0]
        window.client_listwidget.setCurrentItem(item2)


def update_email():
    item = window.client_listwidget.selectedItems()[0]
    c = get_client(item.text())
    if(c):
        emailtext = window.contact_email_field.text()
        print("setting email:" + emailtext)
        c.set_email(emailtext)
        load_clients()
        item2 = window.client_listwidget.findItems(
            c.name(), PySide2.QtCore.Qt.MatchFixedString)[0]
        window.client_listwidget.setCurrentItem(item2)


def select_client(text):
    global window
    global clientlist
    for c in clientlist:
        if(c.name() == text):
            window.contact_name_field.setText(c.name())
            window.contact_email_field.setText(c.email())
            load_projects(c.name())
            


def select_client_item(item):
    select_client(item.text())


def nametodirectory(name):
    for c in clientlist:
        if(c.name() == name):
            return c.dirname()


def new_client_dialog():
    dirname, ok = QInputDialog.getText(
        window, "New Client", "Client Directory Name", QLineEdit.Normal, "")
    if(ok):
        clientele.newclient(dirname)
        load_clients()
        select_client(dirname)


def delete_client_dialog():
    text, ok = QInputDialog.getText(
        window, "Delete Client", "WARNING, THIS IS IRREVERSABLE\nType \'delete\' to confirm",)
    if(ok and text == 'delete'):
        items = window.client_listwidget.selectedItems()
        for i in items:
            clientele.deleteclient(nametodirectory(i.text()))
        load_clients()


def new_project_dialog():
    dirname, ok = QInputDialog.getText(
        window, "New Project", "Project Directory Name", QLineEdit.Normal, "")
    if(ok):
        citem = get_selected_client_item()
        for c in clientlist:
            if (c.name() == citem.text()):
                c.new_project(dirname)
                load_projects(c.name())


def delete_project_dialog():
    text, ok = QInputDialog.getText(
        window, "Delete Project", "WARNING, THIS IS IRREVERSABLE\nType \'delete\' to confirm",)
    if(ok and text == 'delete'):
        pitem = window.project_listwidget.selectedItems()[0]
        citem = get_selected_client_item()
        c = get_client(citem.text())
        c.delete_project(pitem.text())
        load_projects(c.name())


def select_project_item(item):
    global window
    global clientlist
    citem = get_selected_client_item()
    c = get_client(citem.text())
    plist = c.projects()
    for p in plist:
        if (p.name() == item.text() or p.dirname() == item.text()):
            window.project_name_field.setText(p.name())
            window.project_folder_field.setText(c.directory + '/' + p.dirname())


def testbutton(item):
    print("button pressed" + item.text())


def load_projects(clientname):
    global window
    window.project_listwidget.clear()
    for c in clientlist:
        if(c.name() == clientname):
            plist = c.projects()
            for p in plist:
                item = QListWidgetItem()
                item.setText(p.name())
                window.project_listwidget.addItem(item)
                window.project_listwidget.itemPressed.connect(
                    select_project_item)


def load_clients():
    global window
    global clientlist
    window.client_listwidget.clear()
    clientlist.clear()
    list = clientele.listclients()
    print(list)
    for client in list:
        print(client)
        c = clientele.Client(client)
        clientlist.append(c)
        item = QListWidgetItem()
        item.setText(c.name())
        window.client_listwidget.addItem(item)
        window.client_listwidget.itemPressed.connect(select_client_item)


if __name__ == "__main__":
    global window
    if (not os.path.isdir(clientele.clientdir)):
        os.mkdir(clientele.clientdir)
    app = QApplication(sys.argv)
    uifile = QFile("proto1.ui")
    uifile.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(uifile)
    load_clients()

    window.actionQuit.triggered.connect(guiexit)
    window.add_client_button.clicked.connect(new_client_dialog)
    window.delete_client_button.clicked.connect(delete_client_dialog)
    window.add_project_button.clicked.connect(new_project_dialog)
    window.delete_project_button.clicked.connect(delete_project_dialog)
    window.contact_name_field.returnPressed.connect(update_name)
    window.contact_name_field.editingFinished.connect(update_name)
    window.contact_email_field.returnPressed.connect(update_email)
    window.contact_email_field.editingFinished.connect(update_email)
    window.show()

    app.exec_()
