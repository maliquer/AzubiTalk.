from flask import Flask, render_template, request, redirect, abort
import json #vv
import datetime
import os #vv für win?? nötig? 

app = Flask(__name__)

JSON_PATH = os.path.join(os.path.dirname(__file__), "posts.json") #os.path.join ==> so auf jd Betriebssystem laufend

# default_posts = [ ......... ] hardgecodeten feed rausgenommen
# posts = []

def load_posts(): ##vv
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)
    
def save_posts(posts):
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)


@app.route("/")
def home():
    posts = load_posts() ##vv
    return render_template("index.html", posts=posts)


@app.route("/add-post", methods=["POST"])
def add_post():
    posts = load_posts() #vv
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist("tags")

    #new post dann im json-Format hinzufügen
    new_post = {
        "id": len(posts)+1,
        "title": title,
        "content": content,
        "votes": 0,
        "author": {
            "first_name": "Community",
            "last_name": "User",
            "username": "username" #??
        },
        "created_at": datetime.datetime.now().isoformat(),
        "answer_count": 0,
        "category": request.form.get("category", "None"), #bei Post-Erstellung einbinden, dass Kategorie wählbar ist
        "tags": tags,
    }

 #   posts.append({
  #      "title": title,
   #     "content": content,
  #  })

    posts.append(new_post) #vv
    save_posts(posts) #vv

    return redirect("/")


@app.route("/post")
def post():
    return redirect("/post/1")


@app.route("/post/<int:post_id>")
def post_detail(post_id):
    posts = load_posts() #vv
    selected_post = next((p for p in posts if p["id"] == post_id), None)
    if selected_post is None:
        abort(404)
    
  #                  try:
   #                     if post_id.startswith("new-"):
    #                        index = int(post_id.replace("new-", ""))
     #                       selected_post = posts[index]
      #                  else:
       #                     index = int(post_id) - 1
        #                    selected_post = default_posts[index]
         #           except (ValueError, IndexError):
          #              abort(404)

    return render_template("post.html", post=selected_post)


@app.route("/upvote/<int:post_id>", methods=["POST"])
def upvote(post_id):
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            post["votes"] += 1
            break
    save_posts(posts)
    return {"votes": post["votes"]}

@app.route("/add-comment/<int:post_id>", methods=["POST"])
def add_comment(post_id):

    posts = load_posts()

    comment_text = request.form["comment"]

    for post in posts:

        if post["id"] == post_id:

            if "comments" not in post:
                post["comments"] = []

            author = request.form["author"]
            
            post["comments"].append({

                "author": author,
                "text": comment_text,
                "created_at": datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

            })

            post["answer_count"] += 1

            break

    save_posts(posts)

    return redirect(f"/post/{post_id}")

if __name__ == "__main__":
    app.run(debug=True)



# index.html 
# @CATEGORIES: added button data-category
# @POSTS: hardcodete Posts durch for posts in posts Loop ersetzen
