import random
import pickle
import datetime
import time

##########
# this part of code is just defing functions
# for reducing the size of main code thus saving
# precious programming and review time

def arr_str(arr):
    x = ""
    for element in arr:
        x += element

    return x

#########
# main code

def new_soln():
    major_lst = []
    symbols = ['.',',','!','@','#','%','&','*','^','-',
           '|','[',']','{','}','(',')','_','+','=',';',
           ':',"'",'"','?','/','>','<','`','~','\\']
    uppercase = ['A','B','C','D','E','F','G','H','I','J','K',
             'L','M','N','O','P','Q','R','S','T','U','V',
             'W','X','Y','Z']
    lowercase = ['a','b','c','d','e','f','g','h','i','j','k',
             'l','m','n','o','p','q','r','s','t','u','v',
             'w','x','y','z',' ']
    currency = ['€','$','£','¥','₹']

    special_characters = ['©']

    numbers = [0,1,2,3,4,5,6,7,8,9]

    pri_lst = symbols + uppercase + lowercase + numbers + currency + special_characters

    inp_var =  input("Enter a some random symbols(more the better):\n")
    random.seed(a = inp_var)

    def lst_set(pri_lst):
        res_lst = []
        sec_lst = pri_lst.copy()

        while len(sec_lst) != 0:
            x = random.choice(sec_lst)
            sec_lst.remove(x)
            res_lst.append(x)
        sec_lst = pri_lst.copy()
        return res_lst

    def sd_rst():
        t = str(time.time())
        rnrn = random.choice(t)
        random.seed(str(inp_var) + rnrn)

    n = 0

    while n != 100:
        some_lst = lst_set(pri_lst)
        major_lst.append(some_lst)
        sd_rst()
        n += 1

    pckl = open("soln.pickle",'wb')
    pickle.dump(major_lst,pckl)
    pckl.close()

    main()

def cryptit():
    pkl = open("soln.pickle",'rb')
    major_lst = pickle.load(pkl)
    pkl.close()

    inp = input("Enter the text to be encrpted: \n")

    res = ""

    for element in inp:
        y = random.randint(0,99)
        try:
            z = major_lst[y].index(eval(element))
        except:
            z = major_lst[y].index(element)
        if len(str(y)) == 2 and len(str(z)) == 2:
            res += str(y)+str(z)
        elif len(str(y)) == 1 and len(str(z)) == 1:
            res += ("0" + str(y) + "0" + str(z))
        elif len(str(y)) == 1:
            res += ("0" + str(y) + str(z))
        elif len(str(z)) == 1:
            res += (str(y) + "0" + str(z))

    if len(res) >= 40 :
        res = passit(2,res,major_lst)

    res = compression1(res,major_lst)

    txt = open("encrypted.txt",'w')
    txt.write(res)
    txt.close()

    main()

def decrypt():
    ext_file = open("soln.pickle",'rb')
    major_lst = pickle.load(ext_file)
    ext_file.close()

    encpt = open("encrypted.txt",'r')
    enc = str(encpt.readline())
    encpt.close()
    enc = uncomp1(enc,major_lst)
    enc = unpass(enc,major_lst)
    encl = len(enc)

    adr_lst = []
    ltr_adr_lst = []

    n = 0

    while n <= encl - 4:
        new_var = enc[n] + enc[n+1]
        adr_lst.append(new_var)
        nex_var = enc[n+2] + enc[n+3]
        ltr_adr_lst.append(nex_var)
        n += 4

    msg = ""
    counter = 0
    for element in adr_lst:
        adr_loc = counter
        adr_mjl = major_lst[int(element)]
        alp_loc = int(ltr_adr_lst[adr_loc])
        alp = adr_mjl[alp_loc]
        msg += str(alp)
        counter += 1

    return msg

def passit(valueofconfig,cryptedL1,major_lst):
    new_cyp_l = list(cryptedL1)
    truelist = major_lst[34]

    inppass = input("Enter the desired password(must be odd no of characters)\n")

    res = ""
    resmd1 = 0


    if len(inppass) % 2 != 0 :

            for element in inppass:
                try:
                    element = int(element)
                except:
                    element = str(element)
                resmd1 += (truelist.index(element))%7
                jusran = str(random.randint(0,9))
                new_cyp_l.insert(resmd1,jusran)

            return arr_str(new_cyp_l)


    else : print("please enter odd character password")

    passit(valueofconfig,cryptedL1,major_lst)

