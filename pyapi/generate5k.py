import pandas as pd
import numpy as np
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)

def generate_synthetic_data(n_samples=5000):
    """
    Generate synthetic mental wellness data with realistic correlations
    """
    data = []
    
    for i in range(n_samples):
        user_id = f"U{str(i+1).zfill(4)}"
        
        # Basic demographics
        age = int(np.random.normal(35, 12))
        age = np.clip(age, 18, 70)
        
        gender = np.random.choice(['Male', 'Female'], p=[0.48, 0.48])
        
        occupation = np.random.choice(
            ['Employed', 'Student', 'Self-employed', 'Unemployed', 'Retired'],
            p=[0.35, 0.35, 0.15, 0.10, 0.05]
        )
        
        # Work mode depends on occupation
        if occupation in ['Employed', 'Self-employed']:
            work_mode = np.random.choice(['Remote', 'Hybrid', 'Office'], p=[0.35, 0.30, 0.35])
        elif occupation == 'Student':
            work_mode = np.random.choice(['Remote', 'Hybrid', 'Office'], p=[0.25, 0.35, 0.40])
        else:
            work_mode = 'N/A'
        
        # Screen time modeling with realistic correlations
        # Work screen hours depend on occupation and work mode
        if occupation == 'Employed':
            if work_mode == 'Remote':
                work_screen_hours = np.random.normal(7.5, 1.5)
            elif work_mode == 'Hybrid':
                work_screen_hours = np.random.normal(6, 1.5)
            else:  # Office
                work_screen_hours = np.random.normal(5.5, 1.5)
        elif occupation == 'Self-employed':
            work_screen_hours = np.random.normal(6.5, 2)
        elif occupation == 'Student':
            work_screen_hours = np.random.normal(4.5, 1.5)
        else:
            work_screen_hours = np.random.normal(1, 0.5)
        
        work_screen_hours = np.clip(work_screen_hours, 0, 16)
        
        # Leisure screen hours - younger people tend to have more
        age_factor = (70 - age) / 52  # Normalized age effect
        leisure_screen_hours = np.random.normal(3 + age_factor, 1.5)
        leisure_screen_hours = np.clip(leisure_screen_hours, 0.5, 10)
        
        # Total screen time
        screen_time_hours = work_screen_hours + leisure_screen_hours
        
        # Sleep hours - inversely related to screen time and stress
        base_sleep = 7.5 - (screen_time_hours - 8) * 0.15
        sleep_hours = np.random.normal(base_sleep, 0.8)
        sleep_hours = np.clip(sleep_hours, 4, 10)
        
        # Sleep quality - related to sleep hours and screen time
        if sleep_hours >= 7 and screen_time_hours < 10:
            sleep_quality = np.random.choice([3, 4, 5], p=[0.3, 0.4, 0.3])
        elif sleep_hours >= 6:
            sleep_quality = np.random.choice([2, 3, 4], p=[0.3, 0.5, 0.2])
        else:
            sleep_quality = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
        
        # Stress level - influenced by work hours, sleep, and occupation
        stress_base = 5
        stress_base += (work_screen_hours - 6) * 0.4  # More work = more stress
        stress_base += (7 - sleep_hours) * 0.5  # Less sleep = more stress
        stress_base += np.random.normal(0, 1.5)
        
        if occupation == 'Unemployed':
            stress_base += 1.5
        elif occupation == 'Retired':
            stress_base -= 2
        
        stress_level = np.clip(stress_base, 0, 10)
        
        # Exercise - inversely related to screen time and work hours
        exercise_base = 180 - (screen_time_hours - 8) * 15
        exercise_minutes = np.random.normal(exercise_base, 60)
        exercise_minutes = np.clip(exercise_minutes, 0, 600)
        
        # Social hours - less screen time and lower stress = more social time
        social_base = 12 - (screen_time_hours - 8) * 0.3 - stress_level * 0.3
        social_hours = np.random.normal(social_base, 3)
        social_hours = np.clip(social_hours, 0, 40)
        
        # Productivity - function of sleep, stress, exercise
        productivity_base = 50
        productivity_base += (sleep_hours - 7) * 5  # Good sleep improves productivity
        productivity_base -= (stress_level - 5) * 3  # High stress reduces productivity
        productivity_base += (exercise_minutes / 60) * 2  # Exercise helps
        productivity_base += (sleep_quality - 3) * 5
        productivity_base += np.random.normal(0, 10)
        
        productivity = np.clip(productivity_base, 0, 100)
        
        # Mental Wellness Index - comprehensive calculation
        wellness_base = 50
        
        # Positive factors
        wellness_base += (sleep_hours - 7) * 4
        wellness_base += (sleep_quality - 3) * 6
        wellness_base += (exercise_minutes / 60) * 1.5
        wellness_base += (social_hours - 10) * 1
        wellness_base += (productivity - 50) * 0.2
        
        # Negative factors
        wellness_base -= (stress_level - 5) * 4
        wellness_base -= max(0, (screen_time_hours - 10)) * 2
        wellness_base -= max(0, (work_screen_hours - 8)) * 1.5
        
        # Age effect (U-shaped: mid-life crisis)
        age_wellness_effect = -((age - 45) ** 2) / 200
        wellness_base += age_wellness_effect
        
        # Add some random variation
        wellness_base += np.random.normal(0, 5)
        
        mental_wellness_index = np.clip(wellness_base, 0, 100)
        
        # Create row
        row = {
            'user_id': user_id,
            'age': age,
            'gender': gender,
            'occupation': occupation,
            'work_mode': work_mode,
            'screen_time_hours': round(screen_time_hours, 2),
            'work_screen_hours': round(work_screen_hours, 2),
            'leisure_screen_hours': round(leisure_screen_hours, 2),
            'sleep_hours': round(sleep_hours, 2),
            'sleep_quality_1_5': sleep_quality,
            'stress_level_0_10': round(stress_level, 1),
            'productivity_0_100': round(productivity, 1),
            'exercise_minutes_per_week': round(exercise_minutes, 0),
            'social_hours_per_week': round(social_hours, 1),
            'mental_wellness_index_0_100': round(mental_wellness_index, 1)
        }
        
        data.append(row)
    
    return pd.DataFrame(data)

# Generate the dataset
print("🔄 Generating synthetic mental wellness dataset...")
df = generate_synthetic_data(n_samples=5000)

# Save to CSV
filename = "synthetic_mental_wellness_5000.csv"
df.to_csv(filename, index=False)

print(f"✅ Dataset generated successfully!")
print(f"📊 Total samples: {len(df)}")
print(f"💾 Saved to: {filename}")
print("\n📈 Dataset Statistics:")
print(df.describe())

print("\n🔍 Sample data (first 5 rows):")
print(df.head())

print("\n📊 Correlation with Mental Wellness Index:")
correlations = df.select_dtypes(include=[np.number]).corr()['mental_wellness_index_0_100'].sort_values(ascending=False)
print(correlations)