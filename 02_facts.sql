CREATE TABLE IF NOT EXISTS fact_decision (decision_id BIGSERIAL PRIMARY KEY, project_id INT, employee_id INT, decision_date DATE, estimated_cost NUMERIC(12,2));
CREATE TABLE IF NOT EXISTS fact_decision_outcome (outcome_id BIGSERIAL PRIMARY KEY, decision_id BIGINT, actual_cost NUMERIC(12,2), actual_benefit NUMERIC(12,2), success_rating INT);
CREATE TABLE IF NOT EXISTS fact_risk_assessment (risk_id BIGSERIAL PRIMARY KEY, decision_id BIGINT, probability INT, impact INT);
CREATE TABLE IF NOT EXISTS fact_budget_impact (impact_id BIGSERIAL PRIMARY KEY, decision_id BIGINT, budget_variance NUMERIC(12,2));
CREATE TABLE IF NOT EXISTS fact_project_performance (performance_id BIGSERIAL PRIMARY KEY, project_id INT, roi NUMERIC(12,2));