import json
import os
import shutil
emptydata = {

    "name": "empty",
    "email": "empty",
    "directory": "empty"

}
clientdir = '/home/tristan/src/Clientele/Clients'


class Client:
    def __init__(self, dirname):
        self.directory = clientdir + '/' + dirname + '/'
        self.data = loadfile(self.directory + "Client.json")

    def projects(self):
        return dirlist(self.directory)

    def name(self):
        return self.data['name']

    def email(self):
        return self.data['email']

    def dirname(self):
        return self.data['directory']

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
    print("Loading "+file.name)
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
