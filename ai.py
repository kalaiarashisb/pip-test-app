import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/student-mat.csv'
data = pd.read_csv(url, sep=';')

# Display first few rows
print(data.head())

# Target: Final grade G3 (use binary classification: pass/fail)
data['pass'] = data['G3'] >= 10  # Pass if G3 >= 10
data['pass'] = data['pass'].astype(int)

# Select relevant features
features = ['studytime', 'failures', 'absences']
X = data[features]
y = data['pass']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Plot feature importance
importance = model.feature_importances_
sns.barplot(x=features, y=importance)
plt.title("Feature Importance")
plt.show()
