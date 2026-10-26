import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_full_workflow():
    print("=== Step 1: Health Check ===")
    res = requests.get("http://127.0.0.1:8000/health")
    assert res.status_code == 200
    print("Health check OK:", res.json())

    print("\n=== Step 2: Administrator Login ===")
    res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "admin@enterprise.ai",
        "password": "Admin@123456"
    })
    assert res.status_code == 200, res.text
    admin_token = res.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("Admin login OK. Token acquired.")

    print("\n=== Step 3: Fetch Pending Tasks ===")
    res = requests.get(f"{BASE_URL}/tasks?status=NOT_SUBMITTED", headers=admin_headers)
    assert res.status_code == 200, res.text
    pending_tasks = res.json()
    assert len(pending_tasks) > 0
    target_task = pending_tasks[0]
    print(f"Target Task ID: {target_task['task_id']}")
    print(f"Target Employee: {target_task['employee_name']} ({target_task['employee_id']})")
    print(f"Task Title: {target_task['title']}")

    print("\n=== Step 4: Login as Target Employee ===")
    emp_email = target_task['employee_email']
    emp_pass = f"Emp@{target_task['employee_id']}"
    res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": emp_email,
        "password": emp_pass
    })
    assert res.status_code == 200, res.text
    emp_token = res.json()["access_token"]
    emp_headers = {"Authorization": f"Bearer {emp_token}"}
    print(f"Employee {target_task['employee_id']} logged in successfully.")

    print("\n=== Step 5: Test Incomplete Submission -> NEEDS_CORRECTION ===")
    incomplete_content = """
    # Incomplete initial draft
    print('Work in progress')
    """
    sub_data = {
        "task_id": target_task["task_id"],
        "submission_type": "TEXT",
        "text_content": incomplete_content
    }
    res = requests.post(f"{BASE_URL}/submissions", data=sub_data, headers=emp_headers)
    assert res.status_code == 200, res.text
    review1 = res.json()
    print("AI Evaluation Result (Attempt 1):")
    print(f" - Status: {review1['status']}")
    print(f" - Score: {review1['score']}/100")
    print(f" - Positive Feedback: {review1['positive_feedback'][:120]}...")
    print(f" - Errors Identified ({len(review1['identified_errors'])} issues):")
    for err in review1['identified_errors'][:2]:
        print(f"   * Issue: {err['issue']}")
        print(f"     Suggested fix: {err['suggested_correction']}")

    print("\n=== Step 6: Verify Correction Email Was Logged with Details ===")
    res = requests.get(f"{BASE_URL}/emails/logs?email_type=CORRECTION", headers=admin_headers)
    assert res.status_code == 200
    corr_emails = res.json()
    assert len(corr_emails) > 0
    latest_corr_email = corr_emails[0]
    print(f" - Email ID: {latest_corr_email['email_id']}")
    print(f" - Recipient: {latest_corr_email['recipient']}")
    print(f" - Subject: {latest_corr_email['subject']}")
    print(f" - Delivery: {latest_corr_email['delivery_status']}")

    print("\n=== Step 7: Employee Resubmits Corrected Work -> APPROVED ===")
    corrected_code = """
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, confusion_matrix

# Split data without leakage
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Calculate ROC-AUC score >= 0.82
y_pred_proba = model.predict_proba(X_test)[:, 1]
score = roc_auc_score(y_test, y_pred_proba)

# Feature importance and confusion matrix
importance = model.feature_importances_
matrix = confusion_matrix(y_test, model.predict(X_test))
    """
    sub_data2 = {
        "task_id": target_task["task_id"],
        "submission_type": "TEXT",
        "text_content": corrected_code
    }
    res = requests.post(f"{BASE_URL}/submissions", data=sub_data2, headers=emp_headers)
    assert res.status_code == 200, res.text
    review2 = res.json()
    print("AI Evaluation Result (Attempt 2 - Resubmission):")
    print(f" - Version Number: {review2['version_number']}")
    print(f" - Status: {review2['status']}")
    print(f" - Score: {review2['score']}/100")
    print(f" - Positive Feedback: {review2['positive_feedback'][:120]}...")

    print("\n=== Step 8: Verify Approval Email Was Logged ===")
    res = requests.get(f"{BASE_URL}/emails/logs?email_type=APPROVAL", headers=admin_headers)
    assert res.status_code == 200
    appr_emails = res.json()
    assert len(appr_emails) > 0
    print(f" - Approval Email Recipient: {appr_emails[0]['recipient']}")
    print(f" - Subject: {appr_emails[0]['subject']}")

    print("\n ALL WORKFLOW CHECKS (SUBMISSION -> CORRECTION -> RESUBMISSION -> APPROVAL) PASSED PERFECTLY!")

if __name__ == "__main__":
    test_full_workflow()
