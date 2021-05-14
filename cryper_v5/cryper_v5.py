#!/bin/python3

from secrets import randbelow,choice
from pickle import load,dump

# Extra function declaration

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


    def list_setup(parent_list):                    #generated randomly shuffled list
        result_list = []
        intermediate_list = parent_list.copy()

        while len(intermediate_list) != 0:
            x = choice(intermediate_list)
            intermediate_list.remove(x)
            result_list.append(x)
        intermediate_list = parent_list.copy()
        return result_list

    n = 0

    #major_list generation

    while n != 100:
        temporary_list = list_setup(parent_list)
        major_list.append(temporary_list)
        n += 1

    #putting the major_list in the solution_file

    pickle_solution_file = open("solution_file.pickle",'wb')
    dump(major_list,pickle_solution_file)
    pickle_solution_file.close()

    main()

def encrypt():

    #here(below) first, a randomised char substitution is carried out
    pickle_solution_file = open("solution_file.pickle",'rb')
    major_list = load(pickle_solution_file)
    pickle_solution_file.close()

    clear_text_message = input("Enter the text to be encrpted: \n")

    char_substitution_step_result = ""

    #(below)here the script choose a random integer from 0 to 99 and use the list at that index of the major_list
    #then in that list the index of the char is noted
    #the two indexes (one of the list in the major_list and one of the char in the list) are combined to give a 4 digit intger result

    for element in clear_text_message:
        y = randbelow(100)
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
        char_substitution_step_result = add_secondary_password(char_substitution_step_result,major_list)

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
    major_list = load(pickle_solution_file)
    pickle_solution_file.close()

    final_encrypted_result = open("encrypted.txt",'r')
    cipher_text = str(final_encrypted_result.readline())
    final_encrypted_result.close()
    cipher_text = reverse_modification_and_resubstitution(cipher_text,major_list)
    cipher_text = use_secondary_password_for_decryption(cipher_text,major_list)
    length_of_cipher_text = len(cipher_text)

    index_list = []
    char_index_list = []

    n = 0

    while n <= length_of_cipher_text - 4:
        index_of_list_in_major_list = cipher_text[n] + cipher_text[n+1]
        index_list.append(index_of_list_in_major_list)
        index_of_char = cipher_text[n+2] + cipher_text[n+3]
        char_index_list.append(index_of_char)
        n += 4

    decrypted_plain_text = ""
    counter = 0
    for element in index_list:
        index_list_index = counter
        list_in_focus = major_list[int(element)]
        char_list_index = int(char_index_list[index_list_index])
        character = list_in_focus[char_list_index]
        decrypted_plain_text += str(character)
        counter += 1

    return decrypted_plain_text

def add_secondary_password(char_substituted_cipher,major_list):
    
    #the below code works in the following way:
        #find the index of the char in the list_to_use_for_adding_random_chars
        #(2)find the remainder of the index after dividing it with 7
        #put a random char at index equal the result from previous step
        #for the next iteration add the random char at the old index + the result of the 2nd step for this char
        #repeat this for every char in the whole secondary_password
        #in the result group all digits in the sets of 2 . Now resubstitute the digits with the char at the index = value inside the set

    cypher_text_in_list_format = list(char_substituted_cipher)
    list_to_use_for_adding_random_chars = major_list[34]

    secondary_password = input("Enter the desired password(must be odd no of characters)\n")

    index_of_the_char_in_password = 0


    if len(secondary_password) % 2 != 0 :

        for element in secondary_password:
            try:
                element = int(element)
            except:
                element = str(element)
            index_of_the_char_in_password += (list_to_use_for_adding_random_chars.index(element))%7
            random_integer = str(randbelow(10))
            cypher_text_in_list_format.insert(index_of_the_char_in_password,random_integer)

        return array_to_string(cypher_text_in_list_format)


    else : 
        print("please enter odd character password")

        return add_secondary_password(char_substituted_cipher,major_list)

def use_secondary_password_for_decryption(cipher_text,major_list):

    secondary_password = input("Enter the password\n")
    cipher_text = list(cipher_text)
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
        del cipher_text[length_of_secondary_password]
        length_of_secondary_password -= (list_to_be_used_for_decryption.index(element))%7

    return array_to_string(cipher_text)

def modification_and_resubstitution(input_result,major_list):

    input_result = list(input_result)
    temporary_poped_char_variable = input_result.pop()
    list_to_use_for_resubstitution = major_list[83]
    list_of_indexes_of_chars = []
    cipher_text = ""
    n = 0
    while n < len(input_result):
        sorter_var = str(input_result[n])+str(input_result[n+1])
        list_of_indexes_of_chars.append(int(sorter_var))
        n += 2
    for element in list_of_indexes_of_chars:
        cipher_text += str(list_to_use_for_resubstitution[element])
    cipher_text += str(temporary_poped_char_variable)
    return str(cipher_text)

def reverse_modification_and_resubstitution(cipher_text,major_list):
    cipher_text = list(cipher_text)
    temporary_poped_char_variable = cipher_text.pop()
    list_to_use_for_resubstitution = major_list[83]
    list_of_indexes_before_encryption = []
    cipher_text_before_resubstitution = ""

    for element in cipher_text:
        try:
            element = int(element)
        except:
            element = str(element)
        resvar1 = list_to_use_for_resubstitution.index(element)
        list_of_indexes_before_encryption.append(resvar1)

    for element in list_of_indexes_before_encryption:
        if len(str(element)) == 2:
            cipher_text_before_resubstitution += str(element)
        elif len(str(element)) == 1:
            cipher_text_before_resubstitution += ("0" + str(element))

    cipher_text_before_resubstitution += str(temporary_poped_char_variable)
    return cipher_text_before_resubstitution

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
