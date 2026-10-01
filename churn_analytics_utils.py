"""
Behavioral Analytics Utilities for Customer Churn Prediction System
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_customer_segments(df):
    """Generate customer segments based on behavior"""
    segments = []
    
    for idx, row in df.iterrows():
        # Define segments based on tenure and churn status
        if row['tenure_months'] < 12:
            segment = 'New Customer'
        elif row['tenure_months'] < 24:
            segment = 'Growing Customer'
        elif row['tenure_months'] < 48:
            segment = 'Established Customer'
        else:
            segment = 'Loyal Customer'
        
        segments.append({
            'customer_id': row['customer_id'],
            'segment': segment,
            'tenure_months': row['tenure_months'],
            'churn': row['churn'],
            'monthly_charges': row['monthly_charges'],
            'satisfaction_score': row['satisfaction_score']
        })
    
    return pd.DataFrame(segments)

def generate_engagement_metrics(df):
    """Generate engagement metrics for customers"""
    metrics = []
    
    for idx, row in df.iterrows():
        # Calculate engagement score (0-100)
        engagement_score = (
            (row['usage_frequency'] / 30) * 30 +
            (1 - row['service_complaints'] / 5) * 30 +
            (1 - row['payment_delays'] / 3) * 20 +
            (row['satisfaction_score'] / 5) * 20
        )
        
        # Determine engagement level
        if engagement_score >= 75:
            level = 'High'
        elif engagement_score >= 50:
            level = 'Medium'
        else:
            level = 'Low'
        
        metrics.append({
            'customer_id': row['customer_id'],
            'engagement_score': engagement_score,
            'engagement_level': level,
            'usage_frequency': row['usage_frequency'],
            'support_interactions': row['customer_support_calls'],
            'churn_risk': 'High' if row['churn'] == 1 else 'Low'
        })
    
    return pd.DataFrame(metrics)

def generate_retention_insights(df, segments_df, metrics_df):
    """Generate retention insights and recommendations"""
    insights = []
    
    # Overall churn rate
    overall_churn_rate = df['churn'].mean() * 100
    
    # Churn by segment
    segment_churn = segments_df.groupby('segment')['churn'].agg(['sum', 'count'])
    segment_churn['rate'] = (segment_churn['sum'] / segment_churn['count'] * 100)
    
    # High-risk customers
    high_risk = metrics_df[metrics_df['engagement_level'] == 'Low']
    
    # Satisfaction analysis
    low_satisfaction = df[df['satisfaction_score'] < 2.5]
    
    insights.append({
        'metric': 'Overall Churn Rate',
        'value': f'{overall_churn_rate:.2f}%',
        'interpretation': 'Percentage of customers who discontinued service'
    })
    
    insights.append({
        'metric': 'High-Risk Customers',
        'value': len(high_risk),
        'interpretation': 'Customers with low engagement scores requiring immediate attention'
    })
    
    insights.append({
        'metric': 'Low Satisfaction Customers',
        'value': len(low_satisfaction),
        'interpretation': 'Customers with satisfaction scores below 2.5/5.0'
    })
    
    insights.append({
        'metric': 'New Customer Churn',
        'value': f'{segment_churn.loc["New Customer", "rate"]:.2f}%',
        'interpretation': 'Churn rate for customers with tenure < 12 months'
    })
    
    insights.append({
        'metric': 'Loyal Customer Retention',
        'value': f'{100 - segment_churn.loc["Loyal Customer", "rate"]:.2f}%',
        'interpretation': 'Retention rate for customers with tenure > 48 months'
    })
    
    return pd.DataFrame(insights)

def generate_intervention_recommendations(df, segments_df, metrics_df):
    """Generate intervention recommendations for at-risk customers"""
    recommendations = []
    
    # Identify at-risk customers
    at_risk = df[
        ((df['tenure_months'] < 12) & (df['satisfaction_score'] < 3)) |
        ((df['service_complaints'] > 2)) |
        ((df['payment_delays'] > 0) & (df['satisfaction_score'] < 3))
    ]
    
    for idx, customer in at_risk.iterrows():
        intervention = {
            'customer_id': customer['customer_id'],
            'risk_level': 'High' if customer['satisfaction_score'] < 2 else 'Medium',
            'primary_issue': None,
            'recommended_action': None,
            'priority': 'Urgent' if customer['satisfaction_score'] < 2 else 'High'
        }
        
        # Determine primary issue
        if customer['service_complaints'] > 2:
            intervention['primary_issue'] = 'Service Quality'
            intervention['recommended_action'] = 'Technical support review and service upgrade'
        elif customer['payment_delays'] > 0:
            intervention['primary_issue'] = 'Payment Issues'
            intervention['recommended_action'] = 'Payment plan adjustment and financial counseling'
        elif customer['satisfaction_score'] < 2.5:
            intervention['primary_issue'] = 'Low Satisfaction'
            intervention['recommended_action'] = 'Personalized outreach and retention offer'
        
        if intervention['primary_issue']:
            recommendations.append(intervention)
    
    return pd.DataFrame(recommendations)

def main():
    print("="*80)
    print("CUSTOMER CHURN ANALYTICS - UTILITIES")
    print("="*80)
    
    # Load the generated customer data
    print("\n[Step 1] Loading customer data...")
    df = pd.read_csv('/home/ubuntu/customer_churn_data.csv')
    print(f"✓ Loaded {len(df)} customer records")
    
    # Generate customer segments
    print("\n[Step 2] Generating customer segments...")
    segments_df = generate_customer_segments(df)
    segments_df.to_csv('/home/ubuntu/customer_segments.csv', index=False)
    print("✓ Customer segments saved")
    
    # Display segment distribution
    segment_dist = segments_df['segment'].value_counts()
    print("\nSegment Distribution:")
    for segment, count in segment_dist.items():
        print(f"  {segment}: {count} customers ({count/len(segments_df)*100:.1f}%)")
    
    # Generate engagement metrics
    print("\n[Step 3] Generating engagement metrics...")
    metrics_df = generate_engagement_metrics(df)
    metrics_df.to_csv('/home/ubuntu/engagement_metrics.csv', index=False)
    print("✓ Engagement metrics saved")
    
    # Display engagement distribution
    engagement_dist = metrics_df['engagement_level'].value_counts()
    print("\nEngagement Distribution:")
    for level, count in engagement_dist.items():
        print(f"  {level} Engagement: {count} customers ({count/len(metrics_df)*100:.1f}%)")
    
    # Generate retention insights
    print("\n[Step 4] Generating retention insights...")
    insights_df = generate_retention_insights(df, segments_df, metrics_df)
    insights_df.to_csv('/home/ubuntu/retention_insights.csv', index=False)
    print("✓ Retention insights saved")
    
    print("\nKey Insights:")
    for idx, row in insights_df.iterrows():
        print(f"  {row['metric']}: {row['value']}")
        print(f"    → {row['interpretation']}")
    
    # Generate intervention recommendations
    print("\n[Step 5] Generating intervention recommendations...")
    recommendations_df = generate_intervention_recommendations(df, segments_df, metrics_df)
    recommendations_df.to_csv('/home/ubuntu/intervention_recommendations.csv', index=False)
    print(f"✓ Intervention recommendations saved ({len(recommendations_df)} at-risk customers)")
    
    # Display recommendations summary
    if len(recommendations_df) > 0:
        print("\nIntervention Summary:")
        print(f"  High Priority: {len(recommendations_df[recommendations_df['priority'] == 'High'])} customers")
        print(f"  Urgent: {len(recommendations_df[recommendations_df['priority'] == 'Urgent'])} customers")
        
        print("\nPrimary Issues:")
        issue_dist = recommendations_df['primary_issue'].value_counts()
        for issue, count in issue_dist.items():
            print(f"  {issue}: {count} customers")
    
    print("\n" + "="*80)
    print("ANALYTICS GENERATION COMPLETED")
    print("="*80)

if __name__ == "__main__":
    main()
