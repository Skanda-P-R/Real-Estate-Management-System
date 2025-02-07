-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 07, 2025 at 11:54 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `real_estate_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `property_id` int(11) NOT NULL,
  `booking_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`id`, `customer_id`, `property_id`, `booking_date`) VALUES
(1, 3, 1, '2025-02-07 06:32:34'),
(4, 4, 6, '2025-02-07 10:45:03'),
(5, 4, 10, '2025-02-07 10:53:54');

-- --------------------------------------------------------

--
-- Table structure for table `properties`
--

CREATE TABLE `properties` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `location` varchar(255) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `status` enum('available','booked') DEFAULT 'available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `properties`
--

INSERT INTO `properties` (`id`, `title`, `description`, `price`, `location`, `owner_id`, `status`) VALUES
(1, '3BHK Flat in Srinagar', 'There is a 3BHK flat available for rent in Srinagar Bangalore.', 15000.00, 'Srinagar', 2, 'booked'),
(2, '2BHK Apartment in Delhi', 'A well-furnished 2BHK apartment available for rent in Delhi.', 18000.00, 'Delhi', 2, 'available'),
(3, 'Luxury Villa in Mumbai', 'A spacious 4BHK luxury villa with a sea view in Mumbai.', 75000.00, 'Mumbai', 2, 'available'),
(4, 'Studio Apartment in Bangalore', 'A compact studio apartment suitable for bachelors in Bangalore.', 12000.00, 'Bangalore', 2, 'available'),
(6, 'Penthouse in Hyderabad', 'A 5BHK penthouse with a rooftop pool in Hyderabad.', 90000.00, 'Hyderabad', 2, 'booked'),
(8, 'Farmhouse in Goa', 'A serene farmhouse with a beachside view in Goa.', 60000.00, 'Goa', 2, 'available'),
(9, '1RK PG in Kengeri', 'A spacious 1RK PG room is available for rent near RVCE college, Kengeri.', 5000.00, 'Kengeri', 2, 'available'),
(10, '2BHK Penthouse in MG Road', 'A luxurious Penthouse is available for rent in MG Road. ', 100000.00, 'MG Road', 5, 'booked');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','owner','customer') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `role`) VALUES
(1, 'Skanda', 'skandapr@gmail.com', 'scrypt:32768:8:1$ximGrzmcMooNcoDE$5e67a046df2b438c9d0152e84316c7cacec4cfe6545206acec0b451bb31ca6b8fed968394d0466aba27b6681cb9c76701c32f6d3d83af1f3aa1b45169923ecd4', 'admin'),
(2, 'Sneha', 'sneha@gmail.com', 'scrypt:32768:8:1$0bvsRY4qLA7XBO80$d35e0869a880a95ce99cbaca0873a57f6ae8dd1ebd301515477fa5be46f8a6926ba361a143f2c97c9dd69d10d2dd71215ad9b119696fb2db664ac9af06d92fb5', 'owner'),
(3, 'Phaniraj', 'phaniraj@gmail.com', 'scrypt:32768:8:1$IV16tceUuFdjKgav$848c10f82bd129d96181eb9370ddae33735ddf1ac2f0984151eb59d77e0bba694e2794ed2fc4c3be266a22c7c19017ca034bb69ed6d19258819e789a5c6880cd', 'customer'),
(4, 'Rekha', 'rekha@gmail.com', 'scrypt:32768:8:1$hh3m41tp5lEWQ7FB$783fd6b7dcecf8f63e536c34b848c7aeee4342a8baebba7225f683eef2415af3eb62463352971a616d91cf5f92bf4d32382e9c57db35168da0625c8f87bb4fa4', 'customer'),
(5, 'Vaibhav', 'vaibhav@yahoo.in', 'scrypt:32768:8:1$MiZiKi5eHXaOGprc$86870c0978bcc3af6cb9053ec628bf29d7446770598c445b3817b184418ac71563d67be99e30c7807a41906320f5126d72b0c45948b6dc8c739f47376f2501c9', 'owner');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `property_id` (`property_id`);

--
-- Indexes for table `properties`
--
ALTER TABLE `properties`
  ADD PRIMARY KEY (`id`),
  ADD KEY `owner_id` (`owner_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `properties`
--
ALTER TABLE `properties`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`property_id`) REFERENCES `properties` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `properties`
--
ALTER TABLE `properties`
  ADD CONSTRAINT `properties_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
