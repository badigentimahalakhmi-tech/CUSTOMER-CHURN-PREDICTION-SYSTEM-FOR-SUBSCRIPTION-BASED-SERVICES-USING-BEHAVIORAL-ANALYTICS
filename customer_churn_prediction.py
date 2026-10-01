"""
Customer Churn Prediction System for Subscription-Based Services
Using Behavioral Analytics and Machine Learning
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, confusion_matrix, roc_auc_score, roc_curve, auc)
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def generate_churn_dataset(n_samples=1000, random_state=42):
    """Generate synthetic customer churn dataset"""
    np.random.seed(random_state)
    
    data = {
        'customer_id': range(1, n_samples + 1),
        'age': np.random.randint(18, 75, n_samples),
        'tenure_months': np.random.randint(1, 60, n_samples),
        'monthly_charges': np.random.uniform(20, 150, n_samples),
        'total_charges': np.random.uniform(100, 5000, n_samples),
        'usage_frequency': np.random.randint(1, 30, n_samples),
        'service_complaints': np.random.randint(0, 5, n_samples),
        'payment_delays': np.random.randint(0, 3, n_samples),
        'contract_length': np.random.choice(['month-to-month', 'one_year', 'two_year'], n_samples),
        'internet_service': np.random.choice(['DSL', 'Fiber', 'No'], n_samples),
        'customer_support_calls': np.random.randint(0, 10, n_samples),
        'satisfaction_score': np.random.uniform(1, 5, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Generate churn based on features (realistic patterns)
    churn_probability = (
        0.02 * (df['tenure_months'] < 12) +
        0.03 * (df['service_complaints'] > 2) +
        0.02 * (df['payment_delays'] > 0) +
        0.01 * (df['monthly_charges'] > 100) +
        0.02 * (df['satisfaction_score'] < 2.5) +
        0.01 * (df['customer_support_calls'] > 5)
    )
    
    df['churn'] = (np.random.random(n_samples) < churn_probability).astype(int)
    
    return df

def preprocess_data(df):
    """Preprocess the customer data"""
    df_processed = df.copy()
    
    # Encode categorical variables
    df_processed['contract_length_encoded'] = pd.factorize(df_processed['contract_length'])[0]
    df_processed['internet_service_encoded'] = pd.factorize(df_processed['internet_service'])[0]
    
    # Drop original categorical columns
    df_processed = df_processed.drop(['customer_id', 'contract_length', 'internet_service'], axis=1)
    
    return df_processed

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple classification models"""
    models = {}
    predictions = {}
    
    # Logistic Regression
    print("Training Logistic Regression...")
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train, y_train)
    models['Logistic Regression'] = lr
    predictions['Logistic Regression'] = lr.predict(X_test)
    
    # Random Forest
    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    models['Random Forest'] = rf
    predictions['Random Forest'] = rf.predict(X_test)
    
    # Gradient Boosting
    print("Training Gradient Boosting...")
    gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
    gb.fit(X_train, y_train)
    models['Gradient Boosting'] = gb
    predictions['Gradient Boosting'] = gb.predict(X_test)
    
    return models, predictions

