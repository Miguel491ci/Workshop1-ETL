CREATE DATABASE IF NOT EXISTS hiring_excercise;
USE hiring_excercise;

-- ==============================
-- DIMENSIONS
-- ==============================

CREATE TABLE IF NOT EXISTS DimCandidate (
    CandidateID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Email VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS DimCountry (
    CountryID INT PRIMARY KEY AUTO_INCREMENT,
    CountryName VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS DimDate (
    DateID INT PRIMARY KEY AUTO_INCREMENT,
    FullDate DATE,
    Year INT,
    Month INT,
    Quarter INT
);

CREATE TABLE IF NOT EXISTS DimSeniority (
    SeniorityID INT PRIMARY KEY AUTO_INCREMENT,
    SeniorityLevel VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS DimTechnology (
    TechnologyID INT PRIMARY KEY AUTO_INCREMENT,
    TechnologyName VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS DimExperience (
    ExperienceID INT PRIMARY KEY AUTO_INCREMENT,
    ExactYoe INT
);

-- ==============================
-- FACT TABLE
-- ==============================

CREATE TABLE IF NOT EXISTS FactHiring (
    FactID INT PRIMARY KEY AUTO_INCREMENT,
    CandidateID INT,
    CountryID INT,
    DateID INT,
    SeniorityID INT,
    TechnologyID INT,
    ExperienceID INT,
    CodeChallengeScore DECIMAL(5,2),
    TechnicalInterviewScore DECIMAL(5,2),
    HiredFlag BOOLEAN,
    FOREIGN KEY (CandidateID) REFERENCES DimCandidate(CandidateID),
    FOREIGN KEY (CountryID) REFERENCES DimCountry(CountryID),
    FOREIGN KEY (DateID) REFERENCES DimDate(DateID),
    FOREIGN KEY (SeniorityID) REFERENCES DimSeniority(SeniorityID),
    FOREIGN KEY (TechnologyID) REFERENCES DimTechnology(TechnologyID),
    FOREIGN KEY (ExperienceID) REFERENCES DimExperience(ExperienceID)
);

