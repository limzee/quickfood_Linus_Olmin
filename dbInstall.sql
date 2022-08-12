-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Värd: localhost:8889
-- Tid vid skapande: 12 aug 2022 kl 17:52
-- Serverversion: 5.7.34
-- PHP-version: 7.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Databas: `quickfood`
--

CREATE DATABASE quickfood;
USE quickfood;

-- --------------------------------------------------------

--
-- Tabellstruktur `customer`
--

CREATE TABLE `customer` (
  `id` int(2) NOT NULL,
  `first_name` varchar(10) DEFAULT NULL,
  `last_name` varchar(9) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumpning av Data i tabell `customer`
--

INSERT INTO `customer` (`id`, `first_name`, `last_name`) VALUES
(1, 'Linus', 'Olmin');

-- --------------------------------------------------------

--
-- Ersättningsstruktur för vy `customer_sum`
-- (See below for the actual view)
--
CREATE TABLE `customer_sum` (
`id` varchar(11)
,`first_name` varchar(10)
,`last_name` varchar(9)
,`orders_sum` double
);

-- --------------------------------------------------------

--
-- Tabellstruktur `food`
--

CREATE TABLE `food` (
  `id` int(2) NOT NULL,
  `name` varchar(13) DEFAULT NULL,
  `price` varchar(5) DEFAULT NULL,
  `deleted` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumpning av Data i tabell `food`
--

INSERT INTO `food` (`id`, `name`, `price`, `deleted`) VALUES
(1, 'frie', '25', 0),
(2, 'kebab', '79', 0),
(3, 'pancakes', '82', 0);

-- --------------------------------------------------------

--
-- Tabellstruktur `food_tag`
--

CREATE TABLE `food_tag` (
  `id` int(2) NOT NULL,
  `tag_id` varchar(6) DEFAULT NULL,
  `food_id` varchar(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumpning av Data i tabell `food_tag`
--

INSERT INTO `food_tag` (`id`, `tag_id`, `food_id`) VALUES
(2, '2', '3');

-- --------------------------------------------------------

--
-- Tabellstruktur `orders`
--

CREATE TABLE `orders` (
  `id` int(2) NOT NULL,
  `food_id` varchar(7) DEFAULT NULL,
  `customer_id` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumpning av Data i tabell `orders`
--

INSERT INTO `orders` (`id`, `food_id`, `customer_id`) VALUES
(1, '2', '1'),
(2, '1', '1');

-- --------------------------------------------------------

--
-- Tabellstruktur `tag_type`
--

CREATE TABLE `tag_type` (
  `id` int(2) NOT NULL,
  `name` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumpning av Data i tabell `tag_type`
--

INSERT INTO `tag_type` (`id`, `name`) VALUES
(2, 'gluten free');

-- --------------------------------------------------------

--
-- Struktur för vy `customer_sum`
--
DROP TABLE IF EXISTS `customer_sum`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `customer_sum`  AS SELECT `o`.`customer_id` AS `id`, `c`.`first_name` AS `first_name`, `c`.`last_name` AS `last_name`, sum(`f`.`price`) AS `orders_sum` FROM ((`orders` `o` join `food` `f` on((`f`.`id` = `o`.`food_id`))) join `customer` `c` on((`c`.`id` = `o`.`customer_id`))) GROUP BY `o`.`customer_id` ;

--
-- Index för dumpade tabeller
--

--
-- Index för tabell `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`);

--
-- Index för tabell `food`
--
ALTER TABLE `food`
  ADD PRIMARY KEY (`id`);

--
-- Index för tabell `food_tag`
--
ALTER TABLE `food_tag`
  ADD PRIMARY KEY (`id`);

--
-- Index för tabell `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Index för tabell `tag_type`
--
ALTER TABLE `tag_type`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT för dumpade tabeller
--

--
-- AUTO_INCREMENT för tabell `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT för tabell `food`
--
ALTER TABLE `food`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT för tabell `food_tag`
--
ALTER TABLE `food_tag`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT för tabell `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT för tabell `tag_type`
--
ALTER TABLE `tag_type`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
