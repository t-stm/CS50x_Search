from functions import * 

def terminal_app():
    close = False
    next = ""
    while close == False:
        input_word = input("Enter lookup word: ")
        output_node = trie_lookup(input_word)
        if output_node != None:
            print('Found "' + input_word + '" in URLs:')
            for url in output_node.words[input_word]:
                print("-" + url)
        else:
            print('"' + input_word + " not found.")
        while True:
            next = input("Look up another word? Enter y/n.\n")
            if next not in ["y", "n"]:
                return True
            else:
                break
        if next == "y":
            close = False
        else:
            break