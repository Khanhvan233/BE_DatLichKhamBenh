
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Text, SmallInteger, DECIMAL, CHAR, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from Service.Models import *

Base = declarative_base()

# class BacSi(Base):
#     __tablename__ = "bacsi"
#     id = Column('Id', Integer, primary_key=True, autoincrement=True)
#     hoc_ham = Column('HocHam', String(50), nullable=False)
#     ho = Column('Ho', CHAR(10), nullable=False)
#     ten = Column('Ten', CHAR(10), nullable=False)
#     hinh_anh = Column('Hinh_anh', CHAR(20), nullable=True)
#     mo_ta = Column('Mo_ta', String(4000), nullable=True)
#     ngay_bd_hanh_y = Column('Ngay_BD_Hanh_y', Date, nullable=False)
#     password = Column('Password', String(50), nullable=False)
    
# class BangCapChungChi(Base):
#     __tablename__ = "bangcap_chungchi"
    
#     id = Column('Id', Integer, primary_key=True, autoincrement=True)
#     bacsi_id = Column('BacSi_Id', Integer, ForeignKey('bacsi.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
#     ten_bangcap = Column('Ten_bangcap', String(200), nullable=False)
#     co_quan_cap = Column('Co_quan_cap', String(200), nullable=True)
#     ngay_cap = Column('Ngay_cap', Date, nullable=False)

#     # Relationship to BacSi table
#     bacsi = relationship("BacSi", back_populates="bangcap_chungchi")

class ClientAccount(Base):
    __tablename__ = "client_account"
    
    id = Column('Id', Integer, primary_key=True, autoincrement=True)
    username = Column('Username', CHAR(64), nullable=False)
    password = Column('Password', String(50), nullable=False)
    ho = Column('Ho', String(50), nullable=False)
    ten = Column('Ten', String(50), nullable=False)
    sdt = Column('SDT', DECIMAL(10, 0), nullable=False)
    email = Column('Email', String(255), nullable=True)

# class CTKhoa(Base):
#     __tablename__ = "ct_khoa"
    
#     id = Column('Id', Integer, primary_key=True, autoincrement=True)
#     bacsi_id = Column('BacSi_Id', Integer, ForeignKey('bacsi.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
#     khoa_id = Column('Khoa_Id', Integer, ForeignKey('khoa.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=True)

#     # Relationship to BacSi table
#     bacsi = relationship("BacSi", back_populates="ct_khoa")
#     # Relationship to Khoa table
#     khoa = relationship("Khoa", back_populates="ct_khoa")

# class DatHen(Base):
#     __tablename__ = "dat_hen"
    
#     id = Column('Id', Integer, primary_key=True, autoincrement=True)
#     user_account_id = Column('User_account_Id', Integer, ForeignKey('client_account.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
#     vanphong_id = Column('VanPhong_Id', Integer, ForeignKey('vanphong.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
#     gio_hen = Column('Gio_hen', DateTime, nullable=False)
#     gio_ket_thuc = Column('Gio_ket_thuc', DateTime, nullable=True)
#     trang_thai = Column('Trang_thai', CHAR(10), nullable=False)
#     ngay_gio_dat = Column('Ngay_gio_dat', DateTime, nullable=False)
#     kieu_dat = Column('Kieu_dat', Integer, ForeignKey('kieu_dat.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

#     # Relationships to user
#     user_account = relationship("ClientAccount", back_populates="dat_hen")
#     # Relationships to vanphon
#     vanphong = relationship("VanPhong", back_populates="dat_hen")
#     # Relationships to kieu dat
#     kieu_dat_relationship = relationship("KieuDat", back_populates="dat_hen")

# class Khoa(Base):
#     __tablename__ = "khoa"
    
#     id = Column('Id', Integer, primary_key=True, autoincrement=True)
#     ten_khoa = Column('Ten_khoa', String(100), nullable=False)

# class KieuDat(Base):
#     __tablename__ = "kieu_dat"
    
