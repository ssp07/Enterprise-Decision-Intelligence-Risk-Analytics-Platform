CREATE INDEX IF NOT EXISTS idx_decision_date ON fact_decision(decision_date);
CREATE INDEX IF NOT EXISTS idx_decision_project ON fact_decision(project_id);
CREATE INDEX IF NOT EXISTS idx_outcome_decision ON fact_decision_outcome(decision_id);
CREATE INDEX IF NOT EXISTS idx_risk_decision ON fact_risk_assessment(decision_id);