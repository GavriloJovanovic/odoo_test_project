
# Test Applicant Module - Documentation

## Overview
This document is intended for **developers** who need to understand how the module works **at a high level**.

---

## **Module Features**
- Implements **applicant tracking** with a model `test.model`.
- Provides **CRUD operations** with state transitions (`draft → confirmed → done`).
- Automates workflow using **cron jobs**.
- Implements a **custom "Login As" functionality**.

---

## **Technical Components**

### **1. Model (`test_model_api.py`)**
- Defines `test.model` with:
  - **Fields:** `name`, `description`, `reference_code`, `state`, `confirmed_at`.
  - **Methods:**
    - `_generate_reference_code()`: Ensures unique codes.
    - `action_confirm()`: Marks records as confirmed.
    - `_auto_mark_done()`: Automatically marks records as **done after 30 minutes**.

### **2. Security (`security.xml`, `ir.model.access.csv`)**
- Admins can **manage** records.
- Users can only **view** records.
- **Prevents unauthorized actions.**

### **3. Views (`test_model_views.xml`)**
- **Tree view:** Shows a list of records.
- **Form view:** Allows editing and state changes.
- **"Confirm" button:** Moves to the confirmed state.
- **"Set to Done" button:** Moves to the done state.

### **4. Login As Feature (`login_as.py`, `res_users_views.xml`)**
- Adds a **"Login As"** button in user forms.
- Restricts **superuser login (ID=2)**.
- Uses `request.session.uid` to switch users.
- Only **admins** can use this feature.

### **5. Automation (`cron.xml`)**

Where we define two cron jobs:

1. A cron job runs every **5 minutes** to check for confirmed records.
   - Calls `_auto_mark_done()` to mark them as **done**.

2. A cron job that runs every **day** to reset `reference_code`
   * Calls `_reset_reference_code()` to reset code from `TEST-0001`.

### **6. Sequences (`sequence.xml`)**
- Generates `reference_code` values in format: `TEST-00001`.

---

## **How to Extend This Module**
- **Add new fields** in `test_model_api.py`.
- **Modify UI** in `test_model_views.xml`.
- **Change permissions** in `security.xml`.
- **Extend logic** in `login_as.py`.

