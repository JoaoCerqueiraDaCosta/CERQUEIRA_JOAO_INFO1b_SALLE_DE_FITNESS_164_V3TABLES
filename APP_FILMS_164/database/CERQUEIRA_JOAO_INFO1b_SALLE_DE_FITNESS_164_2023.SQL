DROP DATABASE IF EXISTS `fit`;

-- Listage de la structure de la base pour fit
CREATE DATABASE IF NOT EXISTS `fit`;
USE `fit`;

-- Listage de la structure de table fit. t_avoir_coach
CREATE TABLE IF NOT EXISTS `t_membres_avoir_coach` (
  `ID_membres_avoir_coach` int NOT NULL AUTO_INCREMENT,
  `fk_membres` int DEFAULT NULL,
  `fk_coach` int DEFAULT NULL,
  PRIMARY KEY (`ID_membres_avoir_coach`),
  KEY `Index 2` (`fk_coach`,`fk_membres`),
  KEY `FK_t_avoir_coach_t_membres` (`fk_membres`),
  CONSTRAINT `FK_t_avoir_coach_t_coach` FOREIGN KEY (`fk_coach`) REFERENCES `t_coach` (`ID_coach`),
  CONSTRAINT `FK_t_avoir_coach_t_membres` FOREIGN KEY (`fk_membres`) REFERENCES `t_membres` (`id_membres`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table fit.t_avoir_coach : ~4 rows (environ)
INSERT INTO `t_membres_avoir_coach` (`ID_membres_avoir_coach`, `fk_membres`, `fk_coach`) VALUES
	(2, 4, 1),
	(3, 2, 2),
	(1, 5, 3),
	(4, 7, 3);

-- Listage de la structure de table fit. t_coach
CREATE TABLE IF NOT EXISTS `t_coach` (
  `ID_coach` int NOT NULL AUTO_INCREMENT,
  `prenom` varchar(50) DEFAULT NULL,
  `nom` varchar(50) DEFAULT NULL,
  `Specialiter_coach` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`ID_coach`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table fit.t_coach : ~3 rows (environ)
INSERT INTO `t_coach` (`ID_coach`, `prenom`, `nom`,`Specialiter_coach`) VALUES
	(1, 'Jean', 'Dupont','endurance'),
	(2, 'Marie', 'Martin', 'Haut du corps'),
	(3, 'Luc', 'Dubois', 'Bas du corps');

-- Listage de la structure de table fit. t_equipements
CREATE TABLE IF NOT EXISTS `t_equipements` (
  `id_equipements` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `date_achat` date DEFAULT NULL,
  `date_reparation` date DEFAULT NULL,
  `disponible` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id_equipements`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table fit.t_equipements : ~10 rows (environ)
INSERT INTO `t_equipements` (`id_equipements`, `nom`, `type`, `date_achat`, `date_reparation`, `disponible`) VALUES
	(1, 'Tapis de course', 'Cardio', '2020-01-01', '2025-01-01', 1),
	(2, 'Vélo elliptique', 'Cardio', '2019-07-15', '2024-07-15', 1),
	(3, 'Rameur', 'Cardio', '2021-04-20', '2026-04-20', 1),
	(4, 'Haltères', 'Musculation', '2018-12-10', '2023-12-10', 1),
	(5, 'Banc de musculation', 'Musculation', '2019-09-01', '2024-09-01', 1),
	(6, 'Machine à abdominaux', 'Musculation', '2020-03-05', '2025-03-05', 1),
	(7, 'Poulie haute', 'Musculation', '2021-02-10', '2026-02-10', 1),
	(8, 'Balle de stabilité', 'Accessoire', '2019-11-23', '2024-11-23', 1),
	(9, 'Corde à sauter', 'Accessoire', '2020-07-12', '2025-07-12', 1),
	(10, 'Yoga mat', 'Accessoire', '2021-03-30', '2026-03-30', 1);

-- Listage de la structure de table fit. t_membres
CREATE TABLE IF NOT EXISTS `t_membres` (
  `id_membres` int NOT NULL AUTO_INCREMENT,
  `prenom` varchar(50) DEFAULT NULL,
  `nom` varchar(50) DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `date_inscription` date DEFAULT NULL,
  `actif` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id_membres`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table fit.t_membres : ~10 rows (environ)
INSERT INTO `t_membres` (`id_membres`, `prenom`, `nom`, `date_naissance`, `email`, `telephone`, `date_inscription`, `actif`) VALUES
	(1, 'Jean', 'Dupont', '1990-05-12', 'jean.dupont@mail.com', '+41 79 123 45 67', '2021-01-01', 1),
	(2, 'Marie', 'Martin', '1995-02-20', 'marie.martin@mail.com', '+41 78 987 65 43', '2020-03-15', 1),
	(3, 'Luc', 'Dubois', '1985-11-07', 'luc.dubois@mail.com', '+41 79 246 80 12', '2022-02-14', 1),
	(4, 'Emma', 'Lefevre', '2000-08-15', 'emma.lefevre@mail.com', '+41 76 345 67 89', '2021-09-30', 1),
	(5, 'Antoine', 'Roux', '1992-04-30', 'antoine.roux@mail.com', '+41 78 901 23 45', '2020-10-12', 1),
	(6, 'Pauline', 'Garcia', '1998-01-02', 'pauline.garcia@mail.com', '+41 79 678 90 12', '2021-05-05', 1),
	(7, 'Thomas', 'Andre', '1994-12-24', 'thomas.andre@mail.com', '+41 76 234 56 78', '2022-03-03', 1),
	(8, 'Charlotte', 'Pierre', '1996-09-11', 'charlotte.pierre@mail.com', '+41 79 890 12 34', '2021-07-07', 1),
	(9, 'Nicolas', 'Berger', '1988-06-08', 'nicolas.berger@mail.com', '+41 78 345 67 89', '2020-12-23', 1),
	(10, 'Julie', 'Rousseau', '1991-03-25', 'julie.rousseau@mail.com', '+41 76 901 23 45', '2022-01-10', 1);

-- Listage de la structure de table fit. t_salle_de_fitness
CREATE TABLE IF NOT EXISTS `t_salle_de_fitness` (
  `id_salle_de_fitness` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(50) DEFAULT NULL,
  `adresse` varchar(100) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `capacite_max` int DEFAULT NULL,
  PRIMARY KEY (`id_salle_de_fitness`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table fit.t_salle_de_fitness : ~1 rows (environ)
INSERT INTO `t_salle_de_fitness` (`id_salle_de_fitness`, `nom`, `adresse`, `telephone`, `email`, `capacite_max`) VALUES
	(1, 'FitForm', '15 rue des Sports, 75001 Paris', '0144556677', 'contact@fitform.com', 50);
