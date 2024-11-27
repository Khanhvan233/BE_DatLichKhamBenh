-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: dat_lich_kham
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bacsi`
--

DROP TABLE IF EXISTS `bacsi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bacsi` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `HocHam` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Ho` char(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Ten` char(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Hinh_anh` char(20) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Mo_ta` varchar(4000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Ngay_BD_Hanh_y` date NOT NULL,
  `Password` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bacsi`
--

LOCK TABLES `bacsi` WRITE;
/*!40000 ALTER TABLE `bacsi` DISABLE KEYS */;
INSERT INTO `bacsi` VALUES (1,'BS.','Nguyễn','Thành Long',NULL,'123','2003-09-09','123'),(2,'BS.','Lê','Anh Tình',NULL,'123','2003-09-09','123'),(3,'BS.','Trần Ngọc','Khánh Văn',NULL,'123','2003-09-09','123'),(4,'BS.','Vũ','Đức Trọng',NULL,'123','2003-09-09','123'),(5,'Ths.Bs.','Nguyễn','A',NULL,'123','2003-09-09','123');
/*!40000 ALTER TABLE `bacsi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bangcap_chungchi`
--

DROP TABLE IF EXISTS `bangcap_chungchi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bangcap_chungchi` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `BacSi_Id` int NOT NULL,
  `Ten_bangcap` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Co_quan_cap` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Ngay_cap` date NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_BangCap_ChungChi_BacSi` (`BacSi_Id`),
  CONSTRAINT `FK_BangCap_ChungChi_BacSi` FOREIGN KEY (`BacSi_Id`) REFERENCES `bacsi` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bangcap_chungchi`
--

LOCK TABLES `bangcap_chungchi` WRITE;
/*!40000 ALTER TABLE `bangcap_chungchi` DISABLE KEYS */;
INSERT INTO `bangcap_chungchi` VALUES (1,1,'Bằng BS','Bệnh Viện A','2023-09-09'),(2,2,'Bằng BS','Bệnh Viện A','2023-09-09'),(3,3,'Bằng BS','Bệnh Viện A','2023-09-09'),(4,4,'Bằng BS','Bệnh Viện A','2023-09-09'),(5,5,'Bằng Ths','Bệnh Viện A','2023-09-09');
/*!40000 ALTER TABLE `bangcap_chungchi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client_account`
--

DROP TABLE IF EXISTS `client_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client_account` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Username` char(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Password` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Ho` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Ten` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `SDT` decimal(10,0) NOT NULL,
  `Email` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_account`
--

LOCK TABLES `client_account` WRITE;
/*!40000 ALTER TABLE `client_account` DISABLE KEYS */;
INSERT INTO `client_account` VALUES (1,'pakamon','123','Nguyễn','Thành Long',123456789,'ttt@gmail.com'),(2,'sakura','123','Nguyễn','Thành Long',123456789,'ttt@gmail.com'),(3,'neko','123','Nguyễn','Thành Long',123456789,'ttt@gmail.com'),(4,'chan','123','Nguyễn','Thành Long',123456789,'ttt@gmail.com');
/*!40000 ALTER TABLE `client_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ct_khoa`
--

DROP TABLE IF EXISTS `ct_khoa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ct_khoa` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `BacSi_Id` int NOT NULL,
  `Khoa_Id` int DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_CT_Khoa_BacSi` (`BacSi_Id`),
  KEY `FK_CT_Khoa_Khoa` (`Khoa_Id`),
  CONSTRAINT `FK_CT_Khoa_BacSi` FOREIGN KEY (`BacSi_Id`) REFERENCES `bacsi` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_CT_Khoa_Khoa` FOREIGN KEY (`Khoa_Id`) REFERENCES `khoa` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ct_khoa`
--

LOCK TABLES `ct_khoa` WRITE;
/*!40000 ALTER TABLE `ct_khoa` DISABLE KEYS */;
INSERT INTO `ct_khoa` VALUES (1,1,1),(2,2,1),(3,3,4),(4,4,1),(5,5,1),(6,1,2),(7,2,2),(8,3,2),(9,4,2),(10,4,2);
/*!40000 ALTER TABLE `ct_khoa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dat_hen`
--

DROP TABLE IF EXISTS `dat_hen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dat_hen` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `User_account_Id` int NOT NULL,
  `VanPhong_Id` int NOT NULL,
  `Gio_hen` datetime(3) NOT NULL,
  `Gio_ket_thuc` datetime(3) DEFAULT NULL,
  `Trang_thai` char(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Ngay_gio_dat` datetime(3) NOT NULL,
  `Kieu_dat` int NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_Dat_hen_Client_account` (`User_account_Id`),
  KEY `FK_Dat_hen_Kieu_dat` (`Kieu_dat`),
  KEY `FK_Dat_hen_VanPhong` (`VanPhong_Id`),
  CONSTRAINT `FK_Dat_hen_Client_account` FOREIGN KEY (`User_account_Id`) REFERENCES `client_account` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_Dat_hen_Kieu_dat` FOREIGN KEY (`Kieu_dat`) REFERENCES `kieu_dat` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_Dat_hen_VanPhong` FOREIGN KEY (`VanPhong_Id`) REFERENCES `vanphong` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dat_hen`
--

LOCK TABLES `dat_hen` WRITE;
/*!40000 ALTER TABLE `dat_hen` DISABLE KEYS */;
INSERT INTO `dat_hen` VALUES (2,1,2,'2024-09-01 07:00:00.000',NULL,'0','2024-09-01 06:00:00.000',1);
/*!40000 ALTER TABLE `dat_hen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `khoa`
--

DROP TABLE IF EXISTS `khoa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `khoa` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Ten_khoa` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `khoa`
--

LOCK TABLES `khoa` WRITE;
/*!40000 ALTER TABLE `khoa` DISABLE KEYS */;
INSERT INTO `khoa` VALUES (1,'Khoa Thần Kinh'),(2,'Khoa Vật Lý Trị Liệu'),(3,'Khoa Lao'),(4,'Khoa Nội tổng hợp'),(5,'Khoa Nội tiêu hóa'),(6,'Khoa Nội tim mạch'),(7,'Khoa Nội cơ – xương – khớp'),(8,'Khoa Nội thận – tiết niệu'),(9,'Khoa Truyền nhiễm'),(10,'Khoa Da Liễu'),(11,'Khoa Y học cổ truyền'),(12,'Khoa Nhi'),(13,'Khoa Ngoại thần kinh'),(14,'Khoa Phụ sản'),(15,'Khoa Tai – mũi – họng'),(16,'Khoa Răng - hàm – mặt'),(17,'Khoa mắt');
/*!40000 ALTER TABLE `khoa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kieu_dat`
--

DROP TABLE IF EXISTS `kieu_dat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kieu_dat` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Ten_loai_dat` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kieu_dat`
--

LOCK TABLES `kieu_dat` WRITE;
/*!40000 ALTER TABLE `kieu_dat` DISABLE KEYS */;
INSERT INTO `kieu_dat` VALUES (1,'Online trung gian'),(2,'SDT'),(3,'Online bệnh viện');
/*!40000 ALTER TABLE `kieu_dat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lichtrinh`
--

DROP TABLE IF EXISTS `lichtrinh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lichtrinh` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `VanPhong_Id` int DEFAULT NULL,
  `Day_of_week` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Gio_BD` time(5) NOT NULL,
  `Gio_KT` time(5) NOT NULL,
  `Vang` tinyint NOT NULL,
  `Ly_do` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_LichTrinh_VanPhong` (`VanPhong_Id`),
  CONSTRAINT `FK_LichTrinh_VanPhong` FOREIGN KEY (`VanPhong_Id`) REFERENCES `vanphong` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lichtrinh`
--

LOCK TABLES `lichtrinh` WRITE;
/*!40000 ALTER TABLE `lichtrinh` DISABLE KEYS */;
INSERT INTO `lichtrinh` VALUES (2,2,'Thứ Hai','07:00:00.00000','17:00:00.00000',0,'');
/*!40000 ALTER TABLE `lichtrinh` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lienketbenhvien`
--

DROP TABLE IF EXISTS `lienketbenhvien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lienketbenhvien` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `BacSi_Id` int NOT NULL,
  `Ten_BenhVien` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Dia_chi` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Ngay_DB` date NOT NULL,
  `Ngay_KT` date DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_LienKetBenhVien_BacSi` (`BacSi_Id`),
  CONSTRAINT `FK_LienKetBenhVien_BacSi` FOREIGN KEY (`BacSi_Id`) REFERENCES `bacsi` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lienketbenhvien`
--

LOCK TABLES `lienketbenhvien` WRITE;
/*!40000 ALTER TABLE `lienketbenhvien` DISABLE KEYS */;
INSERT INTO `lienketbenhvien` VALUES (1,1,'Bệnh Viện A','Quận 9','2021-09-09',NULL),(2,2,'Bệnh Viện B','Quận 9','2021-09-09',NULL),(3,3,'Bệnh Viện C','Quận 9','2021-09-09',NULL),(4,4,'Bệnh Viện D','Quận 9','2021-09-09',NULL),(5,5,'Bệnh Viện E','Quận 9','2021-09-09',NULL);
/*!40000 ALTER TABLE `lienketbenhvien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `User_account_id` int NOT NULL,
  `BacSi_Id` int NOT NULL,
  `Vo_danh` tinyint NOT NULL,
  `Wai_time_rating` int NOT NULL,
  `Danh_gia_BS` int NOT NULL,
  `Danh_gia_tong` int NOT NULL,
  `review` varchar(2000) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `Khuyen_khich` tinyint NOT NULL,
  `Ngay` date NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_Review_BacSi` (`BacSi_Id`),
  KEY `FK_Review_Client_account` (`User_account_id`),
  CONSTRAINT `FK_Review_BacSi` FOREIGN KEY (`BacSi_Id`) REFERENCES `bacsi` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_Review_Client_account` FOREIGN KEY (`User_account_id`) REFERENCES `client_account` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `thongtinbaohiem`
--

DROP TABLE IF EXISTS `thongtinbaohiem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `thongtinbaohiem` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `VanPhong_Id` int NOT NULL,
  `Ten_bao_hiem` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_ThongTinBaoHiem_VanPhong` (`VanPhong_Id`),
  CONSTRAINT `FK_ThongTinBaoHiem_VanPhong` FOREIGN KEY (`VanPhong_Id`) REFERENCES `vanphong` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `thongtinbaohiem`
--

LOCK TABLES `thongtinbaohiem` WRITE;
/*!40000 ALTER TABLE `thongtinbaohiem` DISABLE KEYS */;
INSERT INTO `thongtinbaohiem` VALUES (1,2,'Bảo hiểm Nhân Thọ'),(2,3,'Bảo hiểm Nhân Thọ'),(3,4,'Bảo hiểm Nhân Thọ'),(4,5,'Bảo hiểm Nhân Thọ'),(5,6,'Bảo hiểm Nhân Thọ');
/*!40000 ALTER TABLE `thongtinbaohiem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vanphong`
--

DROP TABLE IF EXISTS `vanphong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vanphong` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `BacSi_Id` int NOT NULL,
  `lienketbenhvien_id` int DEFAULT NULL,
  `Thoi_Luong_Kham` int NOT NULL,
  `Phi_gap_dau` int NOT NULL,
  `Phi_gap_sau` int NOT NULL,
  `Dia_chi` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `FK_VanPhong_BacSi` (`BacSi_Id`),
  KEY `FK_VanPhong_LienKetBenhVien` (`lienketbenhvien_id`),
  CONSTRAINT `FK_VanPhong_BacSi` FOREIGN KEY (`BacSi_Id`) REFERENCES `bacsi` (`Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_VanPhong_LienKetBenhVien` FOREIGN KEY (`lienketbenhvien_id`) REFERENCES `lienketbenhvien` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vanphong`
--

LOCK TABLES `vanphong` WRITE;
/*!40000 ALTER TABLE `vanphong` DISABLE KEYS */;
INSERT INTO `vanphong` VALUES (2,1,1,60,250000,200000,'Quận 9'),(3,2,2,45,250000,200000,'Quận 9'),(4,3,3,45,250000,200000,'Quận 9'),(5,4,4,70,250000,200000,'Quận 9'),(6,1,1,40,250000,200000,'Quận 9');
/*!40000 ALTER TABLE `vanphong` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-27 15:37:40
