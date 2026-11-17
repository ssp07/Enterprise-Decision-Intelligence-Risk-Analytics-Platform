CREATE TABLE IF NOT EXISTS dim_department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_employee (
    employee_id SERIAL PRIMARY KEY,
    employee_name VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS dim_role (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_location (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_project (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS dim_decision_type (
    decision_type_id SERIAL PRIMARY KEY,
    decision_type VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_risk_type (
    risk_type_id SERIAL PRIMARY KEY,
    risk_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_vendor (
    vendor_id SERIAL PRIMARY KEY,
    vendor_name VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS dim_business_unit (
    business_unit_id SERIAL PRIMARY KEY,
    business_unit_name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id SERIAL PRIMARY KEY,
    full_date DATE
);