import datetime
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort, redirect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
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
import base64
from Variable import *
from Service.FirebaseHandler import FirebaseHandler

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


book_blueprint = Blueprint('book', __name__)

@book_blueprint.route('/booking', methods=['POST'])
@jwt_required()
def dat_lich_kham():

    try:
        identity = get_jwt_identity()
        
        # Kiểm tra xem identity có phải là đối tượng hợp lệ và có trường 'role'
        if not identity or not isinstance(identity, dict) or "role" not in identity:
            return jsonify({"msg": "Token không hợp lệ"}), 400

        if identity["role"] != client:  # chỉ user mới đc book lịch khám
            return jsonify({"msg": "Bạn không có quyền đặt lịch khám"}), 403
        # Lấy dữ liệu từ yêu cầu JSON

        data = request.json
        user_account_id = data['user_account_id']
        vanphong_id = data['vanphong_id']
        gio_hen = datetime.strptime(data['gio_hen'], "%Y-%m-%d %H:%M:%S")

        # Kiểm tra sự tồn tại của user_account và vanphong
        user_account = session_db.query(ClientAccount).filter_by(id=user_account_id).first()
        vanphong = session_db.query(VanPhong).filter_by(id=vanphong_id).first()
        if not user_account:
            return jsonify({"error": "Người dùng không tồn tại"}), 404
        if not vanphong:
            return jsonify({"error": "Văn phòng không tồn tại"}), 404

        # Tạo lịch hẹn mới
        lich_hen = DatHen(
            user_account_id=user_account_id,
            vanphong_id=vanphong_id,
            gio_hen=gio_hen,
            gio_ket_thuc=None,  # Có thể thêm thông tin này nếu cần
            trang_thai=0,
            ngay_gio_dat=datetime.now(),
            kieu_dat=1
        )
        session_db.add(lich_hen)
        session_db.commit()

        return jsonify({"message": "Đặt lịch khám thành công", "lich_hen_id": lich_hen.id}), 201

    except Exception as e:
        session_db.rollback()
        return jsonify({"error": str(e)}), 500
    
@book_blueprint.route('/appointments/<int:user_account_id>', methods=['GET'])
def get_user_appointments(user_account_id):
    try:
        # Kiểm tra sự tồn tại của user_account
        user_account = session_db.query(ClientAccount).filter_by(id=user_account_id).first()
        if not user_account:
            return jsonify({"error": "Người dùng không tồn tại"}), 404

        # Truy vấn danh sách các lịch hẹn của user
        appointments = session_db.query(DatHen).filter_by(user_account_id=user_account_id).all()

        # Xử lý nếu không có lịch hẹn nào
        if not appointments:
            return jsonify({"message": "Người dùng chưa đặt lịch hẹn nào"}), 404

        # Chuẩn bị dữ liệu trả về
        appointments_list = []
        for appointment in appointments:
            appointments_list.append({
                "id": appointment.id,
                "vanphong_id": appointment.vanphong_id,
                "gio_hen": appointment.gio_hen.strftime("%Y-%m-%d %H:%M:%S") if appointment.gio_hen else None,
                "trang_thai": appointment.trang_thai,
                "ngay_gio_dat": appointment.ngay_gio_dat.strftime("%Y-%m-%d %H:%M:%S") if appointment.ngay_gio_dat else None,
                "kieu_dat": appointment.kieu_dat,
            })

        return jsonify({"appointments": appointments_list}), 200

    except Exception as e:
        session_db.rollback()
        return jsonify({"error": str(e)}), 500
