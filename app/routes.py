from flask import request, render_template, redirect, url_for, jsonify
from .database import insert_visitor, query_visitors

def init_routes(app):

    @app.route("/")
    def index():
        return redirect(url_for('visit'))

    @app.route("/visit")
    def visit():
        return render_template("visit.html")

    @app.route("/submit", methods=["POST"])
    def submit():
        name = request.form.get("name","").strip()
        national_id = request.form.get("national_id","").strip()
        phone = request.form.get("phone","").strip()
        reason = request.form.get("reason","").strip()

        if not name or not national_id or not phone:
            return "Missing required fields", 400

        if not (national_id.isdigit() and len(national_id) == 14):
            return "الرقم القومي يجب أن يكون 14 رقم", 400
        if not (phone.isdigit() and len(phone) == 11):
            return "رقم التليفون يجب أن يكون 11 رقم", 400

        insert_visitor(name, national_id, phone, reason)
        return render_template("thank_you.html")

    @app.route("/api/visitors")
    def api_visitors():
        rows = query_visitors()
        data = [dict(id=r[0], name=r[1], national_id=r[2], phone=r[3], reason=r[4], submitted_at=r[5]) for r in rows]
        return jsonify(data)

