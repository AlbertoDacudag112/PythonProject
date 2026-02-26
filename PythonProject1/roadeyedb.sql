-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 26, 2026 at 03:15 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `roadeyedb`
--

-- --------------------------------------------------------

--
-- Table structure for table `activity_logs`
--

CREATE TABLE `activity_logs` (
  `LogID` int(11) NOT NULL,
  `UserID` varchar(5) NOT NULL,
  `Action` varchar(255) NOT NULL,
  `TableAffected` varchar(50) DEFAULT NULL,
  `RecordID` varchar(10) DEFAULT NULL,
  `ActionDate` datetime DEFAULT current_timestamp(),
  `IPAddress` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `activity_logs`
--

INSERT INTO `activity_logs` (`LogID`, `UserID`, `Action`, `TableAffected`, `RecordID`, `ActionDate`, `IPAddress`) VALUES
(1, 'U001', 'Created violation type', 'violation_types', 'VT01', '2025-12-01 08:00:00', NULL),
(2, 'U002', 'Processed violation', 'violations', 'VI001', '2025-12-01 09:00:00', NULL),
(3, 'U003', 'Verified payment', 'payments', 'P001', '2025-12-02 09:15:00', NULL),
(4, 'U001', 'Registered vehicle', 'vehicles', 'V001', '2025-11-30 10:00:00', NULL),
(5, 'U001', 'Admin login: admin1', NULL, NULL, '2025-12-17 12:38:13', NULL),
(6, 'U001', 'Admin logout: admin1', NULL, NULL, '2025-12-17 12:38:43', NULL),
(7, 'U004', 'User login: john.doe', NULL, NULL, '2025-12-17 12:39:06', NULL),
(8, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 14:47:53', NULL),
(9, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 14:52:22', NULL),
(10, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 15:26:10', NULL),
(11, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 15:29:48', NULL),
(12, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 15:36:08', NULL),
(13, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 15:52:14', NULL),
(14, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 15:54:31', NULL),
(15, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 15:55:16', NULL),
(16, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 15:56:07', NULL),
(17, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 15:56:25', NULL),
(18, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 15:57:38', NULL),
(19, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 16:01:00', NULL),
(20, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 16:31:37', NULL),
(21, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 16:33:34', NULL),
(22, 'U024', 'User login: alberto', NULL, NULL, '2026-01-23 16:34:43', NULL),
(23, 'U024', 'User logout: alberto', NULL, NULL, '2026-01-23 16:37:25', NULL),
(24, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-23 16:37:31', NULL),
(25, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-23 16:38:00', NULL),
(26, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-23 18:28:56', NULL),
(27, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-23 18:33:00', NULL),
(28, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-23 18:33:27', NULL),
(29, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-23 18:35:59', NULL),
(30, 'U024', 'User login: alberto', NULL, NULL, '2026-01-27 02:49:46', NULL),
(31, 'U024', 'User logout: alberto', NULL, NULL, '2026-01-27 02:50:01', NULL),
(32, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 02:50:05', NULL),
(33, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-01-27 02:50:11', NULL),
(34, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 02:50:14', NULL),
(35, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 02:51:18', NULL),
(36, 'U024', 'User login: alberto', NULL, NULL, '2026-01-27 02:55:18', NULL),
(37, 'U024', 'User login: alberto', NULL, NULL, '2026-01-27 02:55:53', NULL),
(38, 'U024', 'User login: alberto', NULL, NULL, '2026-01-27 03:07:18', NULL),
(39, 'U024', 'User login: alberto', NULL, NULL, '2026-01-27 03:08:58', NULL),
(40, 'U024', 'User login: alberto', NULL, NULL, '2026-01-27 03:09:47', NULL),
(41, 'U024', 'User login: alberto', NULL, NULL, '2026-01-27 03:11:55', NULL),
(42, 'U024', 'User login: alberto', NULL, NULL, '2026-01-27 03:13:33', NULL),
(43, 'U024', 'User login: alberto', NULL, NULL, '2026-01-27 03:20:14', NULL),
(44, 'U024', 'User logout: alberto', NULL, NULL, '2026-01-27 03:20:28', NULL),
(45, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 03:20:33', NULL),
(46, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-01-27 03:22:20', NULL),
(47, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 03:22:42', NULL),
(48, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 03:24:20', NULL),
(49, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 03:39:03', NULL),
(50, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 03:39:24', NULL),
(51, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 03:39:42', NULL),
(52, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 03:44:29', NULL),
(53, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 03:44:57', NULL),
(54, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 03:46:46', NULL),
(55, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-01-27 03:47:40', NULL),
(56, 'U024', 'User login: alberto', NULL, NULL, '2026-01-27 03:47:47', NULL),
(57, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 03:48:15', NULL),
(58, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 04:08:27', NULL),
(59, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-01-27 04:08:37', NULL),
(60, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-27 04:13:48', NULL),
(61, 'U027', 'User logout: qwerty', NULL, NULL, '2026-01-27 04:13:56', NULL),
(62, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 04:14:00', NULL),
(63, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-01-27 04:14:41', NULL),
(64, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-27 04:14:46', NULL),
(65, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-27 04:18:40', NULL),
(66, 'U027', 'User logout: qwerty', NULL, NULL, '2026-01-27 04:19:25', NULL),
(67, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 04:19:29', NULL),
(68, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 04:23:25', NULL),
(69, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 04:23:55', NULL),
(70, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 04:24:31', NULL),
(71, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 14:32:09', NULL),
(72, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-01-27 14:32:43', NULL),
(73, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 14:32:59', NULL),
(74, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 14:34:49', NULL),
(75, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 14:37:06', NULL),
(76, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 14:37:34', NULL),
(77, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 14:37:46', NULL),
(78, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 14:38:16', NULL),
(79, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 14:39:54', NULL),
(80, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 14:40:39', NULL),
(81, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 14:44:45', NULL),
(82, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 14:45:55', NULL),
(83, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 14:47:52', NULL),
(84, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-27 14:50:29', NULL),
(85, 'U027', 'User logout: qwerty', NULL, NULL, '2026-01-27 14:52:23', NULL),
(86, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-27 14:52:26', NULL),
(87, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-01-27 14:53:05', NULL),
(88, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-27 14:53:10', NULL),
(89, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-27 14:54:35', NULL),
(90, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-27 15:08:03', NULL),
(91, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-27 15:13:07', NULL),
(92, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-27 15:15:04', NULL),
(93, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-27 15:15:32', NULL),
(94, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-27 15:17:53', NULL),
(95, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:05:53', NULL),
(96, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:07:09', NULL),
(97, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:10:02', NULL),
(98, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:13:01', NULL),
(99, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:15:06', NULL),
(100, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:17:00', NULL),
(101, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:17:31', NULL),
(102, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:18:51', NULL),
(103, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:19:33', NULL),
(104, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:22:34', NULL),
(105, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:25:03', NULL),
(106, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:26:12', NULL),
(107, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:26:31', NULL),
(108, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:27:30', NULL),
(109, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:28:04', NULL),
(110, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:28:52', NULL),
(111, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:32:15', NULL),
(112, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:33:00', NULL),
(113, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:37:10', NULL),
(114, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:46:44', NULL),
(115, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:47:21', NULL),
(116, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:47:37', NULL),
(117, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:51:50', NULL),
(118, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:52:18', NULL),
(119, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:52:30', NULL),
(120, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:52:47', NULL),
(121, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:54:05', NULL),
(122, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:55:10', NULL),
(123, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 05:56:51', NULL),
(124, 'U027', 'User logout: qwerty', NULL, NULL, '2026-01-28 12:01:45', NULL),
(125, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-28 12:01:51', NULL),
(126, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-28 14:28:33', NULL),
(127, 'U001', 'Admin login: admin1', NULL, NULL, '2026-01-28 14:32:38', NULL),
(128, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-01-28 14:35:17', NULL),
(129, 'U027', 'User login: qwerty', NULL, NULL, '2026-01-28 14:35:23', NULL),
(130, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 12:19:36', NULL),
(131, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 12:33:29', NULL),
(132, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 12:34:07', NULL),
(133, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 12:37:21', NULL),
(134, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 12:47:17', NULL),
(135, 'U027', 'User login: QWERTY', NULL, NULL, '2026-02-03 12:52:09', NULL),
(136, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 12:53:38', NULL),
(137, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 12:54:08', NULL),
(138, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 12:54:45', NULL),
(139, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 12:55:02', NULL),
(140, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 12:55:56', NULL),
(141, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 13:07:07', NULL),
(142, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 13:18:25', NULL),
(143, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 13:19:33', NULL),
(144, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 13:19:56', NULL),
(145, 'U027', 'User logout: qwerty', NULL, NULL, '2026-02-03 13:22:05', NULL),
(146, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 13:22:11', NULL),
(147, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 13:29:42', NULL),
(148, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 13:31:45', NULL),
(149, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-02-03 13:33:04', NULL),
(150, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 13:33:08', NULL),
(151, 'U027', 'User logout: qwerty', NULL, NULL, '2026-02-03 13:33:13', NULL),
(152, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 13:33:59', NULL),
(153, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 13:36:38', NULL),
(154, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 13:37:20', NULL),
(155, 'U027', 'User logout: qwerty', NULL, NULL, '2026-02-03 13:37:49', NULL),
(156, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 13:37:55', NULL),
(157, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 13:40:05', NULL),
(158, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 13:40:24', NULL),
(159, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 13:42:46', NULL),
(160, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 22:05:51', NULL),
(161, 'U027', 'User logout: qwerty', NULL, NULL, '2026-02-03 22:06:46', NULL),
(162, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 22:06:53', NULL),
(163, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 22:17:10', NULL),
(164, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 22:17:30', NULL),
(165, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 22:21:15', NULL),
(166, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 22:22:30', NULL),
(167, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-02-03 22:22:38', NULL),
(168, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 22:22:43', NULL),
(169, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 22:23:11', NULL),
(170, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 22:23:53', NULL),
(171, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 22:37:06', NULL),
(172, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 22:40:55', NULL),
(173, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 22:42:28', NULL),
(174, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 22:43:36', NULL),
(175, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-03 22:45:02', NULL),
(176, 'U027', 'User logout: qwerty', NULL, NULL, '2026-02-03 22:45:06', NULL),
(177, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-03 22:45:09', NULL),
(178, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 06:21:00', NULL),
(179, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 06:25:17', NULL),
(180, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 06:30:11', NULL),
(181, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 06:30:42', NULL),
(182, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 06:35:10', NULL),
(183, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 06:50:07', NULL),
(184, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 06:56:58', NULL),
(185, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 10:01:59', NULL),
(186, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 10:27:22', NULL),
(187, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 10:39:38', NULL),
(188, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 10:42:16', NULL),
(189, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 10:45:04', NULL),
(190, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 10:48:06', NULL),
(191, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 10:49:01', NULL),
(192, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 10:51:58', NULL),
(193, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 10:56:23', NULL),
(194, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 11:00:02', NULL),
(195, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 11:04:53', NULL),
(196, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 11:10:41', NULL),
(197, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 11:11:49', NULL),
(198, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 11:12:48', NULL),
(199, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 11:21:17', NULL),
(200, 'U001', 'Admin login: ADMIN1', NULL, NULL, '2026-02-04 11:27:13', NULL),
(201, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 11:35:19', NULL),
(202, 'U027', 'User login: QWERTY', NULL, NULL, '2026-02-04 11:39:29', NULL),
(203, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 13:41:02', NULL),
(204, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-04 15:13:41', NULL),
(205, 'U027', 'User logout: qwerty', NULL, NULL, '2026-02-04 15:14:17', NULL),
(206, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 15:14:22', NULL),
(207, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-02-04 15:15:20', NULL),
(208, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-04 15:15:24', NULL),
(209, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-10 17:49:24', NULL),
(210, 'U028', 'User login: vince', NULL, NULL, '2026-02-16 13:48:11', NULL),
(211, 'U028', 'User logout: vince', NULL, NULL, '2026-02-16 13:48:42', NULL),
(212, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-16 13:48:46', NULL),
(213, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-02-16 13:49:56', NULL),
(214, 'U028', 'User login: vince', NULL, NULL, '2026-02-16 13:50:00', NULL),
(215, 'U028', 'User logout: vince', NULL, NULL, '2026-02-16 13:51:07', NULL),
(216, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-16 13:51:12', NULL),
(217, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-02-16 13:51:25', NULL),
(218, 'U028', 'User login: vince', NULL, NULL, '2026-02-16 13:51:45', NULL),
(219, 'U028', 'User logout: vince', NULL, NULL, '2026-02-16 13:51:54', NULL),
(220, 'U028', 'User login: vince', NULL, NULL, '2026-02-16 13:52:32', NULL),
(221, 'U028', 'User logout: vince', NULL, NULL, '2026-02-16 13:52:38', NULL),
(222, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-16 13:52:41', NULL),
(223, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-16 13:55:38', NULL),
(224, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-02-16 14:04:02', NULL),
(225, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-19 00:51:04', NULL),
(226, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-19 00:56:13', NULL),
(227, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-19 00:59:12', NULL),
(228, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-19 01:02:24', NULL),
(229, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-19 01:05:43', NULL),
(230, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-19 01:07:25', NULL),
(231, 'U024', 'User login: alberto', NULL, NULL, '2026-02-19 06:54:05', NULL),
(232, 'U030', 'User login: alice', NULL, NULL, '2026-02-19 06:56:46', NULL),
(233, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 06:58:12', NULL),
(234, 'U024', 'User login: alberto', NULL, NULL, '2026-02-19 06:59:07', NULL),
(235, 'U024', 'User logout: alberto', NULL, NULL, '2026-02-19 06:59:18', NULL),
(236, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 06:59:21', NULL),
(237, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 07:07:57', NULL),
(238, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 07:08:22', NULL),
(239, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 07:10:32', NULL),
(240, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 07:15:21', NULL),
(241, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 07:22:55', NULL),
(242, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 07:24:35', NULL),
(243, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 07:28:07', NULL),
(244, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 07:34:10', NULL),
(245, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 07:40:26', NULL),
(246, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-02-19 07:41:18', NULL),
(247, 'U030', 'User login: alice', NULL, NULL, '2026-02-19 07:41:22', NULL),
(248, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 07:43:20', NULL),
(249, 'U001', 'Admin logout: admin1', NULL, NULL, '2026-02-19 07:43:25', NULL),
(250, 'U030', 'User login: alice', NULL, NULL, '2026-02-19 07:43:29', NULL),
(251, 'U030', 'User login: alice', NULL, NULL, '2026-02-19 07:46:32', NULL),
(252, 'U030', 'User login: alice', NULL, NULL, '2026-02-19 07:48:55', NULL),
(253, 'U030', 'User logout: alice', NULL, NULL, '2026-02-19 07:49:29', NULL),
(254, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 07:49:34', NULL),
(255, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-19 11:57:04', NULL),
(256, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-23 14:33:34', NULL),
(257, 'U027', 'User logout: qwerty', NULL, NULL, '2026-02-23 14:33:57', NULL),
(258, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-23 14:34:04', NULL),
(259, 'U027', 'User login: qwerty', NULL, NULL, '2026-02-23 15:51:38', NULL),
(260, 'U027', 'User logout: qwerty', NULL, NULL, '2026-02-23 15:53:52', NULL),
(261, 'U001', 'Admin login: admin1', NULL, NULL, '2026-02-23 15:54:55', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `AdminID` varchar(5) NOT NULL,
  `UserID` varchar(5) NOT NULL,
  `AFirstName` varchar(100) NOT NULL,
  `ALastName` varchar(100) NOT NULL,
  `Role` varchar(50) DEFAULT 'Admin'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`AdminID`, `UserID`, `AFirstName`, `ALastName`, `Role`) VALUES
('A001', 'U001', 'Carlos', 'Mendoza', 'Admin'),
('A002', 'U002', 'Maria', 'Santos', 'Admin'),
('A003', 'U003', 'Roberto', 'Cruz', 'Admin');

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `PaymentID` varchar(5) NOT NULL,
  `ViolationID` varchar(5) NOT NULL,
  `PaymentType` varchar(100) NOT NULL,
  `ReceiptNo` varchar(50) NOT NULL,
  `AmountPaid` decimal(10,2) NOT NULL,
  `PaymentDate` datetime DEFAULT current_timestamp(),
  `Status` enum('PAID','UNPAID','PENDING') DEFAULT 'UNPAID',
  `ProcessedBy` varchar(5) DEFAULT NULL,
  `VerifiedBy` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`PaymentID`, `ViolationID`, `PaymentType`, `ReceiptNo`, `AmountPaid`, `PaymentDate`, `Status`, `ProcessedBy`, `VerifiedBy`) VALUES
('P001', 'VI001', 'Cash', 'RCPT001', 500.00, '2025-12-02 09:00:00', 'PAID', 'A003', 'A001'),
('P002', 'VI002', 'Card', 'RCPT002', 1000.00, '2025-12-02 10:00:00', 'PAID', 'A003', 'A001'),
('P003', 'VI003', 'Cash', 'RCPT003', 1500.00, '2025-12-02 11:00:00', 'PAID', 'A003', 'A001'),
('P004', 'VI004', 'Card', 'RCPT004', 500.00, '2025-12-02 12:00:00', 'UNPAID', 'A003', NULL),
('P005', 'VI005', 'Cash', 'RCPT005', 1000.00, '2025-12-02 13:00:00', 'PENDING', 'A003', NULL),
('P006', 'VI006', 'Card', 'RCPT006', 1500.00, '2025-12-02 14:00:00', 'PAID', 'A003', 'A001'),
('P007', 'VI007', 'Cash', 'RCPT007', 500.00, '2025-12-02 15:00:00', 'PAID', 'A003', 'A001'),
('P008', 'VI008', 'Card', 'RCPT008', 1000.00, '2025-12-02 16:00:00', 'PAID', 'A003', 'A001'),
('P009', 'VI009', 'Cash', 'RCPT009', 1500.00, '2025-12-02 17:00:00', 'UNPAID', 'A003', NULL),
('P010', 'VI010', 'Card', 'RCPT010', 500.00, '2025-12-02 18:00:00', 'PAID', 'A003', 'A001'),
('P011', 'VI011', 'Cash', 'RCPT011', 1000.00, '2025-12-03 09:00:00', 'PAID', 'A003', 'A001'),
('P012', 'VI012', 'Card', 'RCPT012', 1500.00, '2025-12-03 10:00:00', 'PAID', 'A003', 'A001'),
('P013', 'VI013', 'Cash', 'RCPT013', 500.00, '2025-12-03 11:00:00', 'UNPAID', 'A003', NULL),
('P014', 'VI014', 'Card', 'RCPT014', 1000.00, '2025-12-03 12:00:00', 'PENDING', 'A003', NULL),
('P015', 'VI015', 'Cash', 'RCPT015', 1500.00, '2025-12-03 13:00:00', 'PAID', 'A003', 'A001'),
('P016', 'VI016', 'Card', 'RCPT016', 500.00, '2025-12-03 14:00:00', 'PAID', 'A003', 'A001'),
('P017', 'VI017', 'Cash', 'RCPT017', 1000.00, '2025-12-03 15:00:00', 'PAID', 'A003', 'A001'),
('P018', 'VI018', 'Card', 'RCPT018', 1500.00, '2025-12-03 16:00:00', 'UNPAID', 'A003', NULL),
('P019', 'VI019', 'Cash', 'RCPT019', 500.00, '2025-12-03 17:00:00', 'PAID', 'A003', 'A001'),
('P020', 'VI020', 'Card', 'RCPT020', 1000.00, '2025-12-03 18:00:00', 'PAID', 'A003', 'A001'),
('P021', 'V002', 'Cash', 'RCPT-20260127041508-C46S', 1000.00, '2026-01-27 04:15:08', 'PAID', NULL, NULL),
('P022', 'V005', 'Cash', 'RCPT-20260216135045-P9MP', 500.00, '2026-02-16 13:50:45', 'PAID', NULL, NULL),
('P023', 'V004', 'Debit Card', 'RCPT-20260223155313-26UT', 1500.00, '2026-02-23 15:53:13', 'PAID', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `residents`
--

CREATE TABLE `residents` (
  `ResidentID` varchar(5) NOT NULL,
  `UserID` varchar(5) NOT NULL,
  `RFirstName` varchar(100) NOT NULL,
  `RMiddleName` varchar(100) DEFAULT NULL,
  `RLastName` varchar(100) NOT NULL,
  `Sex` enum('Male','Female') DEFAULT NULL,
  `ContactNo` varchar(11) NOT NULL,
  `Address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `residents`
--

INSERT INTO `residents` (`ResidentID`, `UserID`, `RFirstName`, `RMiddleName`, `RLastName`, `Sex`, `ContactNo`, `Address`) VALUES
('R001', 'U004', 'John', 'A.', 'Doe', 'Male', '09171234567', NULL),
('R002', 'U005', 'Jane', 'B.', 'Smith', 'Female', '09181234567', NULL),
('R003', 'U006', 'Michael', 'C.', 'Johnson', 'Male', '09201234567', NULL),
('R004', 'U007', 'Emily', 'D.', 'Williams', 'Female', '09301234567', NULL),
('R005', 'U008', 'David', 'E.', 'Brown', 'Male', '09401234567', NULL),
('R006', 'U009', 'Sarah', 'F.', 'Jones', 'Female', '09501234567', NULL),
('R007', 'U010', 'Daniel', 'G.', 'Garcia', 'Male', '09601234567', NULL),
('R008', 'U011', 'Laura', 'H.', 'Martinez', 'Female', '09701234567', NULL),
('R009', 'U012', 'James', 'I.', 'Rodriguez', 'Male', '09801234567', NULL),
('R010', 'U013', 'Olivia', 'J.', 'Lee', 'Female', '09901234567', NULL),
('R011', 'U014', 'Robert', 'K.', 'Walker', 'Male', '09011234567', NULL),
('R012', 'U015', 'Sophia', 'L.', 'Hall', 'Female', '09121234567', NULL),
('R013', 'U016', 'William', 'M.', 'Allen', 'Male', '09221234567', NULL),
('R014', 'U017', 'Emma', 'N.', 'Young', 'Female', '09321234567', NULL),
('R015', 'U018', 'Joseph', 'O.', 'Hernandez', 'Male', '09421234567', NULL),
('R016', 'U019', 'Isabella', 'P.', 'King', 'Female', '09521234567', NULL),
('R017', 'U020', 'Charles', 'Q.', 'Wright', 'Male', '09621234567', NULL),
('R018', 'U021', 'Mia', 'R.', 'Lopez', 'Female', '09721234567', NULL),
('R019', 'U022', 'Anthony', 'S.', 'Hill', 'Male', '09821234567', NULL),
('R020', 'U023', 'Grace', 'T.', 'Scott', 'Female', '09921234567', NULL),
('R021', 'U024', 'Alberto', '', 'Dacudag', 'Male', '09123456789', 'yes'),
('R022', 'U025', 'als', '', 'sdasdw', 'Male', '09123345678', ''),
('R023', 'U026', 'yesaaa', 'yesaaaa', 'yesssda', 'Female', '09123456789', ''),
('R024', 'U027', 'alberto', '', 'dacudag', 'Female', '09123456789', ''),
('R025', 'U028', 'vince', '', 'pablo', 'Male', '09123456789', ''),
('R026', 'U029', 'ski', 'bi', 'di', 'Male', '09123456789', 'skibidi, boulevard, davao city'),
('R027', 'U030', 'alice', 'lim', 'go', 'Female', '09123456789', 'Hatdog, Tondo, Manila');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `UserID` varchar(5) NOT NULL,
  `Username` varchar(100) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `UserType` enum('Admin','Resident') NOT NULL,
  `CreatedAt` datetime DEFAULT current_timestamp(),
  `IsActive` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`UserID`, `Username`, `Password`, `UserType`, `CreatedAt`, `IsActive`) VALUES
('U001', 'admin1', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Admin', '2025-12-17 12:37:55', 1),
('U002', 'admin2', 'becf77f3ec82a43422b7712134d1860e3205c6ce778b08417a7389b43f2b4661', 'Admin', '2025-12-17 12:37:55', 1),
('U003', 'admin3', '0ca7539a8577dd196641e11315f8fc7d1dba9cc2741752642def9bcdb3599467', 'Admin', '2025-12-17 12:37:55', 1),
('U004', 'john.doe', '9b8769a4a742959a2d0298c36fb70623f2dfacda8436237df08d8dfd5b37374c', 'Resident', '2025-12-17 12:37:55', 1),
('U005', 'jane.smith', '1d4598d1949b47f7f211134b639ec32238ce73086a83c2f745713b3f12f817e5', 'Resident', '2025-12-17 12:37:55', 1),
('U006', 'michael.johnson', '9dbd5c893b5b573a1aa909c8cade58df194310e411c590d9fb0d63431841fd67', 'Resident', '2025-12-17 12:37:55', 1),
('U007', 'emily.williams', '1c6b4f2278067b875faa584b186908eb8c93289fbcb1ae3b057f66fc3c48853a', 'Resident', '2025-12-17 12:37:55', 1),
('U008', 'david.brown', 'c7cc9c9911b3221c6222b213f37acf1a75e75b02f392488ae481ec6721c7a6cd', 'Resident', '2025-12-17 12:37:55', 1),
('U009', 'sarah.jones', 'e99d9635c3e6caae5d4d3444b7cfd985997a6b99c029ac1802f320e8c4a74c04', 'Resident', '2025-12-17 12:37:55', 1),
('U010', 'daniel.garcia', '6fa33abdc23e4b9f7dd15311bea1b68a397370a16307fa1038b5d82894ce711a', 'Resident', '2025-12-17 12:37:55', 1),
('U011', 'laura.martinez', '3c8b8ed3401c4b9b261a52277e6a18cb44e13bdbb13f8e0ddf5dcfa29035340d', 'Resident', '2025-12-17 12:37:55', 1),
('U012', 'james.rodriguez', '815292cdc38cb03d04f91680b71b5c0b7454f5e1484ae9155979726255e2773b', 'Resident', '2025-12-17 12:37:55', 1),
('U013', 'olivia.lee', 'f538abfca830d84796cd2b82918862ab09f0874405c65cb03458ae7beabb3bb6', 'Resident', '2025-12-17 12:37:55', 1),
('U014', 'robert.walker', 'b2c56341cc2b9f8bf898bd7528dd39e641b51c4fbd51f241b46ad70872dd1b99', 'Resident', '2025-12-17 12:37:55', 1),
('U015', 'sophia.hall', '0be5449fd7e110e562888c7f6b2ceac607083936e4a8f286fcf9a2d672f73135', 'Resident', '2025-12-17 12:37:55', 1),
('U016', 'william.allen', '82cc50ae50f2c39014ef7b995bd1050f2638a836a9e0a123088d670dfd5f2ca8', 'Resident', '2025-12-17 12:37:55', 1),
('U017', 'emma.young', 'ae4b6c9d91b55bc6be8ff9b16057c96a72af85a872cf4505bea9a0b6cff2a65f', 'Resident', '2025-12-17 12:37:55', 1),
('U018', 'joseph.hernandez', '5c892e4e93c63f9da889313ab652cc504d88dad1844cfcef1840968f9d79e65d', 'Resident', '2025-12-17 12:37:55', 1),
('U019', 'isabella.king', '632fc5e020ce7727544d1e72c85eef818fc3a9cae7de4240e0016fc44c3cc5a8', 'Resident', '2025-12-17 12:37:55', 1),
('U020', 'charles.wright', '9a6361043893073e0359c0c3b525d02d29fb63314d646c11015b54953eedfa61', 'Resident', '2025-12-17 12:37:55', 1),
('U021', 'mia.lopez', 'd30e0424ac9f6c1c3a7b2dc90d61db4b51e1cce5d171a66153d51fef7441671c', 'Resident', '2025-12-17 12:37:55', 1),
('U022', 'anthony.hill', '8310dd19342d58aa89b230822361b026a451c7be796c074620e05d3f75caf4a2', 'Resident', '2025-12-17 12:37:55', 1),
('U023', 'grace.scott', 'd4429c5a85da5b01e74aad071d73a8b7fb1158b3d410b6444e5dde541410b110', 'Resident', '2025-12-17 12:37:55', 1),
('U024', 'alberto', '8cfd89da548e37f65451ebced79f1f74bd910bb881826ea73069b5496bef7b4d', 'Resident', '2026-01-23 14:30:00', 1),
('U025', 'awiwiu', '96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e', 'Resident', '2026-01-23 14:47:10', 1),
('U026', 'dwad', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'Resident', '2026-01-27 04:09:04', 1),
('U027', 'qwerty', '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225', 'Resident', '2026-01-27 04:13:39', 1),
('U028', 'vince', '9b8769a4a742959a2d0298c36fb70623f2dfacda8436237df08d8dfd5b37374c', 'Resident', '2026-02-16 13:48:05', 1),
('U029', 'skibidi', 'b822bb93905a9bd8b3a0c08168c427696436cf8bf37ed4ab8ebf41a07642ed1c', 'Resident', '2026-02-19 06:38:43', 1),
('U030', 'alice', '932f3c1b56257ce8539ac269d7aab42550dacf8818d075f0bdf1990562aae3ef', 'Resident', '2026-02-19 06:56:40', 1);

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `VehicleID` varchar(5) NOT NULL,
  `ResidentID` varchar(5) NOT NULL,
  `PlateNo` varchar(20) NOT NULL,
  `VehicleType` varchar(100) DEFAULT NULL,
  `Brand` varchar(100) DEFAULT NULL,
  `Model` varchar(100) DEFAULT NULL,
  `Color` varchar(50) DEFAULT NULL,
  `RegisteredBy` varchar(5) DEFAULT NULL,
  `RegistrationDate` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`VehicleID`, `ResidentID`, `PlateNo`, `VehicleType`, `Brand`, `Model`, `Color`, `RegisteredBy`, `RegistrationDate`) VALUES
('V001', 'R001', 'ABC123', 'Sedan', 'yess', 'camry', 'black', 'A001', '2025-12-17 12:37:55'),
('V002', 'R002', 'DEF456', 'SUV', 'Chevy', 'Camaro', 'Yellow', 'A001', '2025-12-17 12:37:55'),
('V003', 'R003', 'GHI789', 'Motorcycle', 'Honda', 'Civic', 'Black', 'A001', '2025-12-17 12:37:55'),
('V004', 'R004', 'JKL012', 'Truck', 'Toyota', 'Hilux', 'Blue', 'A002', '2025-12-17 12:37:55'),
('V005', 'R005', 'MNO345', 'Sedan', 'Ford', 'Mustang', 'Red', 'A002', '2025-12-17 12:37:55'),
('V006', 'R006', 'PQR678', 'SUV', 'Honda', 'SNX', 'Red', 'A002', '2025-12-17 12:37:55'),
('V007', 'R007', 'STU901', 'Van', 'Nissan', 'GTR', 'Gray', 'A001', '2025-12-17 12:37:55'),
('V008', 'R008', 'VWX234', 'Sedan', 'Ford', 'Raptor', 'Black', 'A001', '2025-12-17 12:37:55'),
('V009', 'R009', 'YZA567', 'Motorcycle', 'Honda', 'Civic', 'White', 'A002', '2025-12-17 12:37:55'),
('V010', 'R010', 'BCD890', 'SUV', 'Ford', 'Mustang', 'Blue', 'A002', '2025-12-17 12:37:55'),
('V011', 'R011', 'EFG123', 'Truck', 'Suzuki', 'Mirage', 'White', 'A001', '2025-12-17 12:37:55'),
('V012', 'R012', 'HIJ456', 'Sedan', 'Honda', 'SNX', 'Gray', 'A001', '2025-12-17 12:37:55'),
('V013', 'R013', 'KLM789', 'SUV', 'Chevy', 'Chevrollet', 'Blue', 'A002', '2025-12-17 12:37:55'),
('V014', 'R014', 'NOP012', 'Motorcycle', 'Toyota', 'Camry', 'White', 'A002', '2025-12-17 12:37:55'),
('V015', 'R015', 'QRS345', 'Van', 'Ford', 'Raptor', 'Green', 'A001', '2025-12-17 12:37:55'),
('V016', 'R016', 'TUV678', 'Sedan', 'Mitsubishi', 'Montero Sport', 'Black', 'A001', '2025-12-17 12:37:55'),
('V017', 'R017', 'WXY901', 'Truck', 'Mitsubishi', 'Montero Sport', 'White', 'A002', '2025-12-17 12:37:55'),
('V018', 'R018', 'ZAB234', 'SUV', 'Toyota', 'Camry', 'Blue', 'A002', '2025-12-17 12:37:55'),
('V019', 'R019', 'CDE567', 'Motorcycle', 'Honda', 'Civic', 'Brown', 'A001', '2025-12-17 12:37:55'),
('V020', 'R020', 'FGH890', 'Sedan', 'Lamborghini', 'Gallardo', 'Yellow', 'A001', '2025-12-17 12:37:55'),
('VH021', 'R001', 'ASDA123', NULL, 'YES', 'YES', 'YES', NULL, '2026-01-27 03:21:19'),
('VH022', 'R024', 'qwerty123', NULL, 'yess', 'yess', 'yess', NULL, '2026-01-27 04:14:27'),
('VH023', 'R025', 'skibidi123', NULL, 'toyota', 'camry', 'pink', NULL, '2026-02-16 13:49:16'),
('VH024', 'R027', 'skibidi', NULL, 'Toyota', 'Camry', 'Blue', NULL, '2026-02-19 07:34:53');

-- --------------------------------------------------------

--
-- Table structure for table `violations`
--

CREATE TABLE `violations` (
  `ViolationID` varchar(5) NOT NULL,
  `VehicleID` varchar(5) DEFAULT NULL,
  `ViolationTypeID` varchar(5) NOT NULL,
  `Speed` decimal(10,2) DEFAULT NULL,
  `Location` varchar(100) NOT NULL,
  `ViolationDate` datetime DEFAULT current_timestamp(),
  `PlateNoDetected` varchar(20) DEFAULT NULL,
  `ProcessedBy` varchar(5) DEFAULT NULL,
  `ProcessedDate` datetime DEFAULT NULL,
  `Notes` text DEFAULT NULL,
  `IsDeleted` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `violations`
--

INSERT INTO `violations` (`ViolationID`, `VehicleID`, `ViolationTypeID`, `Speed`, `Location`, `ViolationDate`, `PlateNoDetected`, `ProcessedBy`, `ProcessedDate`, `Notes`, `IsDeleted`) VALUES
('V001', 'VH021', 'VT02', NULL, '', '2026-01-27 00:00:00', NULL, NULL, NULL, NULL, 0),
('V002', 'VH022', 'VT02', NULL, '', '2026-01-27 00:00:00', NULL, NULL, NULL, NULL, 0),
('V003', 'VH022', 'VT01', NULL, '', '2026-01-27 00:00:00', NULL, NULL, NULL, NULL, 0),
('V004', 'VH022', 'VT03', NULL, '', '2026-01-22 00:00:00', NULL, NULL, NULL, NULL, 0),
('V005', 'VH023', 'VT01', NULL, '', '2026-02-15 00:00:00', NULL, NULL, NULL, NULL, 0),
('V006', 'VH024', 'VT02', NULL, '', '2026-01-19 00:00:00', NULL, NULL, NULL, NULL, 0),
('VI001', 'V001', 'VT01', 80.00, 'Main St', '2025-12-01 08:30:00', 'ABC123', 'A002', '2025-12-01 09:00:00', NULL, 0),
('VI002', 'V002', 'VT02', NULL, '2nd Ave', '2025-12-01 09:00:00', 'DEF456', 'A002', '2025-12-01 09:30:00', NULL, 0),
('VI003', 'V003', 'VT03', NULL, '3rd Blvd', '2025-12-01 10:15:00', 'GHI789', 'A002', '2025-12-01 10:45:00', NULL, 0),
('VI004', 'V004', 'VT01', 90.00, '4th St', '2025-12-01 11:00:00', 'JKL012', 'A002', '2025-12-01 11:30:00', NULL, 0),
('VI005', 'V005', 'VT02', NULL, '5th Ave', '2025-12-01 12:00:00', 'MNO345', 'A002', '2025-12-01 12:30:00', NULL, 0),
('VI006', 'V006', 'VT03', NULL, '6th St', '2025-12-01 12:30:00', 'PQR678', 'A002', '2025-12-01 13:00:00', NULL, 0),
('VI007', 'V007', 'VT01', 100.00, '7th Blvd', '2025-12-01 13:00:00', 'STU901', 'A002', '2025-12-01 13:30:00', NULL, 0),
('VI008', 'V008', 'VT02', NULL, '8th Ave', '2025-12-01 13:30:00', 'VWX234', 'A002', '2025-12-01 14:00:00', NULL, 0),
('VI009', 'V009', 'VT03', NULL, '9th St', '2025-12-01 14:00:00', 'YZA567', 'A002', '2025-12-01 14:30:00', NULL, 0),
('VI010', 'V010', 'VT01', 85.00, '10th Ave', '2025-12-01 14:30:00', 'BCD890', 'A002', '2025-12-01 15:00:00', NULL, 0),
('VI011', 'V011', 'VT02', NULL, '11th St', '2025-12-01 15:00:00', 'EFG123', 'A002', '2025-12-01 15:30:00', NULL, 0),
('VI012', 'V012', 'VT03', NULL, '12th Blvd', '2025-12-01 15:30:00', 'HIJ456', 'A002', '2025-12-01 16:00:00', NULL, 0),
('VI013', 'V013', 'VT01', 95.00, '13th St', '2025-12-01 16:00:00', 'KLM789', 'A002', '2025-12-01 16:30:00', NULL, 0),
('VI014', 'V014', 'VT02', NULL, '14th Ave', '2025-12-01 16:30:00', 'NOP012', 'A002', '2025-12-01 17:00:00', NULL, 0),
('VI015', 'V015', 'VT03', NULL, '15th Blvd', '2025-12-01 17:00:00', 'QRS345', 'A002', '2025-12-01 17:30:00', NULL, 0),
('VI016', 'V016', 'VT01', 90.00, '16th St', '2025-12-01 17:30:00', 'TUV678', 'A002', '2025-12-01 18:00:00', NULL, 0),
('VI017', 'V017', 'VT02', NULL, '17th Ave', '2025-12-01 18:00:00', 'WXY901', 'A002', '2025-12-01 18:30:00', NULL, 0),
('VI018', 'V018', 'VT03', NULL, '18th Blvd', '2025-12-01 18:30:00', 'ZAB234', 'A002', '2025-12-01 19:00:00', NULL, 0),
('VI019', 'V019', 'VT01', 80.00, '19th St', '2025-12-01 19:00:00', 'CDE567', 'A002', '2025-12-01 19:30:00', NULL, 0),
('VI020', 'V020', 'VT02', NULL, '20th Ave', '2025-12-01 19:30:00', 'FGH890', 'A002', '2025-12-01 20:00:00', NULL, 0);

-- --------------------------------------------------------

--
-- Table structure for table `violation_types`
--

CREATE TABLE `violation_types` (
  `ViolationTypeID` varchar(5) NOT NULL,
  `ViolationName` varchar(50) NOT NULL,
  `FineAmount` decimal(10,2) NOT NULL,
  `Description` text DEFAULT NULL,
  `CreatedBy` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `violation_types`
--

INSERT INTO `violation_types` (`ViolationTypeID`, `ViolationName`, `FineAmount`, `Description`, `CreatedBy`) VALUES
('VT01', 'Overspeeding', 500.00, 'Exceeding speed limit', 'A002'),
('VT02', 'Illegal Parking', 1000.00, 'Parking in prohibited zones', 'A002'),
('VT03', 'Red Light Violation', 1500.00, 'Running red traffic light', 'A002');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`LogID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`AdminID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`PaymentID`),
  ADD UNIQUE KEY `ReceiptNo` (`ReceiptNo`),
  ADD KEY `ViolationID` (`ViolationID`),
  ADD KEY `ProcessedBy` (`ProcessedBy`),
  ADD KEY `VerifiedBy` (`VerifiedBy`);

--
-- Indexes for table `residents`
--
ALTER TABLE `residents`
  ADD PRIMARY KEY (`ResidentID`),
  ADD KEY `UserID` (`UserID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`UserID`),
  ADD UNIQUE KEY `Username` (`Username`);

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`VehicleID`),
  ADD UNIQUE KEY `PlateNo` (`PlateNo`),
  ADD KEY `ResidentID` (`ResidentID`),
  ADD KEY `RegisteredBy` (`RegisteredBy`);

--
-- Indexes for table `violations`
--
ALTER TABLE `violations`
  ADD PRIMARY KEY (`ViolationID`),
  ADD KEY `VehicleID` (`VehicleID`),
  ADD KEY `ViolationTypeID` (`ViolationTypeID`),
  ADD KEY `ProcessedBy` (`ProcessedBy`);

--
-- Indexes for table `violation_types`
--
ALTER TABLE `violation_types`
  ADD PRIMARY KEY (`ViolationTypeID`),
  ADD KEY `CreatedBy` (`CreatedBy`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `LogID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=262;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD CONSTRAINT `activity_logs_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`);

--
-- Constraints for table `admins`
--
ALTER TABLE `admins`
  ADD CONSTRAINT `admins_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE;

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`ViolationID`) REFERENCES `violations` (`ViolationID`),
  ADD CONSTRAINT `payments_ibfk_2` FOREIGN KEY (`ProcessedBy`) REFERENCES `admins` (`AdminID`),
  ADD CONSTRAINT `payments_ibfk_3` FOREIGN KEY (`VerifiedBy`) REFERENCES `admins` (`AdminID`);

--
-- Constraints for table `residents`
--
ALTER TABLE `residents`
  ADD CONSTRAINT `residents_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`) ON DELETE CASCADE;

--
-- Constraints for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD CONSTRAINT `vehicles_ibfk_1` FOREIGN KEY (`ResidentID`) REFERENCES `residents` (`ResidentID`) ON DELETE CASCADE,
  ADD CONSTRAINT `vehicles_ibfk_2` FOREIGN KEY (`RegisteredBy`) REFERENCES `admins` (`AdminID`);

--
-- Constraints for table `violations`
--
ALTER TABLE `violations`
  ADD CONSTRAINT `violations_ibfk_1` FOREIGN KEY (`VehicleID`) REFERENCES `vehicles` (`VehicleID`),
  ADD CONSTRAINT `violations_ibfk_2` FOREIGN KEY (`ViolationTypeID`) REFERENCES `violation_types` (`ViolationTypeID`),
  ADD CONSTRAINT `violations_ibfk_3` FOREIGN KEY (`ProcessedBy`) REFERENCES `admins` (`AdminID`);

--
-- Constraints for table `violation_types`
--
ALTER TABLE `violation_types`
  ADD CONSTRAINT `violation_types_ibfk_1` FOREIGN KEY (`CreatedBy`) REFERENCES `admins` (`AdminID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
