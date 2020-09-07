import random
import pickle
import datetime
import time


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

def new_soln():
    major_lst = []
    pri_lst = [0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']

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

    while n != 50:
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
        y = random.randint(0,49)
        z = major_lst[y].index(element)
        if len(str(y)) == 2 and len(str(z)) == 2:
            res += str(y)+str(z)
        elif len(str(y)) == 1 and len(str(z)) == 1:
            res += ("0" + str(y) + "0" + str(z))
        elif len(str(y)) == 1:
            res += ("0" + str(y) + str(z))
        elif len(str(z)) == 1:
            res += (str(y) + "0" + str(z))


    print(res)
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

main()
