def encrypt(word):
    import random
    ciphertext = ""
    number = 0
    key = 9001
    #Jumble the word (reverse it)
    length = len(word)
    word = word[length::-1]
    word = word.upper()
    
    for index in range(len(word)):
        #Add random characters at prime number locations (kept short for simplicity)
        if index in [2,3,5,7,11,13]:
            charGen = str(chr(random.randint(65,90)))
            ciphertext += charGen
            
        if word[index].isalpha(): 
            number = ord(word[index]) + int(key) % 26
            if number > 90:
                number = number - (ord('Z') + 1 - ord('A'))
                
            ciphertext += str(chr(number)) 
        else:
            ciphertext += str(word[index])
    return ciphertext

def decrypt(word):
    text = ""
    key = 9001
    word = word.upper()
    
    for index in range(len(word)):
        #These were randomly inserted into word
        if index in [2,4,7,10,15,18]:
            continue

        if word[index].isalpha():
            number = ord(word[index]) - int(key) % 26
            if number < 65:
                number = number + (ord('Z') + 1 - ord('A'))
            text += str(chr(number))
            
        else:
            text += str(word[index])

    #Unjumble the word (unreverse it)
    length = len(text)
    text = text[length::-1]
    return text