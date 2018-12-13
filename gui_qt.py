import clientele

import sys
import clientele
import os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QInputDialog, QFormLayout, QApplication, QPushButton, QLabel, QDialog, QLineEdit
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QListWidgetItem

clientlist = []
def guiexit():
    sys.exit()

def select_client(text):
    global window
    global clientlist
    for c in clientlist:
        if(c.name() == text):
            window.contact_name_field.setText(c.name())
            window.contact_email_field.setText(c.email())

def select_client_item(item):
    select_client(item.text())

def nametodirectory(name):
    for c in clientlist:
        if(c.name() == name):
            return c.dirname()

def new_client_dialog():
    dirname, ok = QInputDialog.getText(window, "New Client", "Client Directory Name", QLineEdit.Normal, "")
    if(ok):
        clientele.newclient(dirname)
        load_clients()
        select_client(dirname)

def delete_client_dialog():
    text, ok = QInputDialog.getText(window, "Delete Client", "WARNING, THIS IS IRREVERSABLE\nType \'delete\' to confirm",)
    if(ok and text=='delete'):
        items = window.client_listwidget.selectedItems()
        for i in items:
            clientele.deleteclient(nametodirectory(i.text()))
        load_clients()

def testbutton(item):
    print("button pressed" + item.text())

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
    app = QApplication(sys.argv)
    uifile = QFile("proto1.ui")
    uifile.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(uifile)
    load_clients()

    window.actionQuit.triggered.connect(guiexit)
    window.add_client_button.clicked.connect(new_client_dialog)
    window.delete_client_button.clicked.connect(delete_client_dialog)
    window.show()

    app.exec_()
