# KPIs

TOTAL_DECISIONS = """
SELECT COUNT(*) total
FROM fact_decision;
"""

TOTAL_OUTCOMES = """
SELECT COUNT(*) total
FROM fact_decision_outcome;
"""

TOTAL_RISKS = """
SELECT COUNT(*) total
FROM fact_risk_assessment;
"""

AVG_COST = """
SELECT ROUND(AVG(estimated_cost),2) avg_cost
FROM fact_decision;
"""

AVG_SUCCESS = """
SELECT ROUND(AVG(success_rating),2) avg_success
FROM fact_decision_outcome;
"""

HIGH_RISK_COUNT = """
SELECT COUNT(*) risky
FROM fact_risk_assessment
WHERE impact >= 8;
"""

# Charts

DECISIONS_BY_MONTH = """
SELECT
DATE_TRUNC('month', decision_date) AS month,
COUNT(*) AS decisions
FROM fact_decision
GROUP BY month
ORDER BY month;
"""

COST_DISTRIBUTION = """
SELECT estimated_cost
FROM fact_decision;
"""

RISK_DISTRIBUTION = """
SELECT
impact,
COUNT(*) cnt
FROM fact_risk_assessment
GROUP BY impact
ORDER BY impact;
"""

SUCCESS_DISTRIBUTION = """
SELECT
success_rating,
COUNT(*) cnt
FROM fact_decision_outcome
GROUP BY success_rating
ORDER BY success_rating;
"""

TOP_10_EXPENSIVE = """
SELECT
decision_id,
estimated_cost
FROM fact_decision
ORDER BY estimated_cost DESC
LIMIT 10;
"""

ROI_ANALYSIS = """
SELECT
decision_id,
actual_benefit,
actual_cost,
(actual_benefit - actual_cost) profit
FROM fact_decision_outcome
ORDER BY profit DESC
LIMIT 50;
"""