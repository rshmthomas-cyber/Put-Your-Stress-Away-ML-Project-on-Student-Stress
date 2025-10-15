from django import forms

SCALE_1_5 = [(i, str(i)) for i in range(1, 6)]

GENDER_CHOICES = [
    (0, 'Male'),
    (1, 'Female'),
]

class StressForm(forms.Form):
    gender = forms.TypedChoiceField(label='Gender', choices=GENDER_CHOICES, coerce=int)
    age = forms.IntegerField(label='Age', min_value=10, max_value=100, initial=20)

    # all following fields are 1-5 scale (1 lowest, 5 highest)
    stress_recent = forms.TypedChoiceField(label='Have you recently experienced stress in your life? (1-5)', choices=SCALE_1_5, coerce=int)
    rapid_heartbeat = forms.TypedChoiceField(label='Have you noticed a rapid heartbeat or palpitations? (1-5)', choices=SCALE_1_5, coerce=int)
    anxiety = forms.TypedChoiceField(label='Have you been dealing with anxiety or tension recently? (1-5)', choices=SCALE_1_5, coerce=int)
    sleep_problems = forms.TypedChoiceField(label='Do you face any sleep problems or difficulties falling asleep? (1-5)', choices=SCALE_1_5, coerce=int)
    difficulty_concentrate = forms.TypedChoiceField(label='Are you finding difficulty to concentrate? (1-5)', choices=SCALE_1_5, coerce=int)
    headaches = forms.TypedChoiceField(label='Have you been getting headaches more often than usual? (1-5)', choices=SCALE_1_5, coerce=int)
    irritated = forms.TypedChoiceField(label='Do you get irritated easily? (1-5)', choices=SCALE_1_5, coerce=int)
    trouble_academic_concentration = forms.TypedChoiceField(label='Do you have trouble concentrating on your academic tasks? (1-5)', choices=SCALE_1_5, coerce=int)
    sadness_low_mood = forms.TypedChoiceField(label='Have you been feeling sadness or low mood? (1-5)', choices=SCALE_1_5, coerce=int)
    illness_health_issues = forms.TypedChoiceField(label='Have you been experiencing any illness or health issues? (1-5)', choices=SCALE_1_5, coerce=int)
    lonely_isolated = forms.TypedChoiceField(label='Do you often feel lonely or isolated? (1-5)', choices=SCALE_1_5, coerce=int)
    overwhelmed_workload = forms.TypedChoiceField(label='Do you feel overwhelmed with your academic workload? (1-5)', choices=SCALE_1_5, coerce=int)
    competition_peers = forms.TypedChoiceField(label='Are you in competition with your peers, and does it affect you? (1-5)', choices=SCALE_1_5, coerce=int)
    relationship_stress = forms.TypedChoiceField(label='Do you find that your relationship often causes you stress? (1-5)', choices=SCALE_1_5, coerce=int)
    difficulties_with_professors = forms.TypedChoiceField(label='Are you facing any difficulties with your professors or instructors? (1-5)', choices=SCALE_1_5, coerce=int)
    unpleasant_work_environment = forms.TypedChoiceField(label='Is your working environment unpleasant or stressful? (1-5)', choices=SCALE_1_5, coerce=int)
    no_time_relaxation = forms.TypedChoiceField(label='Do you struggle to find time for relaxation and leisure activities? (1-5)', choices=SCALE_1_5, coerce=int)
    hostel_home_difficulties = forms.TypedChoiceField(label='Is your hostel or home environment causing you difficulties? (1-5)', choices=SCALE_1_5, coerce=int)
    lack_confidence_performance = forms.TypedChoiceField(label='Do you lack confidence in your academic performance? (1-5)', choices=SCALE_1_5, coerce=int)
    lack_confidence_subject_choice = forms.TypedChoiceField(label='Do you lack confidence in your choice of academic subjects? (1-5)', choices=SCALE_1_5, coerce=int)
    conflict_academic_extracurricular = forms.TypedChoiceField(label='Academic and extracurricular activities conflicting for you? (1-5)', choices=SCALE_1_5, coerce=int)
    attend_classes_regularly = forms.TypedChoiceField(label='Do you attend classes regularly? (1-5)', choices=SCALE_1_5, coerce=int)
    gained_lost_weight = forms.TypedChoiceField(label='Have you gained/lost weight? (1-5)', choices=SCALE_1_5, coerce=int)
