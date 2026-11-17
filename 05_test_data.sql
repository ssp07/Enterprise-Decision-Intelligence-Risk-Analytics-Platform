INSERT INTO dim_department(department_name) VALUES ('Technology'),('Finance') ON CONFLICT DO NOTHING;
INSERT INTO fact_decision(project_id,employee_id,decision_date,estimated_cost) VALUES (1,1,CURRENT_DATE,100000);
INSERT INTO fact_decision_outcome(decision_id,actual_cost,actual_benefit,success_rating) VALUES (1,90000,250000,9);