def evaluate_models(models, predictions, X_test, y_test):
    """Evaluate all models and return metrics"""
    results = []
    
    for model_name, y_pred in predictions.items():
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred)
        
        results.append({
            'Model': model_name,
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1,
            'ROC-AUC': roc_auc
        })
        
        print(f"\n{model_name} Performance:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        print(f"  ROC-AUC:   {roc_auc:.4f}")
    
    return pd.DataFrame(results)

def plot_churn_distribution(df):
    """Plot churn distribution"""
    fig, ax = plt.subplots(figsize=(10, 6))
    churn_counts = df['churn'].value_counts()
    colors = ['#2ecc71', '#e74c3c']
    ax.bar(['No Churn', 'Churn'], churn_counts.values, color=colors, edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Number of Customers', fontsize=12, fontweight='bold')
    ax.set_title('Customer Churn Distribution', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    for i, v in enumerate(churn_counts.values):
        ax.text(i, v + 10, str(v), ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/churn_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_feature_importance(models):
    """Plot feature importance from Random Forest"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    rf_model = models['Random Forest']
    feature_names = ['Age', 'Tenure', 'Monthly Charges', 'Total Charges', 'Usage Freq',
                     'Complaints', 'Payment Delays', 'Contract Type', 'Internet Service',
                     'Support Calls', 'Satisfaction']
    importances = rf_model.feature_importances_
    
    indices = np.argsort(importances)[::-1][:11]
    
    ax.barh(range(len(indices)), importances[indices], color='#3498db', edgecolor='black', linewidth=1.5)
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels([feature_names[i] for i in indices])
    ax.set_xlabel('Importance Score', fontsize=12, fontweight='bold')
    ax.set_title('Feature Importance Analysis (Random Forest)', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_model_comparison(results_df):
    """Plot model performance comparison"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(len(results_df))
    width = 0.2
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    colors_list = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    
    for i, metric in enumerate(metrics):
        ax.bar(x + i*width, results_df[metric], width, label=metric, 
               color=colors_list[i], edgecolor='black', linewidth=1.5)
    
    ax.set_xlabel('Model', fontsize=12, fontweight='bold')
    ax.set_ylabel('Score', fontsize=12, fontweight='bold')
    ax.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(results_df['Model'])
    ax.legend(loc='lower right')
    ax.set_ylim([0, 1.1])
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_confusion_matrices(models, predictions, y_test):
    """Plot confusion matrices for all models"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    for idx, (model_name, y_pred) in enumerate(predictions.items()):
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                    cbar=False, annot_kws={'fontsize': 12, 'fontweight': 'bold'})
        axes[idx].set_title(f'{model_name}', fontsize=12, fontweight='bold')
        axes[idx].set_ylabel('True Label', fontsize=10)
        axes[idx].set_xlabel('Predicted Label', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/confusion_matrices.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_roc_curves(models, X_test, y_test):
    """Plot ROC curves for all models"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    
    for idx, (model_name, model) in enumerate(models.items()):
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        ax.plot(fpr, tpr, color=colors[idx], lw=2.5, 
                label=f'{model_name} (AUC = {roc_auc:.3f})')
    
    ax.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Classifier')
    ax.set_xlabel('False Positive Rate', fontsize=12, fontweight='bold')
    ax.set_ylabel('True Positive Rate', fontsize=12, fontweight='bold')
    ax.set_title('ROC Curves - Model Comparison', fontsize=14, fontweight='bold')
    ax.legend(loc='lower right', fontsize=11)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/roc_curves.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_tenure_churn_analysis(df):
    """Plot churn rate by tenure"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    tenure_bins = [0, 12, 24, 36, 48, 60]
    df['tenure_group'] = pd.cut(df['tenure_months'], bins=tenure_bins)
    
    churn_by_tenure = df.groupby('tenure_group')['churn'].agg(['sum', 'count'])
    churn_by_tenure['rate'] = (churn_by_tenure['sum'] / churn_by_tenure['count'] * 100)
    
    tenure_labels = ['0-12 mo', '12-24 mo', '24-36 mo', '36-48 mo', '48-60 mo']
    
    ax.bar(tenure_labels, churn_by_tenure['rate'], color='#e74c3c', edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Churn Rate (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Tenure Group', fontsize=12, fontweight='bold')
    ax.set_title('Customer Churn Rate by Tenure', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    for i, v in enumerate(churn_by_tenure['rate']):
        ax.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/tenure_churn_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("="*80)
    print("CUSTOMER CHURN PREDICTION SYSTEM")
    print("="*80)
    
    # Generate dataset
    print("\n[Step 1] Generating customer churn dataset...")
    df = generate_churn_dataset(n_samples=1000)
    print(f"✓ Dataset generated: {df.shape[0]} customers, {df.shape[1]} features")
    
    # Preprocess data
    print("\n[Step 2] Preprocessing data...")
    df_processed = preprocess_data(df)
    
    # Separate features and target
    X = df_processed.drop('churn', axis=1)
    y = df_processed['churn']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"✓ Data split: {X_train_scaled.shape[0]} training, {X_test_scaled.shape[0]} testing")
    
    # Train models
    print("\n[Step 3] Training machine learning models...")
    models, predictions = train_models(X_train_scaled, X_test_scaled, y_train, y_test)
    
    # Evaluate models
    print("\n[Step 4] Evaluating models...")
    results_df = evaluate_models(models, predictions, X_test_scaled, y_test)
    results_df.to_csv('/home/ubuntu/model_performance.csv', index=False)
    print("✓ Performance metrics saved")
    
    # Generate visualizations
    print("\n[Step 5] Generating visualizations...")
    plot_churn_distribution(df)
    print("✓ Churn distribution plot saved")
    
    plot_feature_importance(models)
    print("✓ Feature importance plot saved")
    
    plot_model_comparison(results_df)
    print("✓ Model comparison plot saved")
    
    plot_confusion_matrices(models, predictions, y_test)
    print("✓ Confusion matrices plot saved")
    
    plot_roc_curves(models, X_test_scaled, y_test)
    print("✓ ROC curves plot saved")
    
    plot_tenure_churn_analysis(df)
    print("✓ Tenure churn analysis plot saved")
    
    # Save dataset
    df.to_csv('/home/ubuntu/customer_churn_data.csv', index=False)
    print("✓ Customer dataset saved")
    
    # Save processed data
    df_processed.to_csv('/home/ubuntu/customer_churn_processed.csv', index=False)
    print("✓ Processed dataset saved")
    
    print("\n" + "="*80)
    print("SYSTEM ANALYSIS COMPLETED")
    print("="*80)

if __name__ == "__main__":
    main()
