from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from .extensions import db
from .models import Advertisement

ads_bp = Blueprint("ads", __name__)


# -----------------------------
# Создание объявления
# POST /api/ads
# -----------------------------
@ads_bp.route("/api/ads", methods=["POST"])
def create_ad():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON обязателен"}), 400

    if "title" not in data or "description" not in data:
        return jsonify({
            "error": "Поля title и description обязательны"
        }), 400

    try:
        ad = Advertisement(
            title=data["title"],
            description=data["description"],
            owner=data.get("owner", "anonymous")
        )
        db.session.add(ad)
        db.session.commit()
        return jsonify(ad.to_dict()), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Ошибка базы данных",
            "details": str(e)
        }), 500


# -----------------------------
# Получение всех объявлений
# GET /api/ads
# -----------------------------
@ads_bp.route("/api/ads", methods=["GET"])
def list_ads():
    ads = Advertisement.query.all()
    return jsonify([ad.to_dict() for ad in ads])


# -----------------------------
# Получение одного объявления
# GET /api/ads/<id>
# -----------------------------
@ads_bp.route("/api/ads/<int:ad_id>", methods=["GET"])
def get_ad(ad_id):
    ad = db.session.get(Advertisement, ad_id)
    if not ad:
        return jsonify({"error": "Объявление не найдено"}), 404
    return jsonify(ad.to_dict())


# -----------------------------
# Обновление объявления
# PUT /api/ads/<id>
# -----------------------------
@ads_bp.route("/api/ads/<int:ad_id>", methods=["PUT"])
def update_ad(ad_id):
    ad = db.session.get(Advertisement, ad_id)
    if not ad:
        return jsonify({"error": "Объявление не найдено"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Нет данных для обновления"}), 400

    try:
        if "title" in data:
            ad.title = data["title"]
        if "description" in data:
            ad.description = data["description"]
        if "owner" in data:
            ad.owner = data["owner"]

        db.session.commit()
        return jsonify(ad.to_dict())

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Ошибка обновления",
            "details": str(e)
        }), 500


# -----------------------------
# Удаление объявления
# DELETE /api/ads/<id>
# -----------------------------
@ads_bp.route("/api/ads/<int:ad_id>", methods=["DELETE"])
def delete_ad(ad_id):
    ad = db.session.get(Advertisement, ad_id)
    if not ad:
        return jsonify({"error": "Объявление не найдено"}), 404

    try:
        db.session.delete(ad)
        db.session.commit()
        return "", 204

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Ошибка удаления",
            "details": str(e)
        }), 500
