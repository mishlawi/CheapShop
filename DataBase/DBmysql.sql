-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema cheapshop
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema cheapshop
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `cheapshop` DEFAULT CHARACTER SET utf8mb3 ;
USE `cheapshop` ;

-- -----------------------------------------------------
-- Table `cheapshop`.`superficie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cheapshop`.`superficie` (
  `Nome` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `IDsup` INT NOT NULL,
  `Website` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  PRIMARY KEY (`IDsup`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `cheapshop`.`item`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cheapshop`.`item` (
  `Nome` VARCHAR(200) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `IDitem` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `EAN` INT NOT NULL,
  `Marca` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL,
  `Quantidade` VARCHAR(45) NULL DEFAULT NULL,
  `PrecoPrim` VARCHAR(45) NULL DEFAULT NULL,
  `PrecoUni` VARCHAR(45) NULL DEFAULT NULL,
  `Promo` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL,
  `superficie_IDsup` INT NOT NULL,
  PRIMARY KEY (`IDitem`),
  INDEX `fk_item_superficie1_idx` (`superficie_IDsup` ASC) VISIBLE,
  CONSTRAINT `fk_item_superficie1`
    FOREIGN KEY (`superficie_IDsup`)
    REFERENCES `cheapshop`.`superficie` (`IDsup`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `cheapshop`.`historicopreco`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cheapshop`.`historicopreco` (
  `Preco` DOUBLE NOT NULL,
  `Data` DATETIME NOT NULL,
  `item_IDitem` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  PRIMARY KEY (`Preco`),
  INDEX `fk_historicopreco_item1_idx` (`item_IDitem` ASC) VISIBLE,
  CONSTRAINT `fk_historicopreco_item1`
    FOREIGN KEY (`item_IDitem`)
    REFERENCES `cheapshop`.`item` (`IDitem`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
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
  `item_IDitem` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NOT NULL,
  `user_EmailUser` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idLista`),
  INDEX `fk_lista_item1_idx` (`item_IDitem` ASC) VISIBLE,
  INDEX `fk_lista_user1_idx` (`user_EmailUser` ASC) VISIBLE,
  CONSTRAINT `fk_lista_item1`
    FOREIGN KEY (`item_IDitem`)
    REFERENCES `cheapshop`.`item` (`IDitem`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_lista_user1`
    FOREIGN KEY (`user_EmailUser`)
    REFERENCES `cheapshop`.`user` (`EmailUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
