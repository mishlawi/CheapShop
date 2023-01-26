-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema cheapshop
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema cheapshop
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `cheapshop` DEFAULT CHARACTER SET utf8 ;
USE `cheapshop` ;

-- -----------------------------------------------------
-- Table `cheapshop`.`superficie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cheapshop`.`superficie` (
  `Nome` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `IDsup` VARCHAR(5) NOT NULL,
  `Website` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  PRIMARY KEY (`IDsup`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `cheapshop`.`item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cheapshop`.`item` (
  `Nome` VARCHAR(200) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `EAN` VARCHAR(100) NOT NULL,
  `Marca` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL,
  `Quantidade` VARCHAR(45) NULL DEFAULT NULL,
  `PrecoPrim` VARCHAR(45) NULL DEFAULT NULL,
  `PrecoUni` VARCHAR(45) NULL DEFAULT NULL,
  `Promo` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL,
  `LinkImagem` VARCHAR(300) NULL DEFAULT NULL,
  `LinkProduto` VARCHAR(300) NULL DEFAULT NULL,
  `superficie_IDsup` VARCHAR(5) NOT NULL,
  PRIMARY KEY (`EAN`, `superficie_IDsup`),
  INDEX `fk_item_superficie1_idx` (`superficie_IDsup` ASC) VISIBLE,
  CONSTRAINT `fk_item_superficie1`
    FOREIGN KEY (`superficie_IDsup`)
    REFERENCES `cheapshop`.`superficie` (`IDsup`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `cheapshop`.`historicopreco`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cheapshop`.`historicopreco` (
  `Preco` DOUBLE NOT NULL,
  `Data` DATETIME NOT NULL,
  `item_EAN` VARCHAR(100) NOT NULL,
  `item_superficie_IDsup` VARCHAR(5) NOT NULL,
  PRIMARY KEY (`Preco`),
  INDEX `fk_historicopreco_item1_idx` (`item_EAN` ASC, `item_superficie_IDsup` ASC) VISIBLE,
  CONSTRAINT `fk_historicopreco_item1`
    FOREIGN KEY (`item_EAN` , `item_superficie_IDsup`)
    REFERENCES `cheapshop`.`item` (`EAN` , `superficie_IDsup`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `cheapshop`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cheapshop`.`user` (
  `EmailUser` VARCHAR(100) NOT NULL,
  `Nome` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `Pass` VARCHAR(100) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `Morada` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  PRIMARY KEY (`EmailUser`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `cheapshop`.`lista`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cheapshop`.`lista` (
  `Quantidade` INT NOT NULL,
  `idLista` INT NOT NULL,
  `user_EmailUser` VARCHAR(100) NOT NULL,
  `item_EAN` VARCHAR(100) NOT NULL,
  `item_superficie_IDsup` VARCHAR(5) NOT NULL,
  PRIMARY KEY (`idLista`),
  INDEX `fk_lista_user1_idx` (`user_EmailUser` ASC) VISIBLE,
  INDEX `fk_lista_item1_idx` (`item_EAN` ASC, `item_superficie_IDsup` ASC) VISIBLE,
  CONSTRAINT `fk_lista_item1`
    FOREIGN KEY (`item_EAN` , `item_superficie_IDsup`)
    REFERENCES `cheapshop`.`item` (`EAN` , `superficie_IDsup`),
  CONSTRAINT `fk_lista_user1`
    FOREIGN KEY (`user_EmailUser`)
    REFERENCES `cheapshop`.`user` (`EmailUser`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

INSERT INTO cheapshop.superficie (Nome, IDsup, Website) values('Froiz', 'FRO', 'https://www.froiz.pt');
INSERT INTO cheapshop.superficie (Nome, IDsup, Website) values('Auchan', 'AUC', 'https://www.auchan.pt');
INSERT INTO cheapshop.superficie (Nome, IDsup, Website) values('InterMarche', 'INM', 'https://www.intermarche.pt');
INSERT INTO cheapshop.superficie (Nome, IDsup, Website) values('Continente', 'CON', 'https://www.continente.pt');
INSERT INTO cheapshop.superficie (Nome, IDsup, Website) values('Pingo Doce', 'PDC', 'https://www.pingodoce.pt');
INSERT INTO cheapshop.superficie (Nome, IDsup, Website) values('ElCorte Ingles', 'ECI', 'https://www.elcorteingles.pt');
INSERT INTO cheapshop.superficie (Nome, IDsup, Website) values('Eleclerc', 'ELE', 'https://e-leclerc.pt');

