Subject: API Integration Issues - Need Guidance on Pipeline v2 Data Access

Hi Robert,

I hope this email finds you well. My developer and I are working on integrating our application with the Reboot Motion API, and we've run into some challenges that we're hoping you can help clarify.

**What We're Trying to Do:**
We're building a backend system that syncs athlete data, sessions, and biomechanics reports from the Reboot Motion API into our PostgreSQL database. We've successfully implemented OAuth 2.0 authentication and can sync player data without issues.

**The Problems We're Encountering:**

1. **Pipeline v2 and /processed_data Endpoint:**
   - When we try to use the `/processed_data` endpoint to fetch biomechanics data, we consistently get 404 errors with this message:
   - *"The processed data folder for customers is unavailable for Reboot Motion's Pipeline v2. These files can be found in the inverse-kinematics and momentum-energy folders for a player/session in your Reboot Motion-provided S3 Bucket."*
   - We're using single-camera (hitting-lite) sessions, which appear to be Pipeline v2.
   - **Question:** Is there an API endpoint we should use instead of `/processed_data` for Pipeline v2 sessions? Or do we need direct S3 bucket access?

2. **The /reports Endpoint:**
   - We tried using the `/reports` endpoint as an alternative to identify which sessions have actual data, but we're getting 400 errors regardless of the `movement_types` parameter we use:
   - Tried: `movement_types=[1]` → Error: *"Unsupported movement types: ['1']"*
   - Tried: `movement_types=['hitting-lite-processed-metrics', 'hitting-processed-metrics']` → Error: *"Unsupported movement types: ['hitting-processed-metrics', 'hitting-lite-processed-metrics']"*
   - **Question:** What is the correct format for the `movement_types` parameter in the `/reports` endpoint? Can you provide an example of valid movement type values?

3. **Session Participant Information:**
   - The `/sessions` endpoint returns session metadata, but we can't reliably determine which players actually participated in each session.
   - The `participants` field is either missing or empty in the session data we're receiving.
   - **Question:** Is there a recommended way to determine which players participated in a specific session via the API?

**What We've Tried:**
- Using OAuth 2.0 authentication (working correctly)
- Querying `/players` endpoint (working - syncing 100 players successfully)
- Querying `/sessions` endpoint with date filters (working - getting session metadata)
- Attempting `/processed_data` with session_id + org_player_id (404 errors for Pipeline v2)
- Attempting `/reports` with various movement_types parameters (400 errors)
- Checking for `participants` arrays in session data (mostly empty)

**Current Workaround:**
We're currently importing all hitting sessions for all players and marking them as needing biomechanics data sync, but we'd prefer a more accurate approach that only creates session records for players who actually participated.

**What Would Help:**
- Clarification on how to access Pipeline v2 biomechanics data programmatically
- Example API calls for the `/reports` endpoint with correct parameters
- Guidance on determining session participants via the API
- Documentation or examples for single-camera (hitting-lite) data access

I really appreciate your help with this. The Reboot Motion data is incredibly valuable for our athletes, and we're excited to integrate it properly into our system.

Please let me know if you need any additional information about our use case or the specific API calls we're making.

Thanks so much!

Best regards,
[Your Name]
[Your Organization]

---

**Technical Details for Reference:**
- API Base URL: https://api.rebootmotion.com
- Authentication: OAuth 2.0 (working correctly)
- Sessions: Filtering for hitting sessions from last 30 days
- Session Types: Primarily single-camera (hitting-lite-processed-metrics)
- Current Session Count: ~1 hitting session in the date range tested (session_id: 6764e74b-516d-45eb-a8a9-c50a069ef50d, date: 2025-12-02)
