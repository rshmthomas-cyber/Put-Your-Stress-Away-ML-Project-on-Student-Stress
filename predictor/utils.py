import numpy as np

FEATURE_ORDER = [
    'gender','age','stress_recent','rapid_heartbeat','anxiety','sleep_problems','difficulty_concentrate',
    'headaches','irritated','trouble_academic_concentration','sadness_low_mood','illness_health_issues',
    'lonely_isolated','overwhelmed_workload','competition_peers','relationship_stress','difficulties_with_professors',
    'unpleasant_work_environment','no_time_relaxation','hostel_home_difficulties','lack_confidence_performance',
    'lack_confidence_subject_choice','conflict_academic_extracurricular','attend_classes_regularly','gained_lost_weight',
]

def build_feature_vector(cleaned_data: dict):
    values = []
    for key in FEATURE_ORDER:
        if key not in cleaned_data:
            raise ValueError(f"Missing feature: {key}")
        val = cleaned_data.get(key)
        # validate scales
        if key == 'age':
            # allow int age as-is
            if not (10 <= int(val) <= 100):
                raise ValueError("Age out of range")
            values.append(float(val))
            continue
        if key == 'gender':
            # expect 0/1/2 (adjust if your training used a different mapping)
            values.append(float(val))
            continue
        # all other features expected 1-5
        v = int(val)
        if not (1 <= v <= 5):
            raise ValueError(f"Feature {key} must be 1-5, got {v}")
        values.append(float(v))
    return np.array(values).reshape(1, -1)

