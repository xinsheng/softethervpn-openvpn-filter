import csv
import timeit
import socket,time
import base64

def writeStr2File(text, filePath):
    with open(filePath, 'w') as f:
        f.write(text)

def testIP(ip):
    t0 = time.time()
    t2 = 9999
    try:
        sock = socket.create_connection((ip,443), timeout=3)
        sock.close()
        t2 = time.time()-t0
    except Exception:
        t2 = 9999
    return t2

def saveDeadList(fileName,deads):
    f=open(fileName,'w')
    f.writelines(deads)
    f.close()

def loadDeadList():
    lines = []
    try:
        with open("_dead.list", "r") as f:
            while True:
                tmp = f.readline()
                if not tmp: 
                    break
                lines.append(tmp)
    except Exception:
        None
    return lines

DEADS = loadDeadList()
LIVES = []

with open('import.csv', mode='r', encoding='UTF-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if (len(row) == 1):
            break
        ip = row[None][0]
        if (ip+'\n') in DEADS:
            continue
        print(str(line_count)+' '+ip+'...')
        if len(ip) > 5:
            t2 = testIP(ip)
            if t2 < 3 :
                try:
                    LIVES.append(ip+'\n')
                    ovpn = row[None][13]
                    country = row[None][5].lower()
                    tmp = base64.b64decode(ovpn)
                    datastr = str(tmp, "utf-8")
                    strtime = "%.3f" % t2
                    writeStr2File(datastr, 'output-ovpn\\'+strtime+'-'+ip+'-'+country+'.ovpn')
                    print('\t'+str(line_count)+' '+ip+' -> '+ str(t2))
                except KeyError:
                    print('\tRead Error')
            else:
                DEADS.append(ip+'\n')
            #exit()
        line_count += 1

saveDeadList('_dead.list',DEADS)
saveDeadList('_live.list',LIVES)
print('Parsing Done')