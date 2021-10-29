CREATE DATABASE  IF NOT EXISTS `anita` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `anita`;
-- MySQL dump 10.13  Distrib 8.0.25, for Linux (x86_64)
--
-- Host: localhost    Database: anita
-- ------------------------------------------------------
-- Server version	5.7.35

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
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `country` (
  `country` varchar(100) NOT NULL,
  `alpha2code` varchar(2) NOT NULL,
  `alpha3code` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`country`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback` (
  `id_feedback` int(11) NOT NULL AUTO_INCREMENT,
  `id` int(11) NOT NULL,
  `score` varchar(100) DEFAULT NULL,
  `message` varchar(5000) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `product` varchar(200) DEFAULT NULL,
  `user` varchar(100) DEFAULT NULL,
  `deals` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_feedback`)
) ENGINE=InnoDB AUTO_INCREMENT=3894 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ints`
--

DROP TABLE IF EXISTS `ints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ints` (
  `i` int(11) NOT NULL,
  PRIMARY KEY (`i`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `timestamp` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `market` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `vendor` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `ships_from` varchar(2000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ships_to` varchar(2000) COLLATE utf8_unicode_ci DEFAULT NULL,
  `price` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `price_eur` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `info` longtext COLLATE utf8_unicode_ci,
  `feedback` int(11) DEFAULT NULL,
  PRIMARY KEY (`timestamp`,`market`,`name`,`vendor`,`price`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `products_cleaned`
--

DROP TABLE IF EXISTS `products_cleaned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_cleaned` (
  `timestamp` varchar(255) DEFAULT NULL,
  `market` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `vendor` varchar(225) DEFAULT NULL,
  `ships_from` varchar(255) DEFAULT NULL,
  `ships_to` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `macro_category` varchar(255) DEFAULT NULL,
  KEY `index1` (`vendor`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pseudonymized_vendors`
--

DROP TABLE IF EXISTS `pseudonymized_vendors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pseudonymized_vendors` (
  `alias` varchar(255) DEFAULT NULL,
  `pseudonym` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `feedback_id` varchar(255) DEFAULT NULL,
  `id` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `message` longtext,
  `product` varchar(255) DEFAULT NULL,
  `deals` varchar(255) DEFAULT NULL,
  `market` varchar(255) DEFAULT NULL,
  `timestamp` varchar(255) DEFAULT NULL,
  `macro_category` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sonarqube`
--

DROP TABLE IF EXISTS `sonarqube`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sonarqube` (
  `timestamp` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `project_name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `page` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `label` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `label_three` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `number_links` double DEFAULT NULL,
  `number_of_words` double DEFAULT NULL,
  `min_words_in_sentence` double DEFAULT NULL,
  `max_words_in_sentence` double DEFAULT NULL,
  `bitcoin` bit(1) DEFAULT NULL,
  `deep_web` bit(1) DEFAULT NULL,
  `new_technical_debt` double DEFAULT NULL,
  `blocker_violations` double DEFAULT NULL,
  `bugs` double DEFAULT NULL,
  `burned_budget` double DEFAULT NULL,
  `business_value` double DEFAULT NULL,
  `classes` double DEFAULT NULL,
  `code_smells` double DEFAULT NULL,
  `cognitive_complexity` double DEFAULT NULL,
  `comment_lines` double DEFAULT NULL,
  `comment_lines_data` double DEFAULT NULL,
  `comment_lines_density` double DEFAULT NULL,
  `class_complexity` double DEFAULT NULL,
  `file_complexity` double DEFAULT NULL,
  `function_complexity` double DEFAULT NULL,
  `complexity_in_classes` double DEFAULT NULL,
  `complexity_in_functions` double DEFAULT NULL,
  `branch_coverage` double DEFAULT NULL,
  `new_branch_coverage` double DEFAULT NULL,
  `conditions_to_cover` double DEFAULT NULL,
  `new_conditions_to_cover` double DEFAULT NULL,
  `confirmed_issues` double DEFAULT NULL,
  `coverage` double DEFAULT NULL,
  `new_coverage` double DEFAULT NULL,
  `critical_violations` double DEFAULT NULL,
  `complexity` double DEFAULT NULL,
  `last_commit_date` double DEFAULT NULL,
  `development_cost` double DEFAULT NULL,
  `new_development_cost` double DEFAULT NULL,
  `directories` double DEFAULT NULL,
  `duplicated_blocks` double DEFAULT NULL,
  `new_duplicated_blocks` double DEFAULT NULL,
  `duplicated_files` double DEFAULT NULL,
  `duplicated_lines` double DEFAULT NULL,
  `duplicated_lines_density` double DEFAULT NULL,
  `new_duplicated_lines_density` double DEFAULT NULL,
  `new_duplicated_lines` double DEFAULT NULL,
  `duplications_data` double DEFAULT NULL,
  `effort_to_reach_maintainability_rating_a` double DEFAULT NULL,
  `executable_lines_data` double DEFAULT NULL,
  `false_positive_issues` double DEFAULT NULL,
  `file_complexity_distribution` double DEFAULT NULL,
  `files` double DEFAULT NULL,
  `function_complexity_distribution` double DEFAULT NULL,
  `functions` double DEFAULT NULL,
  `generated_lines` double DEFAULT NULL,
  `generated_ncloc` double DEFAULT NULL,
  `info_violations` double DEFAULT NULL,
  `violations` double DEFAULT NULL,
  `line_coverage` double DEFAULT NULL,
  `new_line_coverage` double DEFAULT NULL,
  `lines` double DEFAULT NULL,
  `ncloc` double DEFAULT NULL,
  `ncloc_language_distribution` double DEFAULT NULL,
  `lines_to_cover` double DEFAULT NULL,
  `new_lines_to_cover` double DEFAULT NULL,
  `sqale_rating` double DEFAULT NULL,
  `new_maintainability_rating` double DEFAULT NULL,
  `major_violations` double DEFAULT NULL,
  `minor_violations` double DEFAULT NULL,
  `ncloc_data` double DEFAULT NULL,
  `new_blocker_violations` double DEFAULT NULL,
  `new_bugs` double DEFAULT NULL,
  `new_code_smells` double DEFAULT NULL,
  `new_critical_violations` double DEFAULT NULL,
  `new_info_violations` double DEFAULT NULL,
  `new_violations` double DEFAULT NULL,
  `new_lines` double DEFAULT NULL,
  `new_major_violations` double DEFAULT NULL,
  `new_minor_violations` double DEFAULT NULL,
  `new_security_hotspots` double DEFAULT NULL,
  `new_vulnerabilities` double DEFAULT NULL,
  `open_issues` double DEFAULT NULL,
  `quality_profiles` double DEFAULT NULL,
  `projects` double DEFAULT NULL,
  `public_api` double DEFAULT NULL,
  `public_documented_api_density` double DEFAULT NULL,
  `public_undocumented_api` double DEFAULT NULL,
  `quality_gate_details` double DEFAULT NULL,
  `alert_status` double DEFAULT NULL,
  `reliability_rating` double DEFAULT NULL,
  `new_reliability_rating` double DEFAULT NULL,
  `reliability_remediation_effort` double DEFAULT NULL,
  `new_reliability_remediation_effort` double DEFAULT NULL,
  `reopened_issues` double DEFAULT NULL,
  `security_hotspots` double DEFAULT NULL,
  `security_rating` double DEFAULT NULL,
  `new_security_rating` double DEFAULT NULL,
  `security_remediation_effort` double DEFAULT NULL,
  `new_security_remediation_effort` double DEFAULT NULL,
  `security_review_rating` double DEFAULT NULL,
  `skipped_tests` double DEFAULT NULL,
  `sonarjava_feedback` double DEFAULT NULL,
  `statements` double DEFAULT NULL,
  `team_size` double DEFAULT NULL,
  `sqale_index` double DEFAULT NULL,
  `sqale_debt_ratio` double DEFAULT NULL,
  `new_sqale_debt_ratio` double DEFAULT NULL,
  `uncovered_conditions` double DEFAULT NULL,
  `new_uncovered_conditions` double DEFAULT NULL,
  `uncovered_lines` double DEFAULT NULL,
  PRIMARY KEY (`timestamp`,`project_name`,`page`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vendor`
--

DROP TABLE IF EXISTS `vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor` (
  `timestamp` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `market` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `score` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `score_normalized` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `registration` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `registration_deviation` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `last_login` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `last_login_deviation` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sales` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `info` longtext COLLATE utf8_unicode_ci,
  `feedback` int(11) DEFAULT NULL,
  `pgp` varchar(5000) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`timestamp`,`market`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vendor-analysis`
--

DROP TABLE IF EXISTS `vendor-analysis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor-analysis` (
  `timestamp` varchar(255) DEFAULT NULL,
  `market` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `registration_date` varchar(255) DEFAULT NULL,
  `normalized_score` varchar(225) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone number` varchar(255) DEFAULT NULL,
  `wickr` varchar(255) DEFAULT NULL,
  `group/individual` varchar(255) DEFAULT NULL,
  `other markets` varchar(255) DEFAULT NULL,
  `ships_from` varchar(255) DEFAULT NULL,
  `ships_to` varchar(255) DEFAULT NULL,
  KEY `indexName` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-28 15:21:13
