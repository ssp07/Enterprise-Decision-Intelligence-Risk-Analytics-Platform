ALTER TABLE fact_decision_outcome DROP CONSTRAINT IF EXISTS chk_rating;
ALTER TABLE fact_decision_outcome ADD CONSTRAINT chk_rating CHECK(success_rating BETWEEN 1 AND 10);
ALTER TABLE fact_risk_assessment DROP CONSTRAINT IF EXISTS chk_probability;
ALTER TABLE fact_risk_assessment ADD CONSTRAINT chk_probability CHECK(probability BETWEEN 1 AND 100);
ALTER TABLE fact_risk_assessment DROP CONSTRAINT IF EXISTS chk_impact;
ALTER TABLE fact_risk_assessment ADD CONSTRAINT chk_impact CHECK(impact BETWEEN 1 AND 10);