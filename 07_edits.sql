--SELECT COUNT(*) FROM dim_department;
--SELECT * FROM dim_project;
--SELECT COUNT(*) FROM dim_employee;

--SELECT COUNT(*) FROM fact_decision;
--SELECT COUNT(*) FROM fact_decision_outcome;
--SELECT COUNT(*) FROM fact_risk_assessment;

--TRUNCATE TABLE dim_department RESTART IDENTITY;

/* INSERT INTO dim_department (department_name)
VALUES
('Technology'),
('Finance'),
('Operations'),
('Marketing'),
('Human Resources'),
('Sales'),
('Legal'),
('Procurement'),
('Research'),
('Customer Success'); */

--TRUNCATE TABLE dim_project RESTART IDENTITY;

/* INSERT INTO dim_project (project_name)
SELECT
'Project ' || x
FROM generate_series(1,100) x; */

/* ALTER TABLE dim_department
ADD CONSTRAINT uq_department_name
UNIQUE(department_name); */

/* ALTER TABLE dim_project
ADD CONSTRAINT uq_project_name
UNIQUE(project_name); */

/* INSERT INTO dim_employee(employee_name)
SELECT
'Employee ' || x
FROM generate_series(1,1000) x; */