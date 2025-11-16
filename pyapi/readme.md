# Mental Wellness Index Prediction Using ANN

## Project Overview

This project predicts the **Mental Wellness Index** (0–100) of individuals based on lifestyle and demographic factors using an **Artificial Neural Network (ANN)**.  
The ANN performs **regression**, outputting a continuous score for mental wellness, which is clamped between 0 and 100.

---

## Dataset

The dataset `ScreenTime vs MentalWellness.csv` contains:

- **Numerical Features**:
  - `age`, `screen_time_hours`, `work_screen_hours`, `leisure_screen_hours`
  - `sleep_hours`, `sleep_quality_1_5`, `stress_level_0_10`
  - `productivity_0_100`, `exercise_minutes_per_week`, `social_hours_per_week`
- **Categorical Features**:
  - `gender`, `occupation`, `work_mode`
- **Target**:
  - `mental_wellness_index_0_100` (continuous value between 0 and 100)

Missing values are handled via **median imputation** for numerical features and `'Unknown'` for categorical features. Outliers are clipped using the **IQR method**.

---

## Data Preprocessing

1. **One-Hot Encoding** of categorical features.
2. **Feature Engineering**:
   - `work_leisure_screen_ratio` = work_screen_hours / leisure_screen_hours
   - `total_screen_hours` = work_screen_hours + leisure_screen_hours
3. **Scaling** numerical features with `StandardScaler`.
4. Train-validation-test split: **70% train, 15% validation, 15% test**.

---

## ANN Architecture

- Input layer: number of features
- Hidden layer 1: 64 neurons, ReLU activation
- Dropout: 0.2
- Hidden layer 2: 32 neurons, ReLU activation
- Dropout: 0.2
- Output layer: 1 neuron, linear activation (regression)

**Optimizer**: Adam (learning rate = 0.001)  
**Loss function**: Mean Squared Error (MSE)  
**Metrics**: Mean Absolute Error (MAE)

---

## Training

- Epochs: 100
- Batch size: 16
- Validation monitored to avoid overfitting

**Test performance**:

- MAE ≈ 5
- MSE ≈ 36

---

## Prediction Example

```python
new_user = {
    'age': 30,
    'screen_time_hours': 5,
    'work_screen_hours': 2,
    'leisure_screen_hours': 3,
    'sleep_hours': 8,
    'sleep_quality_1_5': 5,
    'stress_level_0_10': 1,
    'productivity_0_100': 95,
    'exercise_minutes_per_week': 120,
    'social_hours_per_week': 10,
    'gender': 'Female',
    'occupation': 'Professional',
    'work_mode': 'Hybrid'
}

prediction = predict_new_user(model, scaler, X.columns, new_user, num_cols)
prediction = max(0, min(100, prediction))
print(f"Predicted Mental Wellness Index: {prediction:.2f}")
```