#     id = Column('Id', Integer, primary_key=True, autoincrement=True)
#     ten_loai_dat = Column('Ten_loai_dat', String(50), nullable=True)

# class LichTrinh(Base):
#     __tablename__ = "lichtrinh"
    
#     id = Column('Id', Integer, primary_key=True, autoincrement=True)
#     vanphong_id = Column('VanPhong_Id', Integer, ForeignKey('vanphong.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
#     day_of_week = Column('Day_of_week', String(16), nullable=False)
#     gio_bd = Column('Gio_BD', Time, nullable=False)
#     gio_kt = Column('Gio_KT', Time, nullable=False)
#     vang = Column('Vang', Integer, nullable=False)
#     ly_do = Column('Ly_do', String(500), nullable=True)
    
#     # Relationship to VanPhong table
#     vanphong = relationship("VanPhong", back_populates="lichtrinh")

# class LienKetBenhVien(Base):
#     __tablename__ = "lienketbenhvien"
    
#     id = Column('Id', Integer, primary_key=True, autoincrement=True)
#     bac_si_id = Column('BacSi_Id', Integer, ForeignKey('bacsi.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
#     ten_benh_vien = Column('Ten_BenhVien', String(100), nullable=False)
#     dia_chi = Column('Dia_chi', String(128), nullable=False)
#     ngay_db = Column('Ngay_DB', Date, nullable=False)
#     ngay_kt = Column('Ngay_KT', Date, nullable=True)
    
#     # Relationship to BacSi table
#     bac_si = relationship("BacSi", back_populates="lienketbenhvien")

# class Review(Base):
#     __tablename__ = "review"
    
#     id = Column('Id', Integer, primary_key=True, autoincrement=True)
#     user_account_id = Column('User_account_id', Integer, ForeignKey('client_account.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
#     bac_si_id = Column('BacSi_Id', Integer, ForeignKey('bacsi.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
#     vo_danh = Column('Vo_danh', Integer, nullable=False)
#     wai_time_rating = Column('Wai_time_rating', Integer, nullable=False)
#     danh_gia_bs = Column('Danh_gia_BS', Integer, nullable=False)
#     danh_gia_tong = Column('Danh_gia_tong', Integer, nullable=False)
#     review = Column('review', String(2000), nullable=True)
#     khuyen_khich = Column('Khuyen_khich', Integer, nullable=False)
#     ngay = Column('Ngay', Date, nullable=False)
    
#     # Relationship to BacSi and ClientAccount tables
#     bac_si = relationship("BacSi", back_populates="reviews")
#     user_account = relationship("ClientAccount", back_populates="reviews")

# class ThongTinBaoHiem(Base):
#     __tablename__ = "thongtinbaohiem"
    
#     id = Column('Id', Integer, primary_key=True, autoincrement=True)
#     van_phong_id = Column('VanPhong_Id', Integer, ForeignKey('vanphong.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
#     ten_bao_hiem = Column('Ten_bao_hiem', String(100), nullable=False)
    
#     # Relationship to VanPhong table
#     van_phong = relationship("VanPhong", back_populates="thongtinbaohiem")

# class VanPhong(Base):
#     __tablename__ = "vanphong"
    
#     id = Column('Id', Integer, primary_key=True, autoincrement=True)
#     bac_si_id = Column('BacSi_Id', Integer, ForeignKey('bacsi.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
#     lienketbenhvien_id = Column('lienketbenhvien_id', Integer, ForeignKey('lienketbenhvien.Id'), nullable=True)
#     thoi_luong_kham = Column('Thoi_Luong_Kham', Integer, nullable=False)
#     phi_gap_dau = Column('Phi_gap_dau', Integer, nullable=False)
#     phi_gap_sau = Column('Phi_gap_sau', Integer, nullable=False)
#     dia_chi = Column('Dia_chi', String(100), nullable=False)
    
#     # Relationship to BacSi
#     bac_si = relationship("BacSi", back_populates="vanphongs")
#     # Relationship to LienKetBenhVien
#     lienketbenhvien = relationship("LienKetBenhVien", back_populates="vanphongs")
