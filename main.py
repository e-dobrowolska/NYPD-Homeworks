def swap_code(sentence, key):
    '''
    :param sentence: The string to be encoded
    :param key: The key for encoding, eg. GA-DE-RY-PO-LU-KI
    :return: the encoded sentence
    '''

    # is the key correct?
    if len(key) != len(set(key)):
        print("The key is not correct.")
        return

    # Prepare translations:

    key_lst = list(key)
    for i in range(0, len(key_lst)//2):
        key_lst[2*i], key_lst[2*i+1] = key_lst[2*i+1], key_lst[2*i]

    # Make a dictionary:

    code_dict = dict(zip(key, key_lst))

    # Encode the sentence:

    sentence = sentence.upper()

    output = str()

    for letter in sentence:
        if letter in code_dict.keys():
            output += code_dict[letter]
        else:
            output += letter

    return output

def swap_coding():
    translate = 1
    while translate == 1:
        print("Type the sentence to be translated:")
        sentence = str(input())
        print('''If you want to use the key GA-DE-RY-PO-LU-KI, press 1.
If you want to use the key PO-LI-TY-KA-RE-NU, press 2. 
If you want to use your own key, press 3.''')
        answer = int(input())
        if answer == 1:
            key = 'GADERYPOLUKI'
        elif answer == 2:
            key = 'POLITYKARENU'
        elif answer == 3:
            print("Type the key for encoding:")
            key = str(input())
        else:
            print("Please press 1, 2 or 3 in this question. Try again.")
            return
        result = swap_code(sentence, key)
        if result != None:
            print(f"Here is your translation: \n{result}")
        print("Would you like to translate something else? (press Y)")
        decision = str(input())

        if decision not in ['y', 'Y']:
            translate = 0

    return

swap_coding()