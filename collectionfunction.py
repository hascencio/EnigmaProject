def collectionfunction (ipAddress):

    import pexpect

    username = "hascencio"  # Username Example
    password = "Claro19+"  # PasswordU Example
    cmd_1 = 'show interfaces description | exclude "[.]" | include "Gi|Te" '
    print (cmd_1)
    cmd_2 = "show platform | in CPU | ex RSP"
    hostname = ipAddress
    print (hostname)
    print (ipAddress)
    array_modulos=[]
    try:
        C_10GSE = 0
        C_10GTR = 0
        C_1GSE = 0
        C_1GTR = 0
        print 'telnet ' + hostname
        child = pexpect.spawn('telnet ' + hostname, timeout=220)
        child.expect('[uU]sername:')
        child.sendline(username)
        child.expect('[pP]assword:')
        child.sendline(password)
        child.expect('#')
        child.sendline('terminal length 0')
        child.expect('#')
        child.sendline(cmd_1)
        child.expect('#')
        interfaces= str(child.before)
        interfaces_list=interfaces.split("\r\n")
        child.sendline(cmd_2)
        child.expect("#")
        modulos = str(child.before)
        modulos_list= modulos.split("\r\n")
        child.close()
        for mod in modulos_list:
            aux=mod.split()
            linea = aux[0]
            if ("0/" in linea) and ("RSP" not in linea):
                index=int (linea[2])
                if "SE" in aux[1]:
                    array_modulos.insert(index,"SE")
                elif "TR" in aux[1]:
                    array_modulos.insert(index, "TR")
        for i in range(2, len(interfaces_list)):
            interface = interfaces_list[i]
            if "RSP" not in interface:
                indice = int(interface[4])
                if "Te" in interface:
                    if "SE" in array_modulos[indice]:
                        C_10GSE += 1
                    if "TR" in array_modulos[indice]:
                        C_10GTR += 1
                elif "Gi" in interface:
                    if "SE" in array_modulos[indice]:
                        C_1GSE += 1
                    if "TR" in array_modulos[indice]:
                        C_1GTR += 1
        print("Cantidad 10G TR " + str(C_10GTR))
        print("Cantidad 10G SE " + str(C_10GSE))
        print("Cantidad 1G SE " + str(C_1GSE))
        print("Cantidad 1GTR " + str(C_1GTR))
        lista_out = [C_10GTR,C_10GSE,C_1GSE,C_1GTR]
        print (lista_out)
        return lista_out
    except:
        print('\n\n ERROR: Could not retrieve, the information')
