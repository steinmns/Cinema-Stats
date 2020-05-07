-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: moviesheet
-- ------------------------------------------------------
-- Server version	8.0.18

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
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log` (
  `LOG_ID` int(11) NOT NULL AUTO_INCREMENT,
  `LOG_MOVIE_TITLE` varchar(100) NOT NULL,
  `LOG_MOVIE_DATE` date NOT NULL,
  `LOG_MOVIE_RATING` int(11) NOT NULL,
  `LOG_MOVIE_GENRE` varchar(20) NOT NULL,
  `LOG_MOVIE_LOCATION` varchar(20) DEFAULT NULL,
  `LOG_MOVIE_COMMENTS` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`LOG_ID`),
  UNIQUE KEY `idlog_UNIQUE` (`LOG_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Main Movie Log - Could possibly be expanded later for a user to user basis.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log`
--

LOCK TABLES `log` WRITE;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
INSERT INTO `log` VALUES (28,'Alien','2019-02-04',7,'Sci-Fi','Home','Ahead of its time. '),(30,'Shawshank Redemption','2019-03-12',7,'Drama','Home','Great movie!'),(32,'The Good, The Bad, and The Ugly','2019-05-14',8,'Western','Home','Soundtrack is still burnt into my head'),(34,'Once Upon a Time in Hollywood','2019-07-17',8,'Drama','Theater','Edit Test 3'),(35,'Free Solo','2019-08-15',8,'Documentary','Theater','Thrilling!'),(36,'Isle of Dogs','2019-10-14',7,'Animated','Theater',''),(37,'Moonlight','2019-10-17',10,'Drama','Home','Masterpiece'),(39,'Manufactured Landscapes','2019-11-12',9,'Documentary','Home',''),(41,'Cold War','2019-01-22',9,'Drama','Theater',''),(45,'La La Land','2019-06-16',8,'Musical','Home',''),(47,'Dunkirk','2019-08-05',7,'War','Theater',''),(49,'Pulp Fiction','2019-11-14',7,'Drama',NULL,'');
/*!40000 ALTER TABLE `log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settings` (
  `SETTINGS_ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `SETTINGS_APP_THEME` varchar(15) NOT NULL,
  `SETTINGS_FONT_SIZE` varchar(15) NOT NULL COMMENT 'May change this to an into down the line',
  `SETTINGS_GRAPH_THEME` varchar(45) NOT NULL,
  PRIMARY KEY (`SETTINGS_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES (1,'Default (Light)','Default','bmh');
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-07 11:17:49
