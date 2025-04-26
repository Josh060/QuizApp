-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 26, 2025 at 11:51 AM
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
  `answer` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cpp_questions`
--

INSERT INTO `cpp_questions` (`id`, `question`, `option1`, `option2`, `option3`, `option4`, `answer`) VALUES
(1, 'Which of these is not a C++ data type?', 'int', 'float', 'boolean', 'string', 'string'),
(2, 'Which operator is used to allocate memory in C++?', 'malloc', 'new', 'alloc', 'create', 'new'),
(3, 'Which library is used for input/output in C++?', 'stdio.h', 'iostream', 'string', 'vector', 'iostream'),
(4, 'What is the default return type of main() in C++?', 'int', 'void', 'float', 'double', 'int'),
(5, 'Which symbol is used for single-line comments in C++?', '//', '/* */', '--', '#', '//'),
(6, 'What does `cout << 10/0;` do?', 'Prints 0', 'Throws an error', 'Prints infinity', 'Compilation fails', 'Throws an error'),
(7, 'Which of these is used for file handling in C++?', 'fstream', 'file', 'handle', 'document', 'fstream'),
(8, 'What is the output of `sizeof(int)` on most systems?', '2', '4', '8', 'Depends on compiler', '4'),
(9, 'Which loop executes at least once?', 'for', 'while', 'do-while', 'None', 'do-while'),
(10, 'Which keyword is used to define a constant?', 'const', 'final', 'static', 'constant', 'const');

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
  `correct_answer` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `javascript_questions`
--

INSERT INTO `javascript_questions` (`id`, `question`, `option1`, `option2`, `option3`, `option4`, `correct_answer`) VALUES
(2, 'Which symbol is used for comments in JavaScript?', '//', '/* */', '<!-- -->', '#', '//'),
(3, 'Which function is used to print in JavaScript?', 'print()', 'console.log()', 'log()', 'echo()', 'console.log()'),
(4, 'Which of the following is a JavaScript framework?', 'Django', 'Spring', 'React', 'Laravel', 'React');

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
  `answer` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `java_questions`
--

INSERT INTO `java_questions` (`id`, `question`, `option1`, `option2`, `option3`, `option4`, `answer`) VALUES
(1, 'Which keyword is used to define a class in Java?', 'define', 'class', 'struct', 'object', 'class'),
(2, 'What is the default value of a boolean in Java?', 'true', 'false', 'null', '0', 'false'),
(3, 'Which method is used to start a Java program?', 'main()', 'run()', 'start()', 'execute()', 'main()'),
(4, 'Which keyword is used to define a class in Java?', 'define', 'class', 'struct', 'object', 'class'),
(5, 'What is the default value of a boolean in Java?', 'true', 'false', 'null', '0', 'false'),
(6, 'Which method is used to start a Java program?', 'main()', 'run()', 'start()', 'execute()', 'main()'),
(7, 'Which of these is not a primitive type in Java?', 'int', 'float', 'boolean', 'string', 'string'),
(8, 'What is the size of int in Java?', '2 bytes', '4 bytes', '8 bytes', 'Depends on system', '4 bytes'),
(9, 'Which collection type does not allow duplicate values?', 'ArrayList', 'LinkedList', 'HashSet', 'HashMap', 'HashSet'),
(10, 'What does `System.out.println(10 / 0);` throw?', '0', 'ArithmeticException', 'Infinity', 'Compilation Error', 'ArithmeticException'),
(11, 'What is the keyword for inheritance in Java?', 'extend', 'inherit', 'super', 'extends', 'extends'),
(12, 'Which class is the superclass of all Java classes?', 'Object', 'Super', 'Base', 'Root', 'Object'),
(13, 'Which package is imported by default in Java?', 'java.util', 'java.lang', 'java.io', 'java.net', 'java.lang');

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
  `answer` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `python_questions`
--

INSERT INTO `python_questions` (`id`, `question`, `option1`, `option2`, `option3`, `option4`, `answer`) VALUES
(1, 'What is the output of print(2**3)?', '6', '8', '9', '16', '8'),
(2, 'Which keyword is used to define a function?', 'func', 'def', 'define', 'function', 'def'),
(3, 'What data type is the result of: 3 / 2?', 'int', 'float', 'double', 'string', 'float'),
(7, 'Which of these is not a valid Python data type?', 'list', 'tuple', 'dictionary', 'array', 'array'),
(8, 'Which module is used for regular expressions?', 'regex', 're', 'regexp', 'match', 're'),
(9, 'What does `len([])` return?', 'None', '0', '1', 'Error', '0'),
(10, 'Which statement is used to exit a loop?', 'stop', 'exit', 'break', 'continue', 'break'),
(11, 'What is the correct way to start a class?', 'class MyClass:', 'MyClass class:', 'new class MyClass:', 'def class MyClass:', 'class MyClass:'),
(12, 'How do you insert an element at index 2 in a list?', 'list.add(2, item)', 'list.insert(2, item)', 'list.append(2, item)', 'list[2] = item', 'list.insert(2, item)'),
(13, 'Which operator is used for floor division?', '/', '//', '%', '**', '//');

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
(0, 'Joshs', 'JavaScript', 3, 3, '2025-04-26 09:42:58');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `java_questions`
--
ALTER TABLE `java_questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `python_questions`
--
ALTER TABLE `python_questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `user_scores`
--
ALTER TABLE `user_scores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
