-- phpMyAdmin SQL Dump
-- version 3.2.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 26, 2023 at 11:55 PM
-- Server version: 5.1.41
-- PHP Version: 5.3.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `heartdisease`
--
CREATE DATABASE `heartdisease` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `heartdisease`;

-- --------------------------------------------------------

--
-- Table structure for table `doctordetails`
--

CREATE TABLE IF NOT EXISTS `doctordetails` (
  `DoctorId` int(11) NOT NULL AUTO_INCREMENT,
  `Firstname` varchar(250) NOT NULL,
  `Lastname` varchar(250) NOT NULL,
  `Phoneno` bigint(250) NOT NULL,
  `Emailid` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `Username` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`DoctorId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `doctordetails`
--

INSERT INTO `doctordetails` (`DoctorId`, `Firstname`, `Lastname`, `Phoneno`, `Emailid`, `Address`, `Username`, `Password`, `Recorded_Date`) VALUES
(1, 'kiruba', 's', 9043963074, 'kirubakarans2009@gmail.com', 'kiruba', 'kiruba', 'kiruba', '2023-03-15');

-- --------------------------------------------------------

--
-- Table structure for table `healthdetails`
--

CREATE TABLE IF NOT EXISTS `healthdetails` (
  `HealthId` int(11) NOT NULL AUTO_INCREMENT,
  `PersonId` int(11) NOT NULL,
  `Age` int(11) NOT NULL,
  `Sex` int(11) NOT NULL,
  `CP` int(11) NOT NULL,
  `Trestbps` int(11) NOT NULL,
  `Cholestrol` int(11) NOT NULL,
  `Fbs` int(11) NOT NULL,
  `Restecg` int(11) NOT NULL,
  `Thalach` int(11) NOT NULL,
  `Exang` int(11) NOT NULL,
  `OldPeak` float NOT NULL,
  `Slope` int(11) NOT NULL,
  `CA` int(11) NOT NULL,
  `Thal` int(11) NOT NULL,
  `Result` varchar(250) DEFAULT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`HealthId`),
  KEY `PersonId` (`PersonId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=12 ;

--
-- Dumping data for table `healthdetails`
--

INSERT INTO `healthdetails` (`HealthId`, `PersonId`, `Age`, `Sex`, `CP`, `Trestbps`, `Cholestrol`, `Fbs`, `Restecg`, `Thalach`, `Exang`, `OldPeak`, `Slope`, `CA`, `Thal`, `Result`, `Recorded_Date`) VALUES
(3, 6, 63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1, 'Yes', '2023-04-26'),
(4, 6, 63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1, 'Yes', '2023-04-26'),
(5, 6, 63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1, 'Yes', '2023-04-26'),
(8, 6, 67, 1, 0, 160, 286, 0, 0, 108, 1, 1.5, 1, 3, 2, 'No', '2023-04-26'),
(9, 6, 63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1, 'Yes', '2023-04-26'),
(10, 6, 67, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1, 'Yes', '2023-04-26'),
(11, 6, 34, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1, 'Yes', '2023-04-26');

-- --------------------------------------------------------

--
-- Table structure for table `personaldetails`
--

CREATE TABLE IF NOT EXISTS `personaldetails` (
  `PersonId` int(11) NOT NULL AUTO_INCREMENT,
  `Firstname` varchar(250) NOT NULL,
  `Lastname` varchar(250) NOT NULL,
  `Phoneno` bigint(250) NOT NULL,
  `Emailid` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `Username` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`PersonId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `personaldetails`
--

INSERT INTO `personaldetails` (`PersonId`, `Firstname`, `Lastname`, `Phoneno`, `Emailid`, `Address`, `Username`, `Password`, `Recorded_Date`) VALUES
(6, 'kiruba', 's', 9043963074, 'kirubakarans2009@gmail.com', 'No:10,Chinna Ponnu Nagar,\r\nS.N.Chavady, Cuddalore-607002.', 'kiruba', 'kiruba', '2021-04-26');

-- --------------------------------------------------------

--
-- Table structure for table `querydetails`
--

CREATE TABLE IF NOT EXISTS `querydetails` (
  `QueryId` int(11) NOT NULL AUTO_INCREMENT,
  `PersonId` int(11) NOT NULL,
  `DoctorId` int(11) NOT NULL,
  `Comments` varchar(250) NOT NULL,
  `Reply` varchar(250) DEFAULT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`QueryId`),
  KEY `PersonId` (`PersonId`,`DoctorId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10 ;

--
-- Dumping data for table `querydetails`
--

INSERT INTO `querydetails` (`QueryId`, `PersonId`, `DoctorId`, `Comments`, `Reply`, `Recorded_Date`) VALUES
(6, 6, 1, 'How to come out of of this problem?', 'Travel to some natural destination.', '2023-04-01'),
(7, 6, 1, 'dsdfs', 'zXssas', '2023-04-01'),
(8, 6, 1, 'ffdsfdssdf', '-', '2023-04-26'),
(9, 6, 1, 'Kindly suggest the solution for this one.', 'Kindly walk by morning and evening.', '2023-04-26');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `healthdetails`
--
ALTER TABLE `healthdetails`
  ADD CONSTRAINT `healthdetails_ibfk_1` FOREIGN KEY (`PersonId`) REFERENCES `personaldetails` (`PersonId`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
