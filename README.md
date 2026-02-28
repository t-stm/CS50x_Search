# CS50x Search

## Table of Contents
- [Purpose of the application](#Purpose-of-the-application)

- [Quickstart](#quickstart)
  
- [Technical Description](#Technical-description)
  - [Dependencies](#dependencies)
  - [Architecture](#architecture)
  - [functions.py](#functionspy)
    - [extract_elements_html(url)](#extract_elements_htmlurl)
    - [class site_node](#class-site_node)
    - [extract_urls_html(input_node)](#extract_urls_htmlinput_node)
    - [make_sitemap(input_node, index="1", mode="bfs")](#make_sitemapinput_node-index1-modebfs)
    - [print_sitemap(input_node)](#print_sitemapinput_node)
    - [trie_add(word, url, input_node=trie_root, position=0)](#trie_addword-url-input_nodetrie_root-position0))
    - [trie_lookup(word, input_node=trie_root, position=0)](#trie_lookupword-input_nodetrie_root-position0))
    - [trie_print(input_node=trie_root)](#trie_printinput_nodetrie_root))
    - [extract_words_html(url)](#extract_words_htmlurl)
    - [extract_words_sitemap(input_node, index="1", mode="bfs")](#extract_words_sitemapinput_node-index1-modebfs)

  - [web_app.py](#web_apppy)
    - [@app.route("/")](#approute-methodsget)
    - [@app.route("/crawler")](#approutecrawler-methodsget)
    - [@app.route("/crawling")](#approutecrawling-methodsget-post)
    - [@app.route("/results")](#approuteresults-methodsget-post)
    

## Purpose of the application
This application is a mini-search engine for students of Harvard's CS50x course, which allows them to locate particular terms on the CS50x website. The application first crawls the CS50x website using an algorithm of the user's choice (breadth-first or depth-first) and creates a sitemap of the website. The application then proceeds to traverse the sitemap page by page using an algorithm of the user's choice (again breadth-first or depth-first) and creates a trie that indexes all the words that occur on the website, along with the URL of the page on which they occur. Once the index is ready, the user can search any term to get a list of URLs that direct the user to the respective pages on which the search term occurs.


## Quickstart
This application runs in the web browser - no installation required! 
**Live Application:** [Your Deployed URL Here]

1. Visit the live application using the URL above  
2. Select the crawling algorithm from the respective dropdown menu
3. Select the indexing algorithm from the respective dropdown menu
4. Click the "Crawl" button to launch the crawler
5. Wait until the Sitemap and Index are complete (this may take 2-3 minutes!). Once they are complete, users are automatically redirected to the Search page
6. On the search page, enter a search term in the search bar
7. Click the "Search button" to run the search query
8. If query yields any results, users can open any of the resulting URLs in a new window by clicking on them

## Technical description

### Dependencies
- Flask==3.0.0
- beautifulsoup4==4.12.2
- requests==2.31.0

### Architecture
The application contains several elements: functions.py (the "model"), web_app.py (the "controller") and several HTML templates and a CSS file (the "view"). The main HTML template is layout.hmtl. This file serves as the layout for all other .html files in the application, all of which extend layout.html using Jinja. 

### functions.py
#### extract_elements_html(url)
This function takes a URL string as an input and extracts all HTML elements from the HTML code that's returned after sending a request to the input URL. An older version of the code had a manual implementation to achieve this, but this implementation did not capture all URLs reliably. Therefore, the decision was made to use the BeautifulSoup library instead. The extract_elements_html function returns an object that contains all URLs on the input page.

#### class site_node
The sitemap created by the crawler consists of nodes that are defined as a class called "site_node". Each site node has three attributes: a unique URL, an index number (mainly used for testing purposes during the development process) and a list of "child nodes." The index number is used as a reference for the position of the node in the sitemap and the list of "child nodes" is used to store all URLs to other pages on the CS50x website that occur on the parent page (each URL will be added as a child node to the parent node). The method "add_child" is used to add a child node to the parent node's list of children.

#### extract_urls_html(input_node)
This function returns a list of URLs that occur on the page that corresponds to the input_node (which is a node from the sitemap). First, it calls extract_elements_html to parse the HTML code of the input_node, then it loops over all <a> tags in the parsed HTML and then it extracts the "href" part of the tag. For each "href", it checks that the href is not empty; that it doesn't contain "http://" (this step excludes external links so that the crawler doesn't venture outside the CS50x website) and that it doesn't contain a # (since # just points to different sections on a page, crawling through each of them is not needed). The function then uses urljoin to normalize relative URLs and turn them into a full (i.e. absolute) URL. It then checks that the normalized URL actually returns a valid status code and that the URL has not already been visited. If all of those conditions are met, the URL is added to the output list and to the global list of visited URLs. Visited URLs are stored in a global variable called "visited", which is a list of visited URLs. Checking against this list helps prevent endless loops (i.e. if a URL on page A refers to page B and a URL on page B refers to page A) and improves the efficiency of the application (each URL only needs to be visited once to extract the words).

#### make_sitemap(input_node, index="1", mode="bfs")
To generate the sitemap, this function takes an input node (which should contain the root URL of the website that will be crawled through), starts with index 1 (unless another value is entered into the function) and takes "bfs" mode unless the function takes another input. After checking that the inputs are valid, the function proceeds to build the sitemap using an algorithm specified by the user (i.e. the mode). For the sake of the developer's learning, two search algorithms were implemented. The user has a choice between breadth-first or depth-first. The DFS approach starts by calling extract_urls_html to extract all URLs that occur on the input_node's page. It loops through the list of URLs returned by extract_urls_html, creates a child node for every URL on the page using the site_node class and then adds the child nodes to the input node using the add_child method for this class. However, for every child node created, it recursively calls make_sitemap to repeat this process for that particular child node. This causes the algorithm to traverse the website until it arrives at a page that doesn't contain any URLs. This essentially builds the sitemap from the bottom up.

The breadth-first algorithm "queues" all pages that it will crawl through using a list called "queue". It starts by adding the root node to the queue. It then repeatedly takes the first node in the queue (the "current_node") and obtains a list of all URLs on the current_node's page by calling extract_urls_html. It then loops through the list, creates child nodes for each of the URLs, appends the child nodes to the current_node and adds the child nodes to the queue. Finally, it removes the first element from the queue using the "pop" method and runs the same process for the following node in the queue. This way, the sitemap is built from the top down rather than from the bottom up.

#### print_sitemap(input_node)
Once the sitemap is complete, this function traverses the tree depth-first and prints the index number of the node and the corresponding URL. This function was mainly used during the development phase to test whether make_sitemap was working properly. It is run in the terminal and is not used in the web application.

#### class trie_node
The trie data structure is used to organize all the words that occur on the CS50x website. It consists of nodes for individual characters. Each trie_node has four attributes: 1. the char that it represents 2. an index number 3. a variable called "words" which contains a dictionary that has a word as a key and a list of URLs where that word occurs as its value and 4. a list of child nodes. The method add_url checks if a word is already in the trie, adds it if it isn't, and adds the URL where the word occurs. The developer considered using a hash table instead of a trie, but opted for a trie because it has a unique path for every word, rather than grouping words together in buckets. The developer also wanted to practice implementing a data structure they hadn't used yet.

#### trie_add(word, url, input_node=trie_root, position=0)
This function takes a word as an input, along with the URL on which a word occurs and an input_node in the trie. It traverses the trie by looping over the chars in the word (starting from char 0 and moving to the next char with each iteration of the loop by shifting the starting position in the string +1). For every char, it checks the children of the input node. If it finds the char it's looking for among the input_node's children, it will check whether it has reached the final char in the word. If it has, it will add the word/url to the input_node using the add_url method described previously. If it has found a match but hasn't reached the final char yet, it will call itself recursively on the matching child_node and look for the next char in the word. Since the full word is passed in as a variable to the recursive function, shifting the starting position is necessary (otherwise it would keep looking for the first char in the word whenever the function is called recursively instead of moving to the next char).

If it doesn't find a matching char among the current_node's children, it will add a new child_node to the current_node. This essentially creates a new path in the trie for the word. It will keep adding new nodes recursively until it reaches the final char in the word. When it reaches the final char, it will add the word/url to the last node in the word's path using the add_url method and return the final node.

#### trie_lookup(word, input_node=trie_root, position=0)
This function takes a word and a trie_node as inputs. It traverses the trie in a similar fashion to trie_add (by checking the subsequent chars in a word and matching them against the child_nodes of a particular node in the trie), but instead of adding new paths for words that don't yet exist in the trie, it simply follows the path for the word and when it reaches the final node, it returns the final node. If it stops finding matching chars among the child_nodes in the trie (which means that the word's path doesn't exist in the trie), it simply returns None.

#### trie_print(input_node=trie_root)
As an auxiliary function similar to print_sitemap, this was used during development to test in the terminal whether the trie was functioning correctly. It is not used in the web application.

#### extract_words_html(url)
This function first uses extract_elements_html to parse the HTML code of the input URL and then removes all tags that don't contain any text (such as script and style tags). What remains is the actual text on the page, which is stored in a dedicated variable called "text". The function then loops over all of the chars in the text and checks whether they are included in the alphabet (alphabetic chars are defined in the "nondelimiting_chars" array). When it reaches a non-alphabetic character, it has found a complete word. It will then proceed to add the URL (and word if it doesn't yet exist in the trie) to the trie by calling the trie_add function before continuing to loop through the chars in the text until it has found another word.

#### extract_words_sitemap(input_node, index="1", mode="bfs")
This function traverses the sitemap based on the algorithm of the user's choice (bfs or dfs as previously explained) and whenever it reaches a new node in the sitemap, it will extract all the words using the extract_words_html function.


### web_app.py
The web app contains several routes, and takes the user to an error page if the wrong method is used to request a particular route. The "seed" (i.e. root node) of the sitemap is set to the CS50x homepage https://cs50.harvard.edu/x/2025/. The file imports all of the functions from functions.py.

#### @app.route("/", methods=["GET"])
This route first checks a global variable called "crawl_status" to see if the crawler has already been run by one of the other functions (other functions are explained below). If the crawler hasn't been run yet, the user will be redirected and asked to run the crawler. If the crawler has been run, the user will be shown the index.html template, which contains a form with a search field and a submit button so that the user can search for words on the CS50x homepage.

#### @app.route("/crawler", methods=["GET"])
This route will render the crawler.html template. This template contains a form that allows the user to choose the crawling and indexing algorithms (i.e. the algorithms to respectively generate and traverse the sitemap) from two dropdown menus. The user then clicks the "crawl" button, which takes the user to the /crawling route using a POST request to transport the crawl_mode and index_mode variables.

#### @app.route("/crawling", methods=["GET", "POST"])
When this route receives a post request with the inputs from the form on crawler.html, it will store the inputs from the form as variables. It will then check whether the crawler has already been run by checking the global variable crawl_status. If so, it will redirect the user to the / route so that they can run a search query. Otherwise, it will check if the inputs are valid and render an error page if they are not. If the inputs are valid, it will run the crawler by executing the run_crawler function.

This function will make the sitemap using the make_sitemap function with the "seed" node and the crawl_mode provided by the user on crawler.html as inputs. When the sitemap is ready, it will extract the words from the sitemap using the extract_words_sitemap with the "seed" node and the index_mode provided by the user on crawler.html as inputs. When the words have been extracted, it will set the crawl_status variable to True to indicate that the crawler is done and the index is ready.

Since the crawler may take a minute to run, the program contains a separate thread in the application to run the crawler, which prevents the website from timing out before the crawler has finished. Once the thread is started, the user will be redirected to the /crawling route using a GET request. This will render the template crawling.html, which will refresh every 10 seconds until the crawler is ready. When the sitemap has been generated, a global string variable called "sitemap_notice" is passed into the template, which will display an extra line of text to the user to indicate that the crawler is progressing (otherwise the user may get impatient). The global sitemap_notice variable is updated by the run_crawler function. Every time the page is refreshed and the route is requested using a GET request, the route checks whether the "crawl_status" is True. When it's true, it will redirect the user to the "/" route, which will load the index.html template so that the user can run search queries.

#### @app.route("/results", methods=["GET", "POST"])
The user will be redirected to this route with a POST request when the user submits the search form on the index.html template. It will store the search_term from the form as the variable "word", check that a word has actually been entered, and render the error.html template if the user hasn't entered a search term before clicking the search button.

If the input is valid, it will run the trie_lookup function with the word as an input to check if the word exists in the trie (i.e. in the index) and store the return value as the "lookup" variable. If the lookup variable is None, it will render the results.html template and display a message that the search term has not been found by passing in the "no_result" variable into the template.

If results have been found, the "lookup" variable will be the final trie_node of the word's path in the trie. This node will contain a "words" attribute, which is a dictionary that contains the word (in this case the search term that the user has entered) as a key and a list of URLs where the word occurs as its corresponding value. The "results" variable will then take the list of URLs that corresponds to the word from the dictionary. The results.html template will then be rendered and the "results" variable will be passed in. The template contains Jinja syntax that uses a for loop to loop over the results and add them as rows in a table when rendering the template. The user will get to see the results of their search query in the table, and navigate to each of the search results by clicking the respective URLs.




