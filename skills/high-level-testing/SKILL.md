---
name: high-level-testing
description: Advanced vulnerability analysis framework focusing on Business Logic, Access Control, and Session Management flaws beyond automated scanning. Use for complex web application assessments.
---

# High-Level Testing Framework

## 1. Business Logic & Process Validation (The Abstract Machine)

View the application as a Turing machine with tape (data) and head (logic). Flaws occur when the logic head misinterprets the tape state.

- **Order of Operations (Step Manipulation)**:
  - **Skipping**: Attempt to jump from Step 1 (Cart) directly to Step 3 (Order Confirmation), bypassing Step 2 (Payment).
  - **Reordering**: Executing steps out of sequence (e.g., Shipping before Payment).
- **Zero/Negative Values**: Can quantity/price be negative?
- **Race Conditions**: Can coupons be used twice simultaneously? (Parallel Requesting).
- **Mass Assignment**: Can you update `role`, `balance`, or `is_admin` via API updates?

## 2. Advanced Access Control (Authorization)

Verify *who* can do *what*:

- **Horizontal Privilege Escalation (IDOR)**:
  - Can User A access User B's objects (KRS, Transcripts)?
  - Test UUIDs vs Sequential IDs.
- **Vertical Privilege Escalation**:
  - Can a Student access Lecturer/Admin endpoints?
  - Check for "Hidden" admin routes (`/admin`, `/api/admin`).
- **Function-Level Access Control**:
  - Can a low-level user call a high-level API endpoint directly (e.g., `POST /api/users/delete`)?

## 3. Session & Authentication Integrity

- **Session Fixation**: Does the session ID change after login?
- **Session Termination**: Does logout *actually* invalidate the token on the server?
- **Forced Browsing**: Can you access authenticated pages by just knowing the URL (Bypassing login check)?
- **Cookie Attribute Analysis**: Are `HttpOnly`, `Secure`, and `SameSite` flags properly set?

## 4. Workflows

### 4.1. Manual Exploration
Use `astro_session_fixer.py` (if available) to establish a baseline session, then manually verify critical endpoints.

### 4.2. Fuzzing with Context
When fuzzing, ensure the session is valid. Automated tools often lose session context. Use scripts that refresh tokens or handle redirects intelligently.

### 4.3. Data Exfiltration Test
If an IDOR is suspected, attempt to extract *proof* (non-sensitive if possible, or own data from another account) to confirm impact.

## 5. 2025 Emerging Threats & Business Logic Vectors

### 5.1. AI-Powered Logic Analysis
- Use LLMs to analyze API schemas (Swagger/OpenAPI) for logical inconsistencies that scanners miss.
- **Technique**: Feed the API spec to an LLM and ask: "Based on this schema, how can I bypass the payment verification step?"

### 5.2. Cloud-Native Logic Flaws
- **Serverless Function Abuse**: Triggering functions (AWS Lambda/Azure Functions) excessively to cause Denial of Wallet (DoW).
- **Storage Logic**: Bypassing signed URLs by manipulating expiration times or bucket policies.

### 5.3. Advanced Race Conditions
- **Limit Bypass**: Exceeding withdrawal limits or coupon usage by sending parallel requests (Turbo Intruder style).
- **Time-of-Check to Time-of-Use (TOCTOU)**: Changing the state of a resource (e.g., balance) between the time it is checked and the time it is used.
