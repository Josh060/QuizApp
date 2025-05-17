-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 18, 2025 at 01:11 AM
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
-- Database: `quiz_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `cpp_questions`
--

CREATE TABLE `cpp_questions` (
  `id` int(11) NOT NULL,
  `question` text NOT NULL,
  `option1` varchar(255) NOT NULL,
  `option2` varchar(255) NOT NULL,
  `option3` varchar(255) NOT NULL,
  `option4` varchar(255) NOT NULL,
  `correct_answer` varchar(5) DEFAULT NULL,
  `question_type` varchar(50) NOT NULL DEFAULT 'multiple_choice'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cpp_questions`
--

INSERT INTO `cpp_questions` (`id`, `question`, `option1`, `option2`, `option3`, `option4`, `correct_answer`, `question_type`) VALUES
(1, 'Which of these is not a C++ data type?', 'int', 'float', 'boolean', 'string', 'strin', 'multiple_choice'),
(2, 'Which operator is used to allocate memory in C++?', 'malloc', 'new', 'alloc', 'create', 'new', 'multiple_choice'),
(3, 'Which library is used for input/output in C++?', 'stdio.h', 'iostream', 'string', 'vector', 'iostr', 'multiple_choice'),
(4, 'What is the default return type of main() in C++?', 'int', 'void', 'float', 'double', 'int', 'multiple_choice'),
(5, 'Which symbol is used for single-line comments in C++?', '//', '/* */', '--', '#', '//', 'multiple_choice'),
(6, 'What does `cout << 10/0;` do?', 'Prints 0', 'Throws an error', 'Prints infinity', 'Compilation fails', 'Throw', 'multiple_choice'),
(7, 'Which of these is used for file handling in C++?', 'fstream', 'file', 'handle', 'document', 'fstre', 'multiple_choice'),
(8, 'What is the output of `sizeof(int)` on most systems?', '2', '4', '8', 'Depends on compiler', '4', 'multiple_choice'),
(9, 'Which loop executes at least once?', 'for', 'while', 'do-while', 'None', 'do-wh', 'multiple_choice'),
(10, 'Which keyword is used to define a constant?', 'const', 'final', 'static', 'constant', 'const', 'multiple_choice');

-- --------------------------------------------------------

--
-- Table structure for table `javascript_questions`
--

