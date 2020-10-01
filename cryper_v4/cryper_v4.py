import random
import pickle
import datetime
import time
def new_soln():
    major_lst = []
    pri_lst = ['.',',','!','@','#','$','%','&','*','^','-','|','[',']','{','}','(',')','_','+','=',';',':',"'",'"','?','/','>','<','`','~','\\','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']

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

    inp = input("Enter the text to be encrpted(Avoid caps and special symbols): \n")

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
        inpcon1 = input("Enter the password configuration:\n->2_paswd (1 made by you and one encrption key)\n->3_paswd (1 made by you, 1 auto-generated and one encryption key)\n")
        if inpcon1 == "2_paswd" :
            res = passit(2,res,major_lst)
        elif inpcon1 == "3_paswd" :
            passwordgen = passit(3,res,major_lst)[1]
            res = passit(3,res,major_lst)[2]
    try:
        print(passwordgen)
    except:
        None
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


    print(msg)

    main()

def passit(valueofconfig,cryptedL1,major_lst):
    new_cyp_l = list(cryptedL1)
    truelist = major_lst[34]

    inppass = input("Enter the desired password(must be odd no of characters)\n")
    
    res = ""
    resmd1 = 0


    if len(inppass) % 2 != 0 :

        if valueofconfig == 2 :
            for element in inppass:
                try:
                    element = int(element)
                except:
                    element = str(element)
                resmd1 += (truelist.index(element))%7
                jusran = str(random.randint(0,9))
                new_cyp_l.insert(resmd1,jusran)
            
            for element in new_cyp_l:
                res += element
            return res

        elif valueofconfig == 3 :
            passwordauto = ""
            for element in inppass:
                try:
                    element = int(element)
                except:
                    element = str(element)
                resmd1 += (truelist.index(element))%7
                passwordauto += new_cyp_l[resmd1]
                del new_cyp_l[resmd1]
            
            for element in new_cyp_l:
                res += element
            return [passwordauto,res]
    
    
    else : 
        print("invalid input : Must be odd number of characters\n")  
        passit(valueofconfig,cryptedL1,major_lst)

def unpass(res,ML):
    passcon = input("Enter the passoword confiugration\n")
    skipper = 0

    if passcon == "2":
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

        resvar = ""
 
        for element in res:
            resvar += str(element)
        return resvar

    elif passcon == "3":
        pswd1 = input("Enter your password\n")
        pswd2 = input("Enter auto-generated password\n")
        res = list(res)
        uselst = ML[34]
        counter1 = 0
        for element in pswd1:
            try:
                element = int(element)
            except:
                element = str(element)
            skipper += (uselst.index(element))%7
            res.insert(skipper,pswd2[counter1])
            counter1 += 1
        return res    

def main():
    input_ultimate = input("What to do?:\n")
    if input_ultimate == "new":
        new_soln()
    elif input_ultimate == "encp" :
        cryptit()
    elif input_ultimate == "decp" :
        decrypt()
    else :
        print("Invalid command")
        main()

main()