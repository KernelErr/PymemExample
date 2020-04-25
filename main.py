import pymem
import re
import logging


pm = pymem.Pymem()
pmlogger = logging.getLogger('pymem')
pmlogger.setLevel(logging.WARNING)
memSave = []
pid = input("[*] Input PID:")
try:
    pm.open_process_from_id(int(pid))
    print("[*] Opened process successfully.\n\n[*]Trying to list modules.")
    print("="*20)
    modules = pm.list_modules()
    for i in modules:
        print(i.name)
    print("="*20)
    print()
except pymem.exception.CouldNotOpenProcess:
    print("[!] Couldn't open specified process.")
    exit()
else:
    try:
        moduleName = input("[*] Input modules name:")
        client = pymem.process.module_from_name(pm.process_handle, moduleName)
        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)
        varValue = input("[*] Input value to search:")
        memiter = re.finditer(int(100).to_bytes(length=4, byteorder="little"), clientModule)
        for i in memiter:
            if(pm.read_int(client.lpBaseOfDll + i.start()) == 100):
                memSave.append(i.start())
        print("[*] Find %d addresses.\n" % len(memSave))
        while 1:
            varValue = input("[*] Input value to update:")
            memUpdate = []
            for i in memSave:
                if pm.read_int(client.lpBaseOfDll + i) == int(varValue):
                    memUpdate.append(i)
            memSave.clear()
            memSave = memUpdate
            print("[*] Find %d addresses." % len(memSave))
            if(len(memSave) == 1):
                print("[*] Target found!\n")
                break
        while 1:
            varChange = input("[*] Input value to change:")
            for i in memSave:
                try:
                    print("[*] Change address %s from %s to %s." % (hex(client.lpBaseOfDll + i), pm.read_int(client.lpBaseOfDll + i), varChange))
                    pm.write_int(client.lpBaseOfDll + i, int(varChange))
                except:
                    print("[!] Failed to write value to address %s." % hex(client.lpBaseOfDll + i))
    except pymem.exception.ProcessError:
        print("[!] Couldn't open specified process.")
        exit()
    except pymem.exception.MemoryReadError:
        print("[!] Couldn't read mem.")
        exit()