import random
import pickle
import datetime
import time

##########
# this part of code is just defing functions
# for reducing the size of main code thus saving
# precious programming and review time
# for this version it might not be that big but later will be appended as the program gets more complicated

def array_to_string(arr):
    x = ""
    for element in arr:
        x += element

    return x

#########
# main code

def generate_new_solution_file():
    major_list = []                                                    #this is where all the shuffled arrays will be stored
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

    #parent_list is the array that holds all the allowed char set without shuffling

    parent_list = symbols + uppercase + lowercase + numbers + currency + special_characters

    input_for_seed =  input("Enter a some random symbols(more the better):\n")
    random.seed(a = input_for_seed)

    def list_setup(parent_list):                    #generated randomly shuffled list
        result_list = []
        intermediate_list = parent_list.copy()

        while len(intermediate_list) != 0:
            x = random.choice(intermediate_list)
            intermediate_list.remove(x)
            result_list.append(x)
        intermediate_list = parent_list.copy()
        return result_list

    #resets the seed (this will be removed later in favour of secure pseudo-random generation module)

    def seed_reset():
        absolute_time = str(time.time())
        random_char = random.choice(absolute_time)
        random.seed(str(input_for_seed) + random_char)

    n = 0

    #major_list generation

    while n != 100:
        temporary_list = list_setup(parent_list)
        major_list.append(temporary_list)
        seed_reset()
        n += 1

    #putting the major_list in the solution_file

    pickle_solution_file = open("solution_file.pickle",'wb')
    pickle.dump(major_list,pickle_solution_file)
    pickle_solution_file.close()

    main()

def encrypt():

    #here(below) first, a randomised char substitution is carried out
    pickle_solution_file = open("solution_file.pickle",'rb')
    major_list = pickle.load(pickle_solution_file)
    pickle_solution_file.close()

    clear_text_message = input("Enter the text to be encrpted: \n")

    char_substitution_step_result = ""

    #(below)here the script choose a random integer from 0 to 99 and use the list at that index of the major_list
    #then in that list the index of the char is noted
    #the two indexes (one of the list in the major_list and one of the char in the list) are combined to give a 4 digit intger result

    for element in clear_text_message:
        y = random.randint(0,99)
        try:
            z = major_list[y].index(eval(element))
        except:
            z = major_list[y].index(element)
        if len(str(y)) == 2 and len(str(z)) == 2:
            char_substitution_step_result += str(y)+str(z)
        elif len(str(y)) == 1 and len(str(z)) == 1:
            char_substitution_step_result += ("0" + str(y) + "0" + str(z))
        elif len(str(y)) == 1:
            char_substitution_step_result += ("0" + str(y) + str(z))
        elif len(str(z)) == 1:
            char_substitution_step_result += (str(y) + "0" + str(z))

    if len(char_substitution_step_result) >= 40 :
        char_substitution_step_result = add_secondary_password(2,char_substitution_step_result,major_list)

    #(below)here we change and resubstitute in a way that it becomes unreadable without the solution file.
    #also we add a secondary password that isn't that effective if solution file is not securely kept
    #thus revealing most of the cipher .

    final_encrypted_result = modification_and_resubstitution(char_substitution_step_result,major_list)

    cipher_txt_output = open("encrypted.txt",'w')
    cipher_txt_output.write(final_encrypted_result)
    cipher_txt_output.close()

    main()

def decrypt():
    pickle_solution_file = open("solution_file.pickle",'rb')
    major_list = pickle.load(pickle_solution_file)
    pickle_solution_file.close()

    final_encrypted_result = open("encrypted.txt",'r')
    enc = str(final_encrypted_result.readline())
    final_encrypted_result.close()
    enc = reverse_modification_and_resubstitution(enc,major_list)
    enc = use_secondary_password_for_decryption(enc,major_list)
    length_of_enc = len(enc)

    index_list = []
    char_index_list = []

    n = 0

    while n <= length_of_enc - 4:
        new_var = enc[n] + enc[n+1]
        index_list.append(new_var)
        nex_var = enc[n+2] + enc[n+3]
        char_index_list.append(nex_var)
        n += 4

    msg = ""
    counter = 0
    for element in index_list:
        adr_loc = counter
        adr_mjl = major_list[int(element)]
        alp_loc = int(char_index_list[adr_loc])
        alp = adr_mjl[alp_loc]
        msg += str(alp)
        counter += 1

    return msg

