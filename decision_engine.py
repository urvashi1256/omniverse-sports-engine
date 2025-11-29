# decision_engine.py
def is_underdog(match_id, scoring_team):
    # simple fake rule for demo: treat anything with 'underdog' in name as underdog
    return "underdog" in scoring_team.lower()
