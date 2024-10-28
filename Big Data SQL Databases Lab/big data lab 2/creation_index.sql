-- Create the database with indexes
CREATE DATABASE UniversityWithIndex;
GO

USE UniversityWithIndex;
GO

-- Create Student table
CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    FirstName NVARCHAR(100),
    LastName NVARCHAR(100),
    DepartmentID INT,
    SemesterID INT
);

-- Create indexes on DepartmentID and SemesterID
CREATE INDEX idx_Student_DepartmentID ON Student(DepartmentID);
CREATE INDEX idx_Student_SemesterID ON Student(SemesterID);

-- Create Teacher table
CREATE TABLE Teacher (
    TeacherID INT PRIMARY KEY,
    FirstName NVARCHAR(100),
    LastName NVARCHAR(100),
    DepartmentID INT
);

-- Create index on DepartmentID
CREATE INDEX idx_Teacher_DepartmentID ON Teacher(DepartmentID);

-- Create Course table
CREATE TABLE Course (
    CourseID INT PRIMARY KEY,
    CourseName NVARCHAR(100),
    DepartmentID INT
);

-- Create index on DepartmentID
CREATE INDEX idx_Course_DepartmentID ON Course(DepartmentID);

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
