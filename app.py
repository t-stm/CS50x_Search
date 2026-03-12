from flask import Flask, redirect, render_template, request
from functions import *
import threading

input_url = 'https://cs50.harvard.edu/x/2025/'
visited.append(input_url)

seed = site_node(input_url, "1")
crawl_status = False
sitemap_status = False

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Routes
@app.route("/", methods=["GET"])
def index():
    global crawl_status
    if request.method == "GET":
        if crawl_status == False:
            return redirect("/crawler")
        return render_template("index.html")
    if request.method == "POST":
        error = "Post request not accepted."
        return render_template("error.html", error=error)

@app.route("/crawler", methods=["GET"])
def crawler():
    if request.method == "GET":
        return render_template("crawler.html")
    if request.method == "POST":
        error = "Post request not accepted."
    return render_template("error.html", error=error)

@app.route("/crawling", methods=["GET", "POST"])
def crawling():
    global crawl_status
    global sitemap_status
    if request.method == "POST":
        crawl_mode = request.form.get("crawl_mode")
        index_mode = request.form.get("index_mode")
        if crawl_status == True:
            return redirect("/")
        elif crawl_mode not in ["bfs", "dfs"]:
            error = "Please choose breadth-first or depth-first crawling algorithm."
            back = "/crawler"
            return render_template("error.html", error=error, back=back)
        elif index_mode not in ["bfs", "dfs"]:
            error = "Please choose breadth-first or depth-first indexing algorithm."
            back = "/crawler"
            return render_template("error.html", error=error, back=back)
        else:
            def run_crawler():
                global crawl_status
                global sitemap_status
                make_sitemap(seed, "1", crawl_mode)
                print("*** sitemap complete ***")
                sitemap_status = True
                print("index mode = " + index_mode)
                extract_words_sitemap(seed, "1", index_mode)
                print("*** dictionary complete ***")
                crawl_status = True
            thread = threading.Thread(target=run_crawler) 
            thread.start()
            crawl_status = False
            return redirect("/crawling")

    if request.method == "GET":
        if crawl_status == True:
            return redirect("/")
        if crawl_status == False:
            sitemap_notice = ""
            if sitemap_status == True:
                sitemap_notice = "Sitemap complete, preparing index..."
            return render_template("crawling.html", sitemap_notice=sitemap_notice)

@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "GET":
        return redirect("/")

    if request.method == "POST":
        word = request.form.get("search_term")
        if word == "":
            back = "/results"
            error = "Error: please enter a search term."
            return render_template("error.html", error=error, back=back)
        print(word)
        lookup = trie_lookup(word)
        if lookup == None:
            no_result = str("Not found: " + word)
            return render_template("results.html", no_result=no_result, word=word)
        else:
            results = lookup.words[word]
            print(results)
            return render_template("results.html", results=results, word=word)
