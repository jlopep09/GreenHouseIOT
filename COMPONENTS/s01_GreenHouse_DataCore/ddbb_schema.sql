-- --------------------------------------------------------
-- Host:                         localhost
-- Versión del servidor:         11.7.2-MariaDB-ubu2404 - mariadb.org binary distribution
-- SO del servidor:              debian-linux-gnu
-- HeidiSQL Versión:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para db_greenhouse
CREATE DATABASE IF NOT EXISTS `db_greenhouse` /*!40100 DEFAULT CHARACTER SET utf8mb3 COLLATE utf8mb3_uca1400_spanish_ai_ci */;
USE `db_greenhouse`;

-- Volcando estructura para tabla db_greenhouse.greenhouses
CREATE TABLE IF NOT EXISTS `greenhouses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT 'Last updated date',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NOT NULL DEFAULT '',
  `description` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci DEFAULT '',
  `image` mediumblob DEFAULT NULL,
  `ip` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NOT NULL DEFAULT '0.0.0.0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_spanish_ai_cs;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla db_greenhouse.images
CREATE TABLE IF NOT EXISTS `images` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `image` mediumblob NOT NULL,
  `label` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_spanish_ai_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla db_greenhouse.sensor_reads
CREATE TABLE IF NOT EXISTS `sensor_reads` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `tds` int(10) unsigned DEFAULT NULL,
  `humidity` int(10) unsigned DEFAULT NULL,
  `water_level` int(10) unsigned DEFAULT NULL,
  `temperature` int(10) unsigned DEFAULT NULL,
  `light_level` set('True','False') DEFAULT NULL,
  `water_temperature` float DEFAULT NULL,
  `date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `gh_id` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `gh_id` (`gh_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1506 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- La exportación de datos fue deseleccionada.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
