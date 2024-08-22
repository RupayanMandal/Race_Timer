import datetime

path='log.txt'

def read():
    with open(path,'+r') as logfile:
        msg=logfile.read()
        return msg
    
def readlines():
    with open(path,'+r') as logfile:
        msg=logfile.readlines()
        return msg    

def write(msg: str):
    with open(path,'+a') as logfile:
        if msg[0]=='\n':
            msg=msg[1:]
        if msg[-1]=='\n':
            msg=msg[0:len(msg)-1]    
        text='\n'+ str(datetime.datetime.now()) + " :: "+ msg + '\n'

        msg=logfile.write(text)
        return msg    
    
def writelines(msg: list):
    with open(path,'+a') as logfile:
        text=str(datetime.datetime.now()) + " :::: "
        logfile.write(text)
        logfile.writelines(msg)
        return msg    
    
def clearlogfile():
    with open(path,'+w') as logfile:
        logfile.write('')

def savelogfile():
    t=str(datetime.datetime.now())
    t=t.replace(':','_')
    t=t.replace(".",'_')
    t=t.replace("-",'_')
    t=t.replace(" ",'_')
    newfilepath='logfile_{}.txt'.format(t)
    with open(newfilepath,'+w') as newfile:
        newfile.write(read())
      
    
if __name__=='__main__':
    write('\nhello\n')    
    print(read())
    savelogfile()
















































    ## created by Rupayan Mandal ##