def unpass(res,ML):
    skipper = 0
    pswd = input("Enter the password\n")
    res = list(res)
    uselst = ML[34]
    pslen = 0

    for element in pswd:
        try:
            element = int(element)
        except:
            element = str(element)
        pslen += (uselst.index(element))%7

    pswd = reversed(pswd)
    for element in pswd:
        del res[pslen]
        pslen -= (uselst.index(element))%7

    return arr_str(res)

def compression1(some_res,ML):
    some_res = list(some_res)
    last_one = some_res.pop()
    encode_lst = ML[83]
    newresult = []
    compressed_val = ""
    n = 0
    while n < len(some_res):
        sorter_var = str(some_res[n])+str(some_res[n+1])
        newresult.append(int(sorter_var))
        n += 2
    for element in newresult:
        decoder_var = str(encode_lst[element])
        compressed_val += decoder_var
    compressed_val += str(last_one)
    return str(compressed_val)

def uncomp1(some_enc,ML):
    some_enc = list(some_enc)
    last_one = some_enc.pop()
    encode_lst = ML[83]
    encresult = []
    decomp_val = ""

    for element in some_enc:
        try:
            element = int(element)
        except:
            element = str(element)
        resvar1 = encode_lst.index(element)
        encresult.append(resvar1)

    for element in encresult:
        if len(str(element)) == 2:
            decomp_val += str(element)
        elif len(str(element)) == 1:
            decomp_val += ("0" + str(element))

    decomp_val += str(last_one)
    return decomp_val

def outputhelp():

    print("would you like to know (s)teps to use or (r)evise function names or(g)eneral info\n ")

    input_info = input(">>(s)/(r)/(g)>")

    if input_info == "s":
        print("Steps to use: \n\n"
        "<*>If you are using for the first time start by typing \"new\" \n"
        ">just randomly enter strings from your keyboard when asked for\n"
        ">This is also what you should do if you feel your soln file has\n"
        "been leaked \n"
        "<*>In the next step type \"encp\" \n"
        ">Now simply enter the text to be excrypted and then the password^\n\n"
        "^password should have odd number of characters\n\n"
        ">Your Text is now encrypted and is ready to share (encrypted.txt)\n"
        "!!Remember!! your soln.pickle file is as important as your password\n"
        "Do not lose it or the decryption may not work\n\n"
        "<*>Now the part where you decrypt the text file\n"
        "!!Remember!! keep your soln and encrypted file in the same directory\n"
        "as the python script/executable\n\n"
        ">To Decrypt start by entering \"decp\"\n"
        ">Now enter the password when asked for\n"
        ">This will reaveal the decrypted text till the console/terminal is\n"
        "running\n"
        ">for permanent decryption use the command \"decpf\"\n\n"
        "use \"help\" to print this info \n"
        "to exit use \"exit\" or \"end\" \n\n\n "
        )

    elif input_info == "r":
        print("Revision of commands:\n\n"
        "new   => for making a fresh soln file\n"
        "encp  => for encrypting text\n"
        "decp  => for temporary decryption\n"
        "decpf => for permanent decryption\n"
        "exit -->> exit\n"
        "\"help\" to print this help\n\n\n"
        )

    elif input_info == "g":
        print("General information:\n\n"
        "Cryper \n\n"
        "Designed by : Siddhant Kundargi\n"
        "for bug report/contact : tinuscientist@gmail.com\n"
        "source forkable at github.com/Siddhant-Kundargi/cryptographic-methods.git \n\n\n"
        )

    else :
        print("No input!\n exiting!... \n")

    main()

def perma_dec():
    msg = decrypt()
    encpt = open("encrypted.txt",'w')
    encpt.write(msg)
    print(msg)

def main():

    input_ultimate = input("What to do?:\n")

    if input_ultimate == "new":
        new_soln()

    elif input_ultimate == "exit":
        exit()

    elif input_ultimate == "encp":
        cryptit()

    elif input_ultimate == "decp":
        msg = decrypt()
        print(msg)

    elif input_ultimate == "decpf":
        perma_dec()

    elif input_ultimate == "help":
        outputhelp()

    else :
        print("Invalid command")
        main()

###########
# script execution
main()
