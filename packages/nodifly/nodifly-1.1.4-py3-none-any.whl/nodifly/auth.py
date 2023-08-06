"""
Nodifly - Real time notifications
Usage:
------
    $ nodifly [your_file_here] [options]
Read one tutorial:

Examples:

Sending notifications to text:
    $ nodifly file_to_run.py -text

Sending notifications to email:
    $ nodifly file_to_run.py -email

Sending notifications to 
Available options are:
    -h, --help         Show this help
    -text               Send to phone associated
    -email              Send to email associated
    -record             Record only to database

Contact:
--------
- nodiflycontact@gmail.com
More information is available at:
- https://pypi.org/project/nodifly/
- https://github.com/stephenjhsu/nodifly

Version:
--------
- nodifly v1.0.6

"""

from subprocess import call
import sys
from IPython.core.magics.execution import _format_time
from IPython import get_ipython
import time
import requests 
import os
import csv

def check_system():
    if (sys.platform == 'win32') | (sys.platform == 'win64'):
        un = os.getenv('username')
        path = "C:/Users/"+str(un)+'/AppData/Local/Temp/'
    elif sys.platform == "darwin":
        path = '/tmp/'
    return path

def alert_type(starttime, endtime, duration, from_where, kind=None, alias='', key='', secret=''):
    if (kind != None) & (kind != 'email') & (kind != 'record') & (kind != 'text'):
        print("Did you mean to add a notification? Add 'email', 'text', or 'record' at the end")
    else:
        stimestr = str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(starttime)))
        etimestr = str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(endtime)))
        cellname = alias
        path = "https://nodifly.com/nodifly/"
        info = '/'.join([str(starttime),str(endtime),str(duration),
                        str(stimestr),str(etimestr),str(from_where),str(key),
                        str(secret)]) 

        if (cellname == None) | (cellname == ''):
            cellname = 'unnamed cell'
        if from_where == 'jupyter':
            scriptname = 'NULL'
            duration = str(duration).replace(" ", "")
            if kind == 'email':
                senttype = str(kind) 
                x = requests.post(path + info + '/' + senttype + '/' + cellname + '/' + scriptname).json()
                print('\033[1m' + x['escalate'] + '\033[0m')
            elif kind == 'text':
                senttype = str(kind)
                x = requests.post(path + info + '/' + senttype + '/' + cellname + '/' + scriptname).json()
                print('\033[1m' + x['escalate'] + '\033[0m')
            elif kind == 'record':
                senttype = str(kind)
                x = requests.post(path + info + '/' + senttype + '/' + cellname + '/' + scriptname).json()
                print('\033[1m' + x['escalate'] + '\033[0m')
        elif from_where == 'terminal':
            scriptname = str(alias)
            cellname = 'NULL'
            senttype = str(kind)
            x = requests.post(path + info + '/' + senttype + '/' + cellname + '/' + scriptname).json()

            print('Nodifly.com - Real time notification system')
            print('Program started at: ' + str(stimestr))
            print('Program finished at: ' + str(etimestr))
            print('Program took: ' + str(duration))
            print(x['escalate'])

def load_keys():
    """
    load keys from text file with form
    sender email, password, receiver email
    """
    path = check_system()
    filename= path + "nodoutput123ez.csv"
    with open(filename) as f:
        items = f.readline().strip().split(',')
        return items

        
def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    opts = [o for o in sys.argv[1:] if o.startswith("-")]

    if "-h" in opts or "--help" in opts:
        print(__doc__)
        return

    script_to_run = args[0]
    notif = opts[0][1:]

    starttime = time.time()

    call(["python", script_to_run, notif])
    endtime = time.time()
    diff = endtime - starttime

    nodifly_key, nodifly_secret = load_keys()

    alert_type(starttime=starttime, endtime=endtime, 
        duration=str(_format_time(diff)), from_where='terminal', 
        kind=notif, alias=script_to_run, key=nodifly_key, secret=nodifly_secret)

    path = check_system()
    filename= path + "nodoutput123ez.csv"
    if os.path.exists(filename):
        os.remove(filename)

class Cell(object):
    """ action cell events """

    def __init__(self, kind, alias, key, secret):
        self.start_time = None
        self.kind = kind
        self.start_time = time.time()
        self.alias = alias
        self.key = key
        self.secret = secret
    
    def post_run_cell(self):       
        if self.start_time:
            end_time = time.time()
            diff = end_time - self.start_time
            print('\033[1m' + 'Nodifly: nodifly.com' + '\033[0m')
            print('\033[1m' + 'Finished at: ' + '\033[0m' + 
                str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.start_time))))
            print('\033[1m'+ 'Duration: ' + '\033[0m' + str(_format_time(diff)))
            alert_type(starttime = self.start_time, endtime = end_time, 
                duration = str(_format_time(diff)), kind = self.kind, 
                alias=self.alias, from_where='jupyter', key=self.key, secret=self.secret)
        self.start_time = None

        path = check_system()
        filename = path + "nodoutput123ez.csv"
        if os.path.exists(filename):
            os.remove(filename)

class NodiflyAuth():
    def __init__(self, key, secret):

        self.key = key
        self.secret = secret
        path = check_system()
        filename= path + "nodoutput123ez.csv"
        
        if os.path.exists(filename):
            os.remove(filename)
        try:
            with open(filename, 'w') as resultFile:
                wr = csv.writer(resultFile, dialect='excel')
                wr.writerow([str(key), str(secret)])
        except:
            with open(filename, 'wb') as resultFile:
                wr = csv.writer(resultFile, dialect='excel')
                wr.writerow([str(key), str(secret)])
        
    def nodifly(self, kind=None, alias=''):
        """
        kinds = jupyter, cell, record
        """
        ip = get_ipython()
        global cell
        cell = Cell(kind, alias, self.key, self.secret)
        ip.events.register('post_run_cell', cell.post_run_cell)

    def alert(self, kind=None, alias=''):
        starttime = time.time()
        stimestr = str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(starttime)))
        etimestr = stimestr
        endtime = etimestr
        duration = '0 µs'
        from_where = 'immediate'

        scriptname = 'NULL'
        cellname = alias
        path = "https://nodifly.com/nodifly/"
        info = '/'.join([str(starttime),str(endtime),str(duration),
                        str(stimestr),str(etimestr),str(from_where),str(self.key),
                        str(self.secret)]) 
        
        x = requests.post(path + info + '/' + kind + '/' + cellname + '/' + scriptname).json()
        
        print('Nodifly.com - Real time notification system')
        print('Program finished at: ' + str(etimestr))
        print('\033[1m' + x['escalate'] + '\033[0m')