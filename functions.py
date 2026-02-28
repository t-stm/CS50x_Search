import requests
from bs4 import BeautifulSoup 
from urllib.parse import urljoin 


# ---------- EXTRACT HTML ELEMENTS ----------

def extract_elements_html(url):
    response = requests.get(url)
    elements = BeautifulSoup(response.text, 'html.parser')
    return elements


# ---------- SITEMAP ----------

class site_node:
    def __init__ (self, url, index):
        self.page = url
        self.index = index
        self.children = []

    def add_child (self, child_node):
        self.children.append(child_node)

visited=[]

def extract_urls_html(input_node):
    global visited
    elements = extract_elements_html(input_node.page)
    url_list = []
    for a in elements.find_all("a"):
        href = a.get("href")
        if href != None and href.find("http://") != 0 and href.find("#") == -1:
            url = urljoin(input_node.page, href)
        else:
            url = href
        if url not in visited and url.find(input_node.page) == 0 and requests.get(url).status_code == 200:
                visited.append(url)
                url_list.append(url)
    return url_list

def make_sitemap(input_node, index="1", mode="bfs"):
    if input_node == None:
        print("Error: input_node missing")
        return

    if mode not in ["bfs", "dfs"]:
        print("Error: choose bfs or dfs mode")
        return

    if mode=="dfs": 
        if index == "1":
                print("starting depth-first crawl")
        url_list = extract_urls_html(input_node)
        for i in range (len(url_list)):
            child_index = index + "." + str(i+1)
            child_node = site_node(url_list[i], child_index)
            input_node.add_child(child_node)
            print("Added " + child_node.index + " - " + child_node.page)
            make_sitemap(child_node, child_index, "dfs")

    if mode=="bfs":
        print("starting breadth-first crawl")
        queue = [input_node]
        print("Added " + input_node.index + " - " + input_node.page)
        while queue != []:
            current_node = queue[0]
            url_list = extract_urls_html(current_node)
            for i in range(len(url_list)):
                child_index = current_node.index + "." + str(i+1)
                child_node = site_node(url_list[i], child_index)
                current_node.add_child(child_node)
                queue.append(child_node)
                print("Added " + child_node.index + " - " + child_node.page)
            queue.pop(0) 

def print_sitemap(input_node):
    for i in range(len(input_node.children)):
        current_node = input_node.children[i]
        print(current_node.index + " - " + current_node.page)
        print_sitemap(current_node)


# ---------- TRIE ----------

class trie_node:
    def __init__ (self):
        self.char = ""
        self.index = ""
        self.words = {}
        self.children = []

    def add_url (self, word, url):
        if word not in self.words:
            self.words[word] = [url]
        elif url not in self.words[word]:
            self.words[word].append(url)

    def add_child (self, child_node):
        self.children.append(child_node)

trie_root = trie_node()

nondelimit_chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
                    ]

def trie_add(word, url, input_node=trie_root, position=0):
    for i in range(position, len(word)):
        for j in range(len(input_node.children)):
            current_node = input_node.children[j]
            if word[i] == current_node.char:
                if position == len(word)-1:
                    current_node.add_url(word, url)
                    return current_node
                else:
                    return trie_add(word, url, current_node, i+1)
        new_child = trie_node()
        new_child.char = word[i]
        input_node.add_child(new_child)
        if position == len(word)-1:
            new_child.add_url(word, url)
            return new_child
        else:
            return trie_add(word, url, new_child, i+1)

def trie_lookup(word, input_node=trie_root, position=0):
    for i in range(position, len(word)):
        for j in range(len(input_node.children)):
            current_node = input_node.children[j]
            if word[i] == current_node.char:
                if position == len(word)-1 and word in current_node.words:
                    return current_node
                return trie_lookup(word, current_node, i+1)
        return None

def trie_print(input_node=trie_root):
    char = input_node.char
    if input_node.words != {}:
        print('Node "' + char + '" is associated with the word: ' + str(input_node.words.keys()))
        print('Node "' + char + '" has ' + str(len(input_node.children)) + " children: ")
    for i in range (len(input_node.children)):
        print('Node "' + char + '" has ' + str(len(input_node.children)) + " children: ")
        child_node = input_node.children[i]
        trie_print(child_node)

def extract_words_html(url):
    elements = extract_elements_html(url)
    for element in elements(['script', 'style', 'head', 'title', 'meta', '[document]']):
        element.extract()
    text = elements.get_text(separator = '\n', strip=True) 

    word = ""
    for i in range(len(text)):
        if text[i] in nondelimit_chars:
            word = word + text[i]
        else:
            word = word.lower()
            trie_add(word, url, trie_root)
            word = ""

def extract_words_sitemap(input_node, index="1", mode="bfs"):
    if input_node == None:
            return "extract_words_sitemap>>> Error: No input_node passed in."

    if mode=="bfs":
        input_node.index = "1"
        queue = []
        queue.append(input_node)
        while queue != []:
            current_node = queue[0]
            extract_words_html(current_node.page)
            print("extract_words_sitemap>>> Extracted from: " + current_node.index + " - " + current_node.page)
            for i in range(len(current_node.children)):
                next_child = current_node.children[i]
                next_child.index = current_node.index + "." + str(i+1)
                queue.append(next_child)
            queue.pop(0) 

    if mode=="dfs":
        extract_words_html(input_node.page)
        for i in range(len(input_node.children)):
            next_node = input_node.children[i]
            next_node_index = index + "." + str(i+1)
            print("extract_words_sitemap>>> Extracted from " + next_node_index + " - " + next_node.page)
            extract_words_sitemap(next_node, next_node_index, "dfs")


# ---------- TERMINAL APP ----------

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
