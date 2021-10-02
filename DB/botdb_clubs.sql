-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: botdb
-- ------------------------------------------------------
-- Server version	8.0.26

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
-- Table structure for table `clubs`
--

DROP TABLE IF EXISTS `clubs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clubs` (
  `name` varchar(30) DEFAULT NULL,
  `price` varchar(30) DEFAULT NULL,
  `posX` varchar(30) DEFAULT NULL,
  `posY` varchar(30) DEFAULT NULL,
  `info` varchar(200) DEFAULT NULL,
  `category` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clubs`
--

LOCK TABLES `clubs` WRITE;
/*!40000 ALTER TABLE `clubs` DISABLE KEYS */;
INSERT INTO `clubs` VALUES ('ДЮЦ на Молодёжной','0','20.513517','54.739452','Художественная школа с профессиональными преподавателями','3'),('Технопарк Кванториум','0','20.491602','54.73618','Изучение различных областей IT-сферы. От программирования до робототехники','2'),('Музыкальная школа им. Гофмана','0','20.524434','54.736402','Любые музыкальные инструменты, вокал и лучшие преподаватели','5'),('Школа греко-римской борьбы','1500','20.48217','54.74645','Школа, где учат постоять за себя. Обучение самообороне, участие в соревнованиях и многое другое','1'),('Футбольный клуб Балтика','3800','20.490132','54.717139','Научим играть в футбол любого ребёнка!','1'),('1С Клуб программистов','5000','20.497633','54.720593','Курсы программирования для школьников 10-16 лет — увлекательно и полезно','2'),('Школа искусств','1900','20.507545','54.705699','Разнообразные стили рисования, множество техник и всё-всё-всё!','3'),('Школа вокала','3700','20.509106','54.73579','Научим петь любого ребёнка. Разнообразные жанры и стили. Ждём всех!','5');
/*!40000 ALTER TABLE `clubs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-01 21:15:19