CREATE TABLE `javascript_questions` (
  `id` int(11) NOT NULL,
  `question` text NOT NULL,
  `option1` varchar(255) NOT NULL,
  `option2` varchar(255) NOT NULL,
  `option3` varchar(255) NOT NULL,
  `option4` varchar(255) NOT NULL,
  `correct_answer` varchar(255) DEFAULT NULL,
  `question_type` varchar(50) NOT NULL DEFAULT 'multiple_choice'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `javascript_questions`
--

INSERT INTO `javascript_questions` (`id`, `question`, `option1`, `option2`, `option3`, `option4`, `correct_answer`, `question_type`) VALUES
(2, 'Which symbol is used for comments in JavaScript?', '//', '/* */', '<!-- -->', '#', '//', 'multiple_choice'),
(3, 'Which function is used to print in JavaScript?', 'print()', 'console.log()', 'log()', 'echo()', 'console.log()', 'multiple_choice'),
(4, 'Which of the following is a JavaScript framework?', 'Django', 'Spring', 'React', 'Laravel', 'React', 'multiple_choice');

-- --------------------------------------------------------

--
-- Table structure for table `java_questions`
--

CREATE TABLE `java_questions` (
  `id` int(11) NOT NULL,
  `question` text NOT NULL,
  `option1` varchar(255) NOT NULL,
  `option2` varchar(255) NOT NULL,
  `option3` varchar(255) NOT NULL,
  `option4` varchar(255) NOT NULL,
  `correct_answer` varchar(5) DEFAULT NULL,
  `question_type` varchar(50) NOT NULL DEFAULT 'multiple_choice'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `java_questions`
--

INSERT INTO `java_questions` (`id`, `question`, `option1`, `option2`, `option3`, `option4`, `correct_answer`, `question_type`) VALUES
(1, 'Which keyword is used to define a class in Java?', 'define', 'class', 'struct', 'object', 'class', 'multiple_choice'),
(2, 'What is the default value of a boolean in Java?', 'true', 'false', 'null', '0', 'false', 'multiple_choice'),
(3, 'Which method is used to start a Java program?', 'main()', 'run()', 'start()', 'execute()', 'main(', 'multiple_choice'),
(6, 'Which method is used to start a Java program?', 'main()', 'run()', 'start()', 'execute()', 'main(', 'multiple_choice'),
(7, 'Which of these is not a primitive type in Java?', 'int', 'float', 'boolean', 'string', 'strin', 'multiple_choice'),
(8, 'What is the size of int in Java?', '2 bytes', '4 bytes', '8 bytes', 'Depends on system', '4 byt', 'multiple_choice'),
(9, 'Which collection type does not allow duplicate values?', 'ArrayList', 'LinkedList', 'HashSet', 'HashMap', 'HashS', 'multiple_choice'),
(10, 'What does `System.out.println(10 / 0);` throw?', '0', 'ArithmeticException', 'Infinity', 'Compilation Error', 'Arith', 'multiple_choice'),
(11, 'What is the keyword for inheritance in Java?', 'extend', 'inherit', 'super', 'extends', 'exten', 'multiple_choice'),
(12, 'Which class is the superclass of all Java classes?', 'Object', 'Super', 'Base', 'Root', 'Objec', 'multiple_choice'),
(13, 'Which package is imported by default in Java?', 'java.util', 'java.lang', 'java.io', 'java.net', 'java.', 'multiple_choice');

-- --------------------------------------------------------

--
-- Table structure for table `python_questions`
--

CREATE TABLE `python_questions` (
  `id` int(11) NOT NULL,
  `question` text NOT NULL,
  `option1` varchar(255) NOT NULL,
  `option2` varchar(255) NOT NULL,
  `option3` varchar(255) NOT NULL,
  `option4` varchar(255) NOT NULL,
  `correct_answer` varchar(5) DEFAULT NULL,
  `question_type` varchar(50) NOT NULL DEFAULT 'multiple_choice'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `python_questions`
--

INSERT INTO `python_questions` (`id`, `question`, `option1`, `option2`, `option3`, `option4`, `correct_answer`, `question_type`) VALUES
(1, 'What is the output of `print(2 + 3 * 4)`?', '14', '20', '11', '12', '14', 'multiple_choice'),
(2, 'What is the correct way to define a function in Python?', 'def func()', 'func() def', 'function()', 'def function()', 'def f', 'multiple_choice'),
(3, 'What does the `len()` function do?', 'Returns the length of an object', 'Returns the size of an object', 'Returns the last element', 'None of the above', 'Retur', 'multiple_choice'),
(4, 'Which of the following is mutable in Python?', 'Tuple', 'List', 'String', 'Dictionary', 'List', 'multiple_choice'),
(5, 'What is the correct way to create a set in Python?', 'set(1, 2, 3)', '{1, 2, 3}', '[1, 2, 3]', '(1, 2, 3)', '{1, 2', 'multiple_choice'),
(6, 'Which of the following is an immutable data type?', 'List', 'Set', 'Tuple', 'Dictionary', 'Tuple', 'multiple_choice'),
(7, 'What is the result of `5 // 2` in Python?', '2.5', '2', '3', '3.0', '2', 'multiple_choice'),
(8, 'What does `break` do in a loop?', 'Exits the loop', 'Continues the loop', 'Skips the loop', 'None of the above', 'Exits', 'multiple_choice'),
(9, 'How do you handle exceptions in Python?', 'try-except', 'catch', 'error-handling', 'raise', 'try-e', 'multiple_choice'),
(10, 'What is the result of `len(\"Hello\")`?', '5', '4', '6', '7', '5', 'multiple_choice'),
(11, 'Which keyword is used to define a class in Python?', 'class', 'def', 'function', 'object', 'class', 'multiple_choice'),
(12, 'What is the output of `print(3 ** 2)`?', '6', '9', '8', '5', '9', 'multiple_choice'),
(13, 'How do you create a dictionary in Python?', 'dict{key: value}', '{key: value}', '[key: value]', '(key: value)', '{key:', 'multiple_choice'),
(14, 'Which function is used to get the current time in Python?', 'time()', 'datetime()', 'get_time()', 'now()', 'datet', 'multiple_choice'),
(15, 'What does `continue` do in a loop?', 'Exits the loop', 'Skips the current iteration and continues with the next', 'Breaks the loop', 'None of the above', 'Skips', 'multiple_choice'),
(16, 'Which of the following is used to import modules in Python?', 'import module', 'include module', 'use module', 'module import', 'impor', 'multiple_choice'),
(17, 'What is the correct syntax to create a while loop in Python?', 'while condition:', 'loop while condition:', 'for while condition:', 'condition while:', 'while', 'multiple_choice'),
(18, 'What is the purpose of `self` in a Python class?', 'Refers to the current instance of the class', 'Refers to the class itself', 'Refers to a global variable', 'None of the above', 'Refer', 'multiple_choice'),
(19, 'How do you check if a key exists in a dictionary?', '`key in dictionary`', '`key.exists(dictionary)`', '`dictionary.has(key)`', '`key.contains(dictionary)`', '`key ', 'multiple_choice'),
(20, 'What does the `open()` function do in Python?', 'Opens a file', 'Opens a database', 'Opens a network connection', 'None of the above', 'Opens', 'multiple_choice');

-- --------------------------------------------------------

--
-- Table structure for table `quiz_history`
--

CREATE TABLE `quiz_history` (
  `id` int(11) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `language` varchar(50) NOT NULL,
  `score` int(11) NOT NULL,
  `total_questions` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `quiz_history`
--

INSERT INTO `quiz_history` (`id`, `user_name`, `language`, `score`, `total_questions`, `timestamp`) VALUES
(1, 'a', 'javascript', 3, 3, '2025-04-27 21:57:46'),
(2, 'a', 'javascript', 3, 3, '2025-04-27 21:58:45'),
(3, 'a', 'javascript', 3, 3, '2025-04-27 22:00:46'),
(4, 'a', 'javascript', 3, 3, '2025-04-27 22:03:53'),
(5, 'a', 'javascript', 3, 3, '2025-04-28 00:27:20'),
(6, 'a', 'cpp', 0, 10, '2025-04-28 00:27:48'),
(7, 'a', 'javascript', 0, 3, '2025-04-28 00:58:04'),
(8, 'a', 'javascript', 0, 3, '2025-04-28 01:04:08'),
(9, 'a', 'javascript', 2, 3, '2025-04-28 05:03:19'),
(10, 'a', 'javascript', 3, 3, '2025-04-28 12:13:03'),
(11, 'a', 'javascript', 0, 3, '2025-04-28 14:37:59'),
(12, 'a', 'javascript', 3, 3, '2025-04-28 14:49:39'),
(13, 'a', 'javascript', 3, 3, '2025-04-28 14:56:14'),
(14, 'q', 'javascript', 3, 3, '2025-04-28 15:26:56'),
(15, 'a', 'javascript', 1, 3, '2025-04-28 15:28:27'),
(16, 'a', 'javascript', 2, 3, '2025-04-28 16:08:09'),
(17, 'a', 'javascript', 1, 3, '2025-04-28 16:09:24'),
(18, 'a', 'javascript', 1, 3, '2025-04-28 16:52:30'),
(19, 'a', 'javascript', 2, 3, '2025-04-28 16:54:32'),
(20, 'a', 'javascript', 2, 3, '2025-04-28 16:55:35'),
(21, 'a', 'javascript', 1, 3, '2025-04-28 16:59:14'),
(22, 'a', 'javascript', 1, 3, '2025-04-28 17:04:27'),
(23, 'a', 'javascript', 0, 3, '2025-04-28 17:07:49'),
(24, 'a', 'javascript', 0, 3, '2025-04-28 17:09:32'),
(25, 'a', 'javascript', 0, 3, '2025-04-28 17:11:46'),
(26, 'a', 'javascript', 1, 3, '2025-04-28 17:14:23'),
(27, 'a', 'javascript', 0, 3, '2025-04-28 17:16:25'),
(28, 'a', 'javascript', 2, 3, '2025-04-28 17:19:09'),
(29, 'a', 'javascript', 2, 3, '2025-04-28 17:20:50'),
(30, 'a', 'javascript', 2, 3, '2025-04-28 17:22:36'),
(31, 'a', 'javascript', 3, 3, '2025-04-28 17:26:34'),
(32, 'a', 'javascript', 1, 3, '2025-04-28 17:36:35'),
(33, 'a', 'javascript', 2, 3, '2025-04-28 17:37:43'),
(34, 'a', 'javascript', 1, 3, '2025-04-28 17:39:11'),
(35, 'a', 'python', 1, 10, '2025-04-28 17:39:50'),
(36, 'a', 'javascript', 1, 3, '2025-04-28 17:42:42'),
(37, 'j', 'javascript', 2, 3, '2025-04-28 17:44:00'),
(38, 'a', 'javascript', 3, 3, '2025-04-28 17:46:36'),
(39, 'a', 'javascript', 1, 3, '2025-04-28 21:51:46'),
(40, 'a', 'java', 1, 11, '2025-04-28 22:03:40'),
(41, 'a', 'javascript', 2, 3, '2025-04-28 22:03:58'),
(42, 'a', 'javascript', 3, 3, '2025-04-28 22:11:25'),
(43, 'a', 'javascript', 4, 3, '2025-04-28 22:12:53'),
(44, 'a', 'javascript', 0, 3, '2025-04-28 22:25:08'),
(45, 'a', 'javascript', 3, 3, '2025-04-28 22:26:58'),
(46, 'a', 'javascript', 2, 3, '2025-04-28 22:29:06'),
(47, 'a', 'javascript', 3, 3, '2025-04-28 22:36:57'),
(48, 'a', 'javascript', 2, 4, '2025-04-29 01:14:10'),
(49, 'sa', 'javascript', 0, 4, '2025-05-04 12:39:49'),
(50, 'hj', 'javascript', 0, 4, '2025-05-04 12:41:27'),
(51, 'a', 'javascript', 0, 4, '2025-05-04 12:42:16'),
(52, 'as', 'javascript', 0, 4, '2025-05-04 12:43:50'),
(53, 'sss', 'javascript', 0, 4, '2025-05-04 12:46:55'),
(54, 'a', 'javascript', 0, 4, '2025-05-04 12:54:40'),
(55, 'a', 'javascript', 0, 4, '2025-05-04 12:56:48'),
(56, 'sss', 'javascript', 0, 4, '2025-05-04 13:07:12'),
(57, 'hg', 'javascript', 0, 4, '2025-05-04 13:20:00'),
(58, 'aaa', 'javascript', 0, 4, '2025-05-04 13:26:10'),
(59, 'aaa', 'javascript', 0, 4, '2025-05-04 13:30:08'),
(60, 'asa', 'javascript', 0, 4, '2025-05-05 00:14:43'),
(61, 'sasasa', 'javascript', 0, 4, '2025-05-05 00:17:11'),
(62, 'asas', 'javascript', 0, 4, '2025-05-05 00:24:28'),
(63, 'asas', 'javascript', 0, 4, '2025-05-05 00:30:35'),
(64, 'a', 'javascript', 0, 4, '2025-05-05 00:33:19'),
(65, 'aa', 'javascript', 0, 4, '2025-05-05 01:06:33'),
(66, 'a', 'javascript', 0, 4, '2025-05-05 01:20:19'),
(67, 'as', 'javascript', 0, 4, '2025-05-05 01:26:54'),
(68, 'asa', 'javascript', 0, 4, '2025-05-05 03:06:40'),
(69, 'aa', 'javascript', 0, 4, '2025-05-05 03:21:55'),
(70, 'asa', 'javascript', 0, 4, '2025-05-05 03:46:17'),
(71, 'aa', 'javascript', 0, 4, '2025-05-05 04:06:30'),
(72, 'aa', 'javascript', 0, 4, '2025-05-05 04:10:42'),
(73, 'aa', 'javascript', 0, 4, '2025-05-05 04:13:54'),
(74, 'sasa', 'javascript', 0, 4, '2025-05-05 04:15:39'),
(75, 'aaa', 'javascript', 0, 4, '2025-05-05 04:24:13'),
(76, 'asss', 'javascript', 0, 4, '2025-05-05 04:31:04'),
(77, 'asa', 'javascript', 0, 4, '2025-05-05 04:34:11'),
(78, 'aaa', 'javascript', 0, 4, '2025-05-05 04:36:21'),
(79, 'aaa', 'javascript', 1, 4, '2025-05-05 04:39:24'),
(80, 'aaa', 'javascript', 1, 4, '2025-05-05 04:40:32'),
(81, 'aaa', 'javascript', 1, 4, '2025-05-05 05:34:04'),
(82, 'fdfd', 'javascript', 4, 4, '2025-05-05 05:39:00'),
(83, 'aaa', 'javascript', 4, 4, '2025-05-05 05:43:06'),
(84, 'aaa', 'javascript', 0, 4, '2025-05-05 05:44:46'),
(85, 'aaa', 'javascript', 4, 4, '2025-05-05 05:49:52'),
(86, 'aaa', 'javascript', 4, 4, '2025-05-05 05:55:27'),
(87, 'aaa', 'javascript', 0, 4, '2025-05-05 06:08:45'),
(88, 'aaa', 'javascript', 0, 4, '2025-05-05 06:13:15'),
(89, 'aaa', 'javascript', 0, 4, '2025-05-05 07:42:15'),
(90, 'aaa', 'javascript', 0, 4, '2025-05-05 07:44:06'),
(91, 'aaa', 'java', 0, 11, '2025-05-05 07:49:04'),
(92, 'aaa', 'javascript', 0, 4, '2025-05-05 07:50:34'),
(93, 'vh', 'javascript', 4, 4, '2025-05-05 08:17:42'),
(94, 'mm', 'javascript', 0, 4, '2025-05-05 08:37:57'),
(95, 'aaaa', 'javascript', 0, 4, '2025-05-05 09:03:39'),
(96, 'aaaa', 'javascript', 0, 4, '2025-05-05 09:10:00'),
(97, 'sad', 'javascript', 4, 4, '2025-05-05 11:08:13'),
(98, 'ass', 'javascript', 4, 4, '2025-05-05 11:08:40'),
(99, 'ddsa', 'javascript', 4, 4, '2025-05-05 11:12:01'),
(100, 'ds', 'javascript', 4, 4, '2025-05-05 11:16:00'),
(101, 'dsd', 'javascript', 4, 4, '2025-05-05 11:27:53'),
(102, 'ssad', 'javascript', 4, 4, '2025-05-05 11:31:36'),
(103, 'asdsda', 'javascript', 4, 4, '2025-05-05 11:34:12'),
(104, 'sdadas', 'javascript', 3, 4, '2025-05-05 11:41:54'),
(105, 'sdsa', 'javascript', 4, 4, '2025-05-05 11:43:31'),
(106, 'sad', 'javascript', 4, 4, '2025-05-05 11:46:20'),
(107, 'asdas', 'javascript', 4, 4, '2025-05-05 12:01:21'),
(108, 'ahbhg', 'javascript', 4, 4, '2025-05-05 12:13:48'),
(109, 'asd', 'javascript', 4, 4, '2025-05-05 12:23:34'),
(110, 'asdasd', 'javascript', 4, 4, '2025-05-05 12:25:01'),
(111, 'user', 'javascript', 4, 4, '2025-05-05 12:28:47'),
(112, 'sadsda', 'cpp', 3, 10, '2025-05-05 12:36:01'),
(113, 'sad', 'python', 1, 2, '2025-05-05 12:36:50'),
(114, 'user', 'javascript', 4, 4, '2025-05-05 12:57:16'),
(115, 'ssad', 'javascript', 4, 4, '2025-05-05 13:19:41'),
(116, 'asd', 'javascript', 4, 4, '2025-05-05 13:27:31'),
(117, 'gh', 'javascript', 4, 4, '2025-05-05 13:43:23'),
(118, 'sad', 'python', 3, 3, '2025-05-05 13:46:05'),
(119, 'as', 'javascript', 4, 4, '2025-05-05 13:46:38'),
(120, 'sdasd', 'javascript', 4, 4, '2025-05-05 13:50:13'),
(121, 'as', 'javascript', 4, 4, '2025-05-05 13:51:18'),
(122, 'sss', 'javascript', 4, 4, '2025-05-05 22:22:05'),
(123, 'asda', 'javascript', 3, 4, '2025-05-05 22:48:24'),
(124, 'asda', 'javascript', 4, 4, '2025-05-05 23:47:43'),
(125, 'asdas', 'javascript', 2, 4, '2025-05-05 23:55:04'),
(126, 'dsfsd', 'javascript', 3, 4, '2025-05-05 23:56:15'),
(127, 'asdas', 'javascript', 0, 4, '2025-05-06 00:15:30'),
(128, 'asdas', 'javascript', 2, 4, '2025-05-06 00:16:36'),
(129, 'asdas', 'python', 0, 10, '2025-05-06 00:25:54'),
(130, 'asdas', 'javascript', 3, 4, '2025-05-06 01:06:12'),
(131, 'andot', 'javascript', 0, 4, '2025-05-06 02:21:19'),
(132, 'asda', 'javascript', 4, 4, '2025-05-07 00:48:04'),
(133, 'asdas', 'javascript', 3, 4, '2025-05-07 00:51:28'),
(134, 'sad', 'javascript', 2, 4, '2025-05-07 00:57:39'),
(135, 'asd', 'javascript', 4, 4, '2025-05-07 01:03:00'),
(136, 'dasd', 'javascript', 3, 4, '2025-05-07 01:06:09'),
(137, 'josh', 'javascript', 4, 4, '2025-05-09 14:14:31'),
(138, 'josh', 'javascript', 4, 4, '2025-05-09 14:57:32'),
(139, 'asd', 'javascript', 4, 4, '2025-05-09 15:00:07'),
(140, 'josh', 'javascript', 4, 4, '2025-05-09 15:52:33'),
(141, 'josh', 'javascript', 4, 4, '2025-05-09 16:10:54'),
(142, 'josh', 'javascript', 3, 4, '2025-05-09 16:33:27'),
(143, 'josh', 'javascript', 3, 4, '2025-05-09 16:38:00'),
(144, 'josh', 'javascript', 2, 4, '2025-05-10 04:29:40'),
(145, 'josh', 'javascript', 2, 4, '2025-05-10 06:56:02'),
(146, 'josh', 'javascript', 4, 4, '2025-05-10 07:10:26'),
(147, 'josh', 'javascript', 4, 4, '2025-05-10 07:19:43'),
(148, 'josh', 'javascript', 4, 4, '2025-05-10 08:33:44'),
(149, 'josh', 'javascript', 4, 4, '2025-05-10 08:43:42'),
(150, 'josh', 'javascript', 4, 4, '2025-05-10 08:50:14'),
(151, 'sada', 'javascript', 4, 4, '2025-05-10 08:56:16'),
(152, 'asd', 'javascript', 4, 4, '2025-05-10 09:03:44'),
(153, 'sa', 'javascript', 3, 3, '2025-05-10 09:07:57'),
(154, 'a', 'javascript', 3, 3, '2025-05-10 09:15:46'),
(155, 'sada', 'javascript', 3, 3, '2025-05-10 09:19:01'),
(156, 'sada', 'javascript', 3, 3, '2025-05-10 09:21:40'),
(157, 'as', 'javascript', 0, 3, '2025-05-10 09:23:35'),
(158, 'asd', 'javascript', 2, 3, '2025-05-10 09:29:29'),
(159, 'asd', 'cpp', 0, 10, '2025-05-10 09:30:23'),
(160, 'asd', 'javascript', 3, 3, '2025-05-10 10:30:22'),
(161, 'dsadsa', 'javascript', 3, 3, '2025-05-10 11:11:06'),
(162, 'bhj', 'javascript', 2, 3, '2025-05-10 11:20:33'),
(163, 'asda', 'javascript', 3, 3, '2025-05-10 11:25:00'),
(164, 'asd', 'javascript', 3, 3, '2025-05-10 11:28:37'),
(165, 'josh', 'javascript', 3, 3, '2025-05-11 01:01:47'),
(166, 'josh', 'javascript', 3, 3, '2025-05-11 01:42:17'),
(167, 'qwe', 'javascript', 3, 3, '2025-05-11 01:43:13'),
(168, 'sa', 'javascript', 3, 3, '2025-05-11 01:56:57'),
(169, 'asd', 'javascript', 3, 3, '2025-05-11 01:59:46'),
(170, 'sd', 'javascript', 3, 3, '2025-05-11 02:10:49'),
(171, 'asd', 'javascript', 3, 3, '2025-05-11 02:33:50'),
(172, 'josh', 'javascript', 3, 3, '2025-05-11 12:41:20'),
(173, 'josh', 'javascript', 3, 3, '2025-05-11 12:45:35'),
(174, 'josh', 'javascript', 3, 3, '2025-05-11 12:47:55'),
(175, 'josh', 'javascript', 3, 3, '2025-05-11 14:40:47'),
(176, 'josh', 'javascript', 3, 3, '2025-05-11 14:41:11'),
(177, 'josh', 'javascript', 3, 3, '2025-05-11 14:44:12'),
(178, 'josh', 'javascript', 1, 3, '2025-05-11 14:44:40'),
(179, 'josh', 'javascript', 3, 3, '2025-05-11 15:22:06');

-- --------------------------------------------------------

--
-- Table structure for table `scores`
--

CREATE TABLE `scores` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `language` varchar(50) NOT NULL,
  `score` int(11) NOT NULL,
  `total_questions` int(11) NOT NULL,
  `submitted_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `scores`
--

INSERT INTO `scores` (`id`, `username`, `language`, `score`, `total_questions`, `submitted_at`) VALUES
(0, 'Joshs', 'JavaScript', 0, 3, '2025-04-26 06:44:13'),
(0, 'Joshs', 'JavaScript', 0, 3, '2025-04-26 06:54:20'),
(0, 'Joshs', 'C++', 5, 10, '2025-04-26 07:04:38'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 07:51:59'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 07:52:02'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 07:57:07'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 08:04:00'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 08:14:16'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 08:16:15'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 08:23:14'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 08:36:17'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 08:39:30'),
(0, 'Joshs', 'JavaScript', 2, 3, '2025-04-26 08:43:50'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 08:51:49'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 08:54:02'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 08:59:26'),
(0, 'Joshs', 'JavaScript', 2, 3, '2025-04-26 09:06:40'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 09:11:21'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 09:13:02'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 09:30:21'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 09:42:58'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 12:10:50'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 12:11:00'),
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 12:17:30'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 04:03:08'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 10:31:49'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 10:34:58'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 10:41:03'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 10:44:22'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 10:46:58'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 10:56:28'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 10:57:51'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 10:59:55'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 11:02:25'),
(0, 'deu', 'javascript', 0, 3, '2025-04-27 11:13:55'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 11:15:26'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 11:20:14'),
(0, 'deu', 'javascript', 0, 3, '2025-04-27 11:22:33'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 11:23:45'),
(0, 'jbsa', 'javascript', 0, 3, '2025-04-27 11:25:43'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 11:27:43'),
(0, 'dsf', 'javascript', 0, 3, '2025-04-27 11:29:34'),
(0, 'asd', 'javascript', 2, 3, '2025-04-27 11:31:37'),
(0, 'josh', 'javascript', 0, 3, '2025-04-27 13:27:19'),
(0, 'josh', 'javascript', 3, 3, '2025-04-27 13:41:43'),
(0, 'josh', 'javascript', 3, 3, '2025-04-27 15:53:23'),
(0, 'josh', 'javascript', 3, 3, '2025-04-27 16:20:42'),
(0, 'josh', 'javascript', 3, 3, '2025-04-27 16:26:43'),
(0, 'a', 'javascript', 0, 3, '2025-04-27 17:30:28'),
(0, 'a', 'javascript', 0, 3, '2025-04-27 17:30:28'),
(0, 'a', 'javascript', 0, 3, '2025-04-27 17:30:28'),
(0, 'a', 'javascript', 0, 3, '2025-04-27 17:30:28'),
(0, 'a', 'javascript', 0, 3, '2025-04-27 17:33:46'),
(0, 'a', 'javascript', 0, 3, '2025-04-27 17:33:46'),
(0, 'a', 'javascript', 0, 3, '2025-04-27 17:33:46'),
(0, 'a', 'javascript', 0, 3, '2025-04-27 17:38:31'),
(0, 'a', 'javascript', 3, 3, '2025-04-27 17:40:49'),
(0, 'a', 'javascript', 3, 3, '2025-04-27 17:40:49'),
(0, 'a', 'javascript', 3, 3, '2025-04-27 17:40:49'),
(0, 'a', 'javascript', 3, 3, '2025-04-27 17:42:35'),
(0, 'a', 'javascript', 1, 3, '2025-04-27 17:50:25'),
(0, 'a', 'javascript', 1, 3, '2025-04-27 17:50:25'),
(0, 'a', 'javascript', 1, 3, '2025-04-27 17:52:45'),
(0, 'a', 'javascript', 1, 3, '2025-04-27 17:52:45'),
(0, 'a', 'javascript', 1, 3, '2025-04-27 17:55:47'),
(0, 'a', 'javascript', 1, 3, '2025-04-27 17:55:47'),
(0, 'a', 'javascript', 1, 3, '2025-04-27 17:57:18'),
(0, 'a', 'javascript', 1, 3, '2025-04-27 17:59:19'),
(0, 'a', 'java', 0, 13, '2025-04-27 17:59:42'),
(0, 'a', 'javascript', 2, 3, '2025-04-27 18:18:54'),
(0, 'a', 'javascript', 2, 3, '2025-04-27 18:23:16'),
(0, 'a', 'javascript', 3, 3, '2025-04-27 18:25:41');

-- --------------------------------------------------------

--
-- Table structure for table `user_scores`
--

CREATE TABLE `user_scores` (
  `id` int(11) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `language` varchar(50) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `total_questions` int(11) DEFAULT NULL,
  `submitted_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cpp_questions`
--
ALTER TABLE `cpp_questions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `javascript_questions`
--
ALTER TABLE `javascript_questions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `java_questions`
--
ALTER TABLE `java_questions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `python_questions`
--
ALTER TABLE `python_questions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `quiz_history`
--
ALTER TABLE `quiz_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_scores`
--
ALTER TABLE `user_scores`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cpp_questions`
--
ALTER TABLE `cpp_questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `javascript_questions`
--
ALTER TABLE `javascript_questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `java_questions`
--
ALTER TABLE `java_questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `python_questions`
--
ALTER TABLE `python_questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `quiz_history`
--
ALTER TABLE `quiz_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=180;

--
-- AUTO_INCREMENT for table `user_scores`
--
ALTER TABLE `user_scores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
