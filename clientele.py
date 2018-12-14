import json
import os
import shutil
emptydata = {

    "name": "empty",
    "email": "empty",
    "directory": "empty"

}
emptyproject = {

    "name": "empty",
    "directory": "empty"

}
clientdir = os.environ['HOME'] + '/clients'

class Project:
    def __init__(self, parentdir, dirname):
        self.directory = clientdir + '/' + parentdir + '/' + dirname
        self.data = loadfile(self.directory + "/Project.json")

    def name(self):
        return self.data['name']

    def dirname(self):
        return self.data['directory']

class Client:
    def __init__(self, dirname):
        self.directory = clientdir + '/' + dirname
        self.data = loadfile(self.directory + "/Client.json")

    def projects(self):
        p = []
        for d in dirlist(self.directory):
            p.append(Project(self.dirname(), d))
        return p

    def name(self):
        return self.data['name']

    def set_name(self, text):
        self.data['name'] = text
        self.write()

    def email(self):
        return self.data['email']

    def set_email(self, text):
        self.data['email'] = text
        self.write()

    def dirname(self):
        return self.data['directory']

    def write(self):
        file = open(self.directory + "/Client.json", "w")
        json.dump(self.data, file)

    def new_project(self, dirname):
        fulldir = self.directory + '/' + dirname
        if(not os.path.isdir(fulldir)):
            os.mkdir(fulldir)
            with open(fulldir + "/Project.json", "w") as write_file:
                newdata = emptyproject.copy()
                newdata['directory'] = dirname
                newdata['name'] = dirname
                json.dump(newdata, write_file)

    def delete_project(self, name):
        for p in self.projects():
            if(p.name() == name or p.directory() == name):
                fulldir = self.directory + '/' + p.data['directory']
                if(os.path.isdir(fulldir)):
                    shutil.rmtree(fulldir)
                    print("deleted:"+fulldir)

def newclient(dirname):
    fulldir = clientdir + '/' + dirname
    if(not os.path.isdir(fulldir)):
        os.mkdir(fulldir)
        with open(fulldir + "/Client.json", "w") as write_file:
            newdata = emptydata.copy()
            newdata['directory'] = dirname
            newdata['name'] = dirname
            json.dump(newdata, write_file)


def deleteclient(dirname):
    fulldir = clientdir + '/' + dirname
    if(os.path.isdir(fulldir)):
        shutil.rmtree(fulldir)
        print("deleted:"+fulldir)


def loadfile(filename):
    file = open(filename, 'r')
    print("Loading "+ file.name)
    data = json.load(file)
    file.close()
    return data


def dirlist(dir):
    ls = os.listdir(dir)
    dirs = []
    for file in ls:
        if(os.path.isdir(dir+'/'+file)):
            dirs.append(file)
    return dirs


def getname(client):
    data = loadfile(clientdir+'/'+client+'/Client.json')
    return data['name']


def listclients():
    print('clientdir: ' + clientdir)
    return dirlist(clientdir)


def testwrite():
    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)
