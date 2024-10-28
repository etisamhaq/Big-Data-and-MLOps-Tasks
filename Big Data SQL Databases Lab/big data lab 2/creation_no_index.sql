-- Create the database without indexes
CREATE DATABASE UniversityNoIndex;
GO

USE UniversityNoIndex;
GO

-- Create Student table
CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    FirstName NVARCHAR(100),
    LastName NVARCHAR(100),
    DepartmentID INT,
    SemesterID INT
);

-- Create Teacher table
CREATE TABLE Teacher (
    TeacherID INT PRIMARY KEY,
    FirstName NVARCHAR(100),
    LastName NVARCHAR(100),
    DepartmentID INT
);

-- Create Course table
CREATE TABLE Course (
    CourseID INT PRIMARY KEY,
    CourseName NVARCHAR(100),
    DepartmentID INT
);

-- Create Semester table
CREATE TABLE Semester (
    SemesterID INT PRIMARY KEY,
    SemesterName NVARCHAR(50)
);

-- Create Department table
CREATE TABLE Department (
    DepartmentID INT PRIMARY KEY,
    DepartmentName NVARCHAR(100)
);
