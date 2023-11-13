-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-11-2023 a las 01:31:17
-- Versión del servidor: 10.4.20-MariaDB
-- Versión de PHP: 8.0.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `mcbd`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ad`
--

CREATE TABLE `ad` (
  `id` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `precio` varchar(45) NOT NULL,
  `foto` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carros`
--

CREATE TABLE `carros` (
  `id` int(11) NOT NULL,
  `marca` varchar(45) NOT NULL,
  `modelo` varchar(45) NOT NULL,
  `year` varchar(45) NOT NULL,
  `color` varchar(45) NOT NULL,
  `puertas` varchar(45) NOT NULL,
  `favorito` varchar(45) NOT NULL,
  `foto` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `carros`
--

INSERT INTO `carros` (`id`, `marca`, `modelo`, `year`, `color`, `puertas`, `favorito`, `foto`) VALUES
(1, 'BMW', 'BMW X7', '2022', 'Gris', '4', 'Si', 'bmw_2022.jpg'),
(2, 'Ford', 'CAMIONETA', '2022', 'Blanco', '4', 'Si', 'ford_camioneta_2020.webp'),
(3, 'Chevrolet', 'Onix Turbo', '2013', 'Blanco', '2', 'No', 'chevrolet.webp'),
(7, 'Toyota', 'Avalon', '2018', 'Gris', '2', 'No', 'toyota_corolla.webp'),
(8, 'Chevrolet', 'Joy HB', '2015', 'Rojo', '4', 'Si', ''),
(10, 'Mercedes-Benz', 'CLA Coupé', '2022', 'Blanco', '4', 'Si', 'CLA_Coupe.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `content`
--

CREATE TABLE `content` (
  `id` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `foto` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `subs`
--

CREATE TABLE `subs` (
  `id` int(11) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `edad` varchar(45) NOT NULL,
  `foto` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `userid` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`userid`, `name`, `email`, `password`) VALUES
(7, 'admin', 'admin@gmail.com', 'admin1');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `ad`
--
ALTER TABLE `ad`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `carros`
--
ALTER TABLE `carros`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `content`
--
ALTER TABLE `content`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `subs`
--
ALTER TABLE `subs`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userid`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `ad`
--
ALTER TABLE `ad`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `carros`
--
ALTER TABLE `carros`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `content`
--
ALTER TABLE `content`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `subs`
--
ALTER TABLE `subs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `userid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
