from flask import Blueprint, render_template, request, redirect, url_for, abort
from .db import get_db

bp = Blueprint("incidents", __name__)

PRIORITES = ["Faible", "Moyenne", "Élevée"]
STATUTS = ["Nouveau", "En cours", "Résolu"]


def get_incident_or_404(incident_id):
    incident = get_db().execute(
        "SELECT * FROM incidents WHERE id = ?", (incident_id,)
    ).fetchone()
    if incident is None:
        abort(404)
    return incident


@bp.route("/")
def index():
    incidents = get_db().execute("SELECT * FROM incidents ORDER BY id DESC").fetchall()
    return render_template("index.html", incidents=incidents)


@bp.route("/ajouter", methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        titre = request.form.get("titre", "").strip()
        description = request.form.get("description", "").strip()
        lieu = request.form.get("lieu", "").strip()
        priorite = request.form.get("priorite", "Moyenne")
        if not titre or not description or not lieu or priorite not in PRIORITES:
            return render_template(
                "ajouter.html", priorites=PRIORITES, erreur="Tous les champs sont obligatoires."
            ), 400
        db = get_db()
        db.execute(
            "INSERT INTO incidents (titre, description, lieu, priorite) VALUES (?, ?, ?, ?)",
            (titre, description, lieu, priorite),
        )
        db.commit()
        return redirect(url_for("incidents.index"))
    return render_template("ajouter.html", priorites=PRIORITES, erreur=None)


@bp.route("/incident/<int:incident_id>")
def detail(incident_id):
    incident = get_incident_or_404(incident_id)
    return render_template("detail.html", incident=incident, statuts=STATUTS)


@bp.route("/incident/<int:incident_id>/statut", methods=["POST"])
def modifier_statut(incident_id):
    get_incident_or_404(incident_id)
    statut = request.form.get("statut")
    if statut not in STATUTS:
        abort(400)
    db = get_db()
    db.execute("UPDATE incidents SET statut = ? WHERE id = ?", (statut, incident_id))
    db.commit()
    return redirect(url_for("incidents.detail", incident_id=incident_id))


@bp.route("/incident/<int:incident_id>/supprimer", methods=["POST"])
def supprimer(incident_id):
    get_incident_or_404(incident_id)
    db = get_db()
    db.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
    db.commit()
    return redirect(url_for("incidents.index"))


@bp.route("/health")
def health():
    return {"status": "OK"}