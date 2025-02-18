from flask import Flask, render_template

app = Flask(__name__)

# Route pour la page d'accueil
@app.route("/")
def home():
    return render_template("index.html")

# Route pour la page des projets
@app.route("/projects")
def projects():
    return render_template("projects.html")

# Route pour la page "À propos"
@app.route("/about")
def about():
    return render_template("about.html")

# Route pour la page de contact
@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
