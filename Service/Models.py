from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Text, SmallInteger, DECIMAL, CHAR, DateTime, VARCHAR, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BacSi(Base):
    __tablename__ = "bacsi"

    id = Column('Id', Integer, primary_key=True, autoincrement=True)
    hoc_ham = Column('HocHam', String(50), nullable=False)
    ho = Column('Ho', CHAR(10), nullable=False)
    ten = Column('Ten', CHAR(10), nullable=False)
    hinh_anh = Column('Hinh_anh', VARCHAR(255), nullable=True)
    mo_ta = Column('Mo_ta', String(4000), nullable=True)
    ngay_bd_hanh_y = Column('Ngay_BD_Hanh_y', Date, nullable=False)
    password = Column('Password', String(50), nullable=False)
    username = Column('Username', CHAR(64), nullable=False)

    lienketbenhvien = relationship("LienKetBenhVien", back_populates="bacsi")
    ct_khoa = relationship("CTKhoa", back_populates="bacsi")
    bangcap_chungchi = relationship("BangCapChungChi", back_populates="bacsi")
    vanphongs = relationship("VanPhong", back_populates="bac_si")
    reviews = relationship("Review", back_populates="bac_si")


class LienKetBenhVien(Base):
    __tablename__ = "lienketbenhvien"

    id = Column('Id', Integer, primary_key=True, autoincrement=True)
    bac_si_id = Column('BacSi_Id', Integer, ForeignKey('bacsi.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    ten_benh_vien = Column('Ten_BenhVien', String(100), nullable=False)
    dia_chi = Column('Dia_chi', String(128), nullable=False)
    ngay_db = Column('Ngay_DB', Date, nullable=False)
    ngay_kt = Column('Ngay_KT', Date, nullable=True)

    bacsi = relationship("BacSi", back_populates="lienketbenhvien")
    vanphongs = relationship("VanPhong", back_populates="lienketbenhvien")


class ClientAccount(Base):
    __tablename__ = "client_account"

    id = Column('Id', Integer, primary_key=True, autoincrement=True)
    username = Column('Username', CHAR(64), nullable=False)
    password = Column('Password', String(50), nullable=False)
    ho = Column('Ho', String(50), nullable=False)
    ten = Column('Ten', String(50), nullable=False)
    sdt = Column('SDT', DECIMAL(10, 0), nullable=False)
    email = Column('Email', String(255), nullable=True)
    cccd = Column('CCCD', String(255), nullable=True)

    dat_hen = relationship("DatHen", back_populates="user_account")
    reviews = relationship("Review", back_populates="user_account")


class Khoa(Base):
    __tablename__ = "khoa"

    id = Column('Id', Integer, primary_key=True, autoincrement=True)
    ten_khoa = Column('Ten_khoa', String(100), nullable=False)

    ct_khoa = relationship("CTKhoa", back_populates="khoa")


class CTKhoa(Base):
    __tablename__ = "ct_khoa"

    id = Column('Id', Integer, primary_key=True, autoincrement=True)
    bacsi_id = Column('BacSi_Id', Integer, ForeignKey('bacsi.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    khoa_id = Column('Khoa_Id', Integer, ForeignKey('khoa.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=True)

    bacsi = relationship("BacSi", back_populates="ct_khoa")
    khoa = relationship("Khoa", back_populates="ct_khoa")


class BangCapChungChi(Base):
    __tablename__ = "bangcap_chungchi"

    id = Column('Id', Integer, primary_key=True, autoincrement=True)
    bacsi_id = Column('BacSi_Id', Integer, ForeignKey('bacsi.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    ten_bangcap = Column('Ten_bangcap', String(200), nullable=False)
    co_quan_cap = Column('Co_quan_cap', String(200), nullable=True)
    ngay_cap = Column('Ngay_cap', Date, nullable=False)

    bacsi = relationship("BacSi", back_populates="bangcap_chungchi")


class DatHen(Base):
    __tablename__ = "dat_hen"

    id = Column('Id', Integer, primary_key=True, autoincrement=True)
    user_account_id = Column('User_account_Id', Integer, ForeignKey('client_account.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    vanphong_id = Column('VanPhong_Id', Integer, ForeignKey('vanphong.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    gio_hen = Column('Gio_hen', DateTime, nullable=False)
    gio_ket_thuc = Column('Gio_ket_thuc', DateTime, nullable=True)
    trang_thai = Column('Trang_thai', CHAR(10), nullable=False)
    ngay_gio_dat = Column('Ngay_gio_dat', DateTime, nullable=False)
    kieu_dat = Column('Kieu_dat', Integer, ForeignKey('kieu_dat.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    user_account = relationship("ClientAccount", back_populates="dat_hen")
    vanphong = relationship("VanPhong", back_populates="dat_hen")
    kieu_dat_relationship = relationship("KieuDat", back_populates="dat_hen")


class KieuDat(Base):
    __tablename__ = "kieu_dat"

    id = Column('Id', Integer, primary_key=True, autoincrement=True)
    ten_loai_dat = Column('Ten_loai_dat', String(50), nullable=True)

    dat_hen = relationship("DatHen", back_populates="kieu_dat_relationship")

class VanPhong(Base):
    __tablename__ = "vanphong"

    id = Column('Id', Integer, primary_key=True, autoincrement=True)  # Đảm bảo cột này tồn tại
    bac_si_id = Column('BacSi_Id', Integer, ForeignKey('bacsi.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    lienketbenhvien_id = Column('lienketbenhvien_id', Integer, ForeignKey('lienketbenhvien.Id'), nullable=True)
    thoi_luong_kham = Column('Thoi_Luong_Kham', Integer, nullable=False)
    phi_gap_dau = Column('Phi_gap_dau', Integer, nullable=False)
    phi_gap_sau = Column('Phi_gap_sau', Integer, nullable=False)
    dia_chi = Column('Dia_chi', String(100), nullable=False)

    bac_si = relationship("BacSi", back_populates="vanphongs")
    lienketbenhvien = relationship("LienKetBenhVien", back_populates="vanphongs")
    dat_hen = relationship("DatHen", back_populates="vanphong")
    lichtrinhs = relationship("LichTrinh", back_populates="vanphong")
    thongtinbaohiems = relationship("ThongTinBaoHiem", back_populates="vanphong")

class LichTrinh(Base):
    __tablename__ = 'lichtrinh'

    id = Column(Integer, primary_key=True)
    vanPhong_id = Column(Integer, ForeignKey('vanphong.Id'))  # Chữ "Id" viết hoa để khớp với định nghĩa trong VanPhong
    day_of_week = Column(String(16), nullable=False)
    gio_bd = Column(Time, nullable=False)
    gio_kt = Column(Time, nullable=False)
    vang = Column(Boolean, nullable=False)
    ly_do = Column(String(500), nullable=True)

    # Quan hệ với bảng vanphong
    vanphong = relationship("VanPhong", back_populates="lichtrinhs")


class ThongTinBaoHiem(Base):
    __tablename__ = 'thongtinbaohiem'

    id = Column(Integer, primary_key=True)
    ten_bao_hiem = Column(String(100), nullable=False)
    vanPhong_id = Column(Integer, ForeignKey('vanphong.Id'), nullable=False)

    # Quan hệ với bảng vanphong
    vanphong = relationship("VanPhong", back_populates="thongtinbaohiems")

class Review(Base):
    __tablename__ = "review"

    id = Column('Id', Integer, primary_key=True, autoincrement=True)
    user_account_id = Column('User_account_id', Integer, ForeignKey('client_account.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    bac_si_id = Column('BacSi_Id', Integer, ForeignKey('bacsi.Id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    vo_danh = Column('Vo_danh', SmallInteger, nullable=False)
    wai_time_rating = Column('Wai_time_rating', Integer, nullable=False)
    danh_gia_bs = Column('Danh_gia_BS', Integer, nullable=False)
    danh_gia_tong = Column('Danh_gia_tong', Integer, nullable=False)
    review = Column('review', String(2000), nullable=True)
    khuyen_khich = Column('Khuyen_khich', SmallInteger, nullable=False)
    ngay = Column('Ngay', Date, nullable=False)

    # Quan hệ với bảng ClientAccount
    user_account = relationship("ClientAccount", back_populates="reviews")

    # Quan hệ với bảng BacSi
    bac_si = relationship("BacSi", back_populates="reviews")
