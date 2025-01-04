from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort, redirect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required
from Utils.EntityHandler import EntityHandler
from Utils.MyConnectPro import MyConnectPro
from flask_jwt_extended import get_jwt_identity
from Service.Models import *
from flask_jwt_extended import jwt_required
import os
from Variable import *

user = os.environ.get('USER_NAME')
password_db = os.environ.get('PASSWORD')
database = os.environ.get('DATABASE')
host = os.environ.get('HOST')
port = os.environ.get('PORT')
secret_key=os.environ.get('SECRET_KEY')
admin=os.environ.get('ADMIN')


db_manager = MyConnectPro(user= user,password=password_db,database= database,host= host,port=port)
db_manager.connect()
session_db = db_manager.get_session()


center_blueprint = Blueprint('center', __name__)


@center_blueprint.route('/searchCenter', methods=['GET'])
def search_center():
    try:
        # Lấy từ khóa tìm kiếm từ body JSON request
        data = request.get_json()
        search_query = data.get('name')  # Truyền từ khóa tìm kiếm trong JSON body

        if not search_query:
            return jsonify({"msg": "Cần truyền từ khóa tìm kiếm"}), 400

        # Tìm bệnh viện theo tên chứa từ khóa (case-insensitive)
        centers = session_db.query(LienKetBenhVien).filter(
            LienKetBenhVien.ten_benh_vien.ilike(f"%{search_query}%")
        ).all()

        if not centers:
            return jsonify({"msg": "Không tìm thấy bệnh viện phù hợp!"}), 404

        # Trả về danh sách bệnh viện
        result = [{
            "id": center.id,
            "bac_si_id": center.bac_si_id,
            "ten_benh_vien": center.ten_benh_vien,
            "dia_chi": center.dia_chi,
            "ngay_db": center.ngay_db,
            "ngay_kt": center.ngay_kt
        } for center in centers]

        return jsonify(result), 200

    except SQLAlchemyError as e:
        return jsonify({"msg": "Lỗi cơ sở dữ liệu!", "error": str(e)}), 500

    except Exception as e:
        return jsonify({"msg": "Hệ thống lỗi!", "error": str(e)}), 500


@center_blueprint.route('/getAllCenters', methods=['GET'])
def get_all_centers():
    try:
        # Lấy danh sách tất cả trung tâm từ cơ sở dữ liệu
        centers = session_db.query(LienKetBenhVien).all()

        center_list = [{
            "id": center.id,
            "bac_si_id": center.bac_si_id,
            "ten_benh_vien": center.ten_benh_vien,
            "dia_chi": center.dia_chi,
            "ngay_db": str(center.ngay_db),
            "ngay_kt": str(center.ngay_kt) if center.ngay_kt else None
        } for center in centers]

        return jsonify(center_list), 200

    except SQLAlchemyError as e:
        return jsonify({"msg": "Lỗi cơ sở dữ liệu!", "error": str(e)}), 500

    except Exception as e:
        return jsonify({"msg": "Hệ thống lỗi!", "error": str(e)}), 500
