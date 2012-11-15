-- MySQL dump 10.13  Distrib 5.5.27, for Linux (i686)
--
-- Host: localhost    Database: EST863
-- ------------------------------------------------------
-- Server version	5.5.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


--
-- Table structure for table `S_User_Role`
--

IF NOT EXISTS `S_User_Role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `S_User_Role` (
  `RoleID` int(11) NOT NULL AUTO_INCREMENT,
  `RoleName` varchar(50) NOT NULL,
  PRIMARY KEY (`RoleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `S_User_Role`
--

LOCK TABLES `S_User_Role` WRITE;
/*!40000 ALTER TABLE `S_User_Role` DISABLE KEYS */;
/*!40000 ALTER TABLE `S_User_Role` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `S_Language_Enum`
--

IF NOT EXISTS `S_Language_Enum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `S_Language_Enum` (
  `LanguageID` int(11) NOT NULL AUTO_INCREMENT,
  `LanguageStr` varchar(50) NOT NULL,
  PRIMARY KEY (`LanguageID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `S_Language_Enum`
--

LOCK TABLES `S_Language_Enum` WRITE;
/*!40000 ALTER TABLE `S_Language_Enum` DISABLE KEYS */;
/*!40000 ALTER TABLE `S_Language_Enum` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `S_Compound_Info`
--

IF NOT EXISTS `S_Compound_Info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `S_Compound_Info` (
  `Smiles` varchar(200) NOT NULL,
  `CAS` varchar(15) NOT NULL,
  PRIMARY KEY (`Smiles`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `S_Compound_Info`
--

LOCK TABLES `S_Compound_Info` WRITE;
/*!40000 ALTER TABLE `S_Compound_Info` DISABLE KEYS */;
/*!40000 ALTER TABLE `S_Compound_Info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `S_Active_KeyInfo`
--

IF NOT EXISTS `S_Active_KeyInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `S_Active_KeyInfo` (
  `KeyID` int(11) NOT NULL AUTO_INCREMENT,
  `KeyValue` char(36) NOT NULL,
  `TotalCount` int(11) NOT NULL,
  `LeftCount` int(11) NOT NULL,
  PRIMARY KEY (`KeyID`),
  UNIQUE KEY `KeyValue` (`KeyValue`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `S_Active_KeyInfo`
--

LOCK TABLES `S_Active_KeyInfo` WRITE;
/*!40000 ALTER TABLE `S_Active_KeyInfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `S_Active_KeyInfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `S_User_Info`
--

IF NOT EXISTS `S_User_Info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `S_User_Info` (
  `Username` varchar(200) NOT NULL,
  `Password` varchar(200) NOT NULL,
  `WorkUnit` varchar(2000) DEFAULT NULL,
  `Address` varchar(2000) DEFAULT NULL,
  `Emails` varchar(200) NOT NULL,
  `Tel` varchar(50) DEFAULT NULL,
  `RoleID` int(11) NOT NULL,
  PRIMARY KEY (`Username`),
  KEY `RoleID` (`RoleID`),
  CONSTRAINT `S_User_Info_ibfk_1` FOREIGN KEY (`RoleID`) REFERENCES `S_User_Role` (`RoleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `S_User_Info`
--

LOCK TABLES `S_User_Info` WRITE;
/*!40000 ALTER TABLE `S_User_Info` DISABLE KEYS */;
/*!40000 ALTER TABLE `S_User_Info` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `H_Active_History`
--

IF NOT EXISTS `H_Active_History`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `H_Active_History` (
  `ActiveID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(200) NOT NULL,
  `ActiveTime` datetime NOT NULL,
  `ActiveIP` char(50) NOT NULL,
  `AntiActiveTime` datetime DEFAULT NULL,
  `AntiActiveIP` char(50) DEFAULT NULL,
  `KeyID` int(11) NOT NULL,
  `MachineCode` char(32) NOT NULL,
  PRIMARY KEY (`ActiveID`),
  KEY `Username` (`Username`),
  KEY `KeyID` (`KeyID`),
  CONSTRAINT `H_Active_History_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `S_User_Info` (`Username`),
  CONSTRAINT `H_Active_History_ibfk_2` FOREIGN KEY (`KeyID`) REFERENCES `S_Active_KeyInfo` (`KeyID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `H_Active_History`
--

LOCK TABLES `H_Active_History` WRITE;
/*!40000 ALTER TABLE `H_Active_History` DISABLE KEYS */;
/*!40000 ALTER TABLE `H_Active_History` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `S_Model_Info`
--

IF NOT EXISTS `S_Model_Info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `S_Model_Info` (
  `ModelID` int(11) NOT NULL AUTO_INCREMENT,
  `ModelName` varchar(200) NOT NULL,
  PRIMARY KEY (`ModelID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `S_Model_Info`
--

LOCK TABLES `S_Model_Info` WRITE;
/*!40000 ALTER TABLE `S_Model_Info` DISABLE KEYS */;
/*!40000 ALTER TABLE `S_Model_Info` ENABLE KEYS */;
UNLOCK TABLES;
--
-- Table structure for table `H_Calculate_History`
--

IF NOT EXISTS `H_Calculate_History`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `H_Calculate_History` (
  `CalID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(200) NOT NULL,
  `CalStarttime` datetime NOT NULL,
  `CalEndtime` datetime NOT NULL,
  `Smiles` varchar(200) NOT NULL,
  `ModelID` int(11) NOT NULL,
  `Param` text,
  `Result` mediumtext,
  PRIMARY KEY (`CalID`),
  KEY `Username` (`Username`),
  KEY `ModelID` (`ModelID`),
  KEY `Smiles` (`Smiles`),
  CONSTRAINT `H_Calculate_History_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `S_User_Info` (`Username`),
  CONSTRAINT `H_Calculate_History_ibfk_2` FOREIGN KEY (`ModelID`) REFERENCES `S_Model_Info` (`ModelID`),
  CONSTRAINT `H_Calculate_History_ibfk_3` FOREIGN KEY (`Smiles`) REFERENCES `S_Compound_Info` (`Smiles`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `H_Calculate_History`
--

LOCK TABLES `H_Calculate_History` WRITE;
/*!40000 ALTER TABLE `H_Calculate_History` DISABLE KEYS */;
/*!40000 ALTER TABLE `H_Calculate_History` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `S_Compound_Name`
--

IF NOT EXISTS `S_Compound_Name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `S_Compound_Name` (
  `NameID` int(11) NOT NULL AUTO_INCREMENT,
  `Smiles` varchar(200) NOT NULL,
  `NameStr` varchar(500) NOT NULL,
  `LanguageID` int(11) NOT NULL,
  `IsDefault` bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (`NameID`),
  KEY `CAS` (`Smiles`),
  KEY `LanguageID` (`LanguageID`),
  CONSTRAINT `S_Compound_Name_ibfk_1` FOREIGN KEY (`Smiles`) REFERENCES `S_Compound_Info` (`Smiles`),
  CONSTRAINT `S_Compound_Name_ibfk_2` FOREIGN KEY (`LanguageID`) REFERENCES `S_Language_Enum` (`LanguageID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `S_Compound_Name`
--

LOCK TABLES `S_Compound_Name` WRITE;
/*!40000 ALTER TABLE `S_Compound_Name` DISABLE KEYS */;
/*!40000 ALTER TABLE `S_Compound_Name` ENABLE KEYS */;
UNLOCK TABLES;



/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-10-31 12:08:46
