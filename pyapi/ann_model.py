# ann_model.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import joblib

# -----------------------------
# 0️⃣ Load and preprocess dataset
# -----------------------------
df = pd.read_csv("synthetic_mental_wellness_5000.csv")
df = df.drop_duplicates()
if 'Unnamed: 15' in df.columns:
    df = df.drop(columns=['Unnamed: 15'])

num_cols = [
    'age', 'screen_time_hours', 'work_screen_hours', 'leisure_screen_hours',
    'sleep_hours', 'sleep_quality_1_5', 'stress_level_0_10',
    'productivity_0_100', 'exercise_minutes_per_week', 'social_hours_per_week'
]
target_col = 'mental_wellness_index_0_100'
cat_cols = ['gender', 'occupation', 'work_mode']

# Fill missing values
df[num_cols + [target_col]] = df[num_cols + [target_col]].fillna(df[num_cols + [target_col]].median())
df[cat_cols] = df[cat_cols].fillna('Unknown')

# One-Hot Encoding
df_encoded = pd.get_dummies(df, columns=cat_cols, drop_first=True)

# Feature engineering
df_encoded['work_leisure_screen_ratio'] = df_encoded['work_screen_hours'] / (df_encoded['leisure_screen_hours'] + 1e-5)
df_encoded['total_screen_hours'] = df_encoded['work_screen_hours'] + df_encoded['leisure_screen_hours']

new_num_cols = num_cols + ['work_leisure_screen_ratio', 'total_screen_hours']

# Clip outliers
for col in new_num_cols:
    Q1 = df_encoded[col].quantile(0.25)
    Q3 = df_encoded[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5*IQR
    upper = Q3 + 1.5*IQR
    df_encoded[col] = df_encoded[col].clip(lower, upper)

# Split features and target
X = df_encoded.drop([target_col, 'user_id'], axis=1)
y = df_encoded[target_col]

# Scaling numerical features
scaler = StandardScaler()
X[new_num_cols] = scaler.fit_transform(X[new_num_cols])

# Save scaler for later
joblib.dump(scaler, "scaler.joblib")

# Train / val / test split
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# -----------------------------
# 1️⃣ Build ANN model
# -----------------------------
model = Sequential([
    Input(shape=(X_train.shape[1],)),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(1, activation='linear')  # Regression
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
print("✅ Model compiled")
model.summary()

# -----------------------------
# 2️⃣ Train the model
# -----------------------------
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=100,
    batch_size=16,
    verbose=1
)

# -----------------------------
# 3️⃣ Evaluate on test set
# -----------------------------
loss, mae = model.evaluate(X_test, y_test, verbose=0)

# Calculate R² Score
y_pred = model.predict(X_test, verbose=0)
r2 = r2_score(y_test, y_pred)

print("\n" + "="*50)
print("📊 MODEL EVALUATION METRICS")
print("="*50)
print(f"🎯 MAE (Mean Absolute Error): {mae:.3f}")
print(f"💥 MSE (Mean Squared Error): {loss:.3f}")
print(f"📈 R² Score: {r2:.4f}")
print("="*50)

# Additional predictions for validation set
y_val_pred = model.predict(X_val, verbose=0)
r2_val = r2_score(y_val, y_val_pred)

print(f"\n🔍 Validation R² Score: {r2_val:.4f}")

# -----------------------------
# 4️⃣ Save the model
# -----------------------------
model.save("mental_wellness_model.keras")  # ✅ Use .keras extension
print("\n💾 Model saved as 'mental_wellness_model.keras'")

# -----------------------------
# 5️⃣ Plot training history
# -----------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Loss plot
axes[0].plot(history.history['loss'], label='Train Loss', linewidth=2)
axes[0].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
axes[0].set_xlabel('Epochs', fontsize=12)
axes[0].set_ylabel('MSE Loss', fontsize=12)
axes[0].set_title('Model Loss Over Epochs', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# MAE plot
axes[1].plot(history.history['mae'], label='Train MAE', linewidth=2)
axes[1].plot(history.history['val_mae'], label='Validation MAE', linewidth=2)
axes[1].set_xlabel('Epochs', fontsize=12)
axes[1].set_ylabel('MAE', fontsize=12)
axes[1].set_title('Model MAE Over Epochs', fontsize=14, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
print("📊 Training plots saved as 'training_history.png'")
plt.show()

# -----------------------------
# 6️⃣ Prediction vs Actual Plot
# -----------------------------
plt.figure(figsize=(8, 8))
plt.scatter(y_test, y_pred, alpha=0.5, s=20)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Perfect Prediction')
plt.xlabel('Actual Mental Wellness Index', fontsize=12)
plt.ylabel('Predicted Mental Wellness Index', fontsize=12)
plt.title(f'Predictions vs Actual (R² = {r2:.4f})', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('predictions_vs_actual.png', dpi=300, bbox_inches='tight')
print("📊 Prediction plot saved as 'predictions_vs_actual.png'")
plt.show()

print("\n✅ Training complete!")