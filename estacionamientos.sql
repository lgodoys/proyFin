SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `estacionamientos` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `estacionamientos`;

CREATE TABLE IF NOT EXISTS `cobros` (
  `idcobros` int NOT NULL AUTO_INCREMENT,
  `hora_entrada` bigint NOT NULL,
  `hora_salida` bigint DEFAULT NULL,
  `valor` int DEFAULT NULL,
  `vehiculos_idvehiculos` varchar(6) NOT NULL,
  `espacios_idespacios` int NOT NULL,
  PRIMARY KEY (`idcobros`),
  KEY `vehiculos_idvehiculos` (`vehiculos_idvehiculos`),
  KEY `espacios_idespacios` (`espacios_idespacios`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `dueños` (
  `rut` varchar(11) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `apellido` varchar(30) NOT NULL,
  `vehiculos_idvehiculos` varchar(6) NOT NULL,
  PRIMARY KEY (`rut`),
  KEY `vehiculos_idvehiculos` (`vehiculos_idvehiculos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `edificios` (
  `idedificios` varchar(6) NOT NULL,
  `direccion` varchar(250) NOT NULL,
  `contacto` varchar(250) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  PRIMARY KEY (`idedificios`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `espacios` (
  `idespacios` int NOT NULL,
  `edificios_idedificios` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `vehiculos_idvehiculos` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`idespacios`),
  KEY `edificios_idedificios` (`edificios_idedificios`),
  KEY `vehiculos_idvehiculos` (`vehiculos_idvehiculos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `vehiculos` (
  `idvehiculos` varchar(6) NOT NULL,
  `placa` varchar(6) NOT NULL,
  PRIMARY KEY (`idvehiculos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


ALTER TABLE `cobros`
  ADD CONSTRAINT `cobros_ibfk_1` FOREIGN KEY (`vehiculos_idvehiculos`) REFERENCES `vehiculos` (`idvehiculos`),
  ADD CONSTRAINT `cobros_ibfk_2` FOREIGN KEY (`espacios_idespacios`) REFERENCES `espacios` (`idespacios`);

ALTER TABLE `dueños`
  ADD CONSTRAINT `dueños_ibfk_1` FOREIGN KEY (`vehiculos_idvehiculos`) REFERENCES `vehiculos` (`idvehiculos`);

ALTER TABLE `espacios`
  ADD CONSTRAINT `espacios_ibfk_1` FOREIGN KEY (`edificios_idedificios`) REFERENCES `edificios` (`idedificios`),
  ADD CONSTRAINT `espacios_ibfk_2` FOREIGN KEY (`vehiculos_idvehiculos`) REFERENCES `vehiculos` (`idvehiculos`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