def add_secondary_password(valueofconfig,cryptedL1,major_list):
    new_cyp_l = list(cryptedL1)
    truelist = major_list[34]

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

            return array_to_string(new_cyp_l)


    else : print("please enter odd character password")

    add_secondary_password(valueofconfig,cryptedL1,major_list)

def use_secondary_password_for_decryption(res,major_list):
    skipper = 0
    secondary_password = input("Enter the password\n")
    res = list(res)
    list_to_be_used_for_decryption = major_list[34]
    length_of_secondary_password = 0

    for element in secondary_password:
        try:
            element = int(element)
        except:
            element = str(element)
        length_of_secondary_password += (list_to_be_used_for_decryption.index(element))%7

    secondary_password = reversed(secondary_password)
    for element in secondary_password:
        del res[length_of_secondary_password]
        length_of_secondary_password -= (list_to_be_used_for_decryption.index(element))%7

    return array_to_string(res)

def modification_and_resubstitution(input_result,major_list):
    input_result = list(input_result)
    temporary_poped_char_variable = input_result.pop()
    list_to_use_for_resubstitution = major_list[83]
    newresult = []
    compressed_val = ""
    n = 0
    while n < len(input_result):
        sorter_var = str(input_result[n])+str(input_result[n+1])
        newresult.append(int(sorter_var))
        n += 2
    for element in newresult:
        decoder_var = str(list_to_use_for_resubstitution[element])
        compressed_val += decoder_var
    compressed_val += str(temporary_poped_char_variable)
    return str(compressed_val)

def reverse_modification_and_resubstitution(some_enc,major_list):
    some_enc = list(some_enc)
    temporary_poped_char_variable = some_enc.pop()
    list_to_use_for_resubstitution = major_list[83]
    encresult = []
    decomp_val = ""

    for element in some_enc:
        try:
            element = int(element)
        except:
            element = str(element)
        resvar1 = list_to_use_for_resubstitution.index(element)
        encresult.append(resvar1)

    for element in encresult:
        if len(str(element)) == 2:
            decomp_val += str(element)
        elif len(str(element)) == 1:
            decomp_val += ("0" + str(element))

    decomp_val += str(temporary_poped_char_variable)
    return decomp_val

def output_help():

    print("would you like to know (s)teps to use or (r)evise function names or(g)eneral info\n ")

    input_for_the_help_prompt = input(">>(s)/(r)/(g)>")

    if input_for_the_help_prompt == "s":
        print("Steps to use: \n\n"
        "<*>If you are using for the first time start by typing \"new\" \n"
        ">just randomajor_listy enter strings from your keyboard when asked for\n"
        ">This is also what you should do if you feel your soln file has\n"
        "been leaked \n"
        "<*>In the next step type \"encp\" \n"
        ">Now simply enter the text to be excrypted and then the password^\n\n"
        "^password should have odd number of characters\n\n"
        ">Your Text is now encrypted and is ready to share (encrypted.txt)\n"
        "!!Remember!! your solution_file.pickle file is as important as your password\n"
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
        "to exit use \"exit\" \n\n\n "
        )

    elif input_for_the_help_prompt == "r":
        print("Revision of commands:\n\n"
        "new   => for making a fresh soln file\n"
        "encp  => for encrypting text\n"
        "decp  => for temporary decryption\n"
        "decpf => for permanent decryption\n"
        "exit -->> exit\n"
        "\"help\" to print this help\n\n\n"
        )

    elif input_for_the_help_prompt == "g":
        print("General information:\n\n"
        "Cryper \n\n"
        "Designed by : Siddhant Kundargi\n"
        "for bug report/contact : tinuscientist@gmail.com\n"
        "source forkable at github.com/Siddhant-Kundargi/cryptographic-methods.git \n\n\n"
        )

    else :
        print("No input!\n exiting!... \n")

    main()

def permanently_decrypt():
    msg = decrypt()
    final_encrypted_result = open("encrypted.txt",'w')
    final_encrypted_result.write(msg)
    print(msg)

def main():

    main_input = input("What to do?:\n")

    if main_input == "new":
        generate_new_solution_file()

    elif main_input == "exit":
        exit()

    elif main_input == "encp":
        encrypt()

    elif main_input == "decp":
        msg = decrypt()
        print(msg)

    elif main_input == "decpf":
        permanently_decrypt()

    elif main_input == "help":
        output_help()

    else :
        print("Invalid command")
        main()

###########
# script execution
main()
