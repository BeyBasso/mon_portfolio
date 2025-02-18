from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'  # Base de données SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ma_cle_secrete'  # Nécessaire pour utiliser flash messages

db = SQLAlchemy(app)

# Modèle pour les projets
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    technologies = db.Column(db.String(200), nullable=False)

# Création de la base de données
with app.app_context():
    db.create_all()

# Route pour afficher la liste des projets
@app.route("/projects")
def projects():
    projects_list = Project.query.all()
    return render_template("projects.html", projects=projects_list)

# Route pour ajouter un nouveau projet
@app.route("/add_project", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        technologies = request.form.get("technologies")
        new_project = Project(title=title, description=description, technologies=technologies)
        db.session.add(new_project)
        db.session.commit()
        flash("Projet ajouté avec succès !", "success")
        return redirect(url_for("projects"))
    return render_template("add_project.html")

# Route pour modifier un projet existant
@app.route("/edit_project/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == "POST":
        project.title = request.form.get("title")
        project.description = request.form.get("description")
        project.technologies = request.form.get("technologies")
        db.session.commit()
        flash("Projet modifié avec succès !", "success")
        return redirect(url_for("projects"))
    return render_template("edit_project.html", project=project)

# Route pour supprimer un projet
@app.route("/delete_project/<int:project_id>", methods=["POST"])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash("Projet supprimé avec succès !", "success")
    return redirect(url_for("projects"))

# Routes pour les autres pages (accueil, about, contact)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
