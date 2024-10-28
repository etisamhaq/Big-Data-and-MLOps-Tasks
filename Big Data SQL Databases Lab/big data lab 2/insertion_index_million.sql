USE UniversityWithIndexm;
GO

-- Insert 1000000 rows into Department table
DECLARE @i INT = 1;
WHILE @i <= 1000000
BEGIN
    INSERT INTO Department (DepartmentID, DepartmentName)
    VALUES (@i, CONCAT('Department_', @i));
    SET @i = @i + 1;
END;

-- Insert 1000000 rows into Semester table
SET @i = 1;
WHILE @i <= 1000000
BEGIN
    INSERT INTO Semester (SemesterID, SemesterName)
    VALUES (@i, CONCAT('Semester_', @i));
    SET @i = @i + 1;
END;

-- Insert 1000000 rows into Student table
SET @i = 1;
WHILE @i <= 1000000
BEGIN
    INSERT INTO Student (StudentID, FirstName, LastName, DepartmentID, SemesterID)
    VALUES (@i, CONCAT('FirstName_', @i), CONCAT('LastName_', @i), (@i % 100) + 1, (@i % 10) + 1);
    SET @i = @i + 1;
END;

-- Insert 1000000 rows into Teacher table
SET @i = 1;
WHILE @i <= 1000000
BEGIN
    INSERT INTO Teacher (TeacherID, FirstName, LastName, DepartmentID)
    VALUES (@i, CONCAT('TeacherFirstName_', @i), CONCAT('TeacherLastName_', @i), (@i % 100) + 1);
    SET @i = @i + 1;
END;

-- Insert 1000000 rows into Course table
SET @i = 1;
WHILE @i <= 1000000
BEGIN
    INSERT INTO Course (CourseID, CourseName, DepartmentID)
    VALUES (@i, CONCAT('Course_', @i), (@i % 100) + 1);
    SET @i = @i + 1;
END;
