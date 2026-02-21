# Audit Report: seodomains.com.hr
**Target:** https://seodomains.com.hr
**CMS:** FOSSBilling 0.6.14
**Server:** nginx/1.25.3

## Findings
1. **Admin Panel:** Located at `/admin/staff/login` (Status 302 to login).
2. **Password Reset:** Located at `/password-reset` (Status 200).
3. **Information Disclosure:** FOSSBilling version 0.6.14 disclosed via `API.js`.
4. **Configuration Prob:** `/config.php` returns 200 but is empty (properly handled).
5. **CSRF Protection:** Enabled (Token present in forms).
6. **Host Header Poisoning (CONFIRMED):** The API endpoint `https://seodomains.com.hr/api/guest/client/reset_password` accepts poisoned `Host` headers. 
   - Test: `Host: windstorm.getfoxyproxy.org` -> Result: `{"result":true}`.
   - Impact: Account Takeover (ATO) via token hijacking.

## Infrastructure Mapping (Local Cluster)
- **Target Portal:** 46.183.184.105 (seodomains.com.hr)
- **Active Graphite C2:** 46.183.184.147 (JARM: 1dd40d40d00040d00042d43d000000ad9bf51cc3f5a1e29eecb81d0c7b06eb)
- **Bouncer/Proxy Node:** 46.183.184.82 (JARM: 2ad2ad0002ad2ad0002ad2ad2ad2ad02098c5f1b1aef82f7daaf9fed36c4e8)
