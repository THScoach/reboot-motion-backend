# 🎯 WHOP DASHBOARD SETUP - STEP-BY-STEP GUIDE

**Your Dashboard**: https://whop.com/home-feed/

This guide will walk you through setting up all products, plans, and integrations for Catching Barrels on Whop.

---

## 📋 SETUP CHECKLIST OVERVIEW

- [ ] **Step 1**: Create Company/Business (if not done)
- [ ] **Step 2**: Create App Subscription Products (6 plans)
- [ ] **Step 3**: Create Coaching Products (3 products)
- [ ] **Step 4**: Create Team Packages (4 plans)
- [ ] **Step 5**: Set Up Developer Settings (API Keys)
- [ ] **Step 6**: Configure Webhooks
- [ ] **Step 7**: Copy All IDs and Send to Me

**Estimated Time**: 1-2 hours

---

## STEP 1️⃣: CREATE/VERIFY YOUR COMPANY

### Navigate to Business Settings
1. Go to: https://whop.com/dashboard
2. Click on your profile/company name in top left
3. If you don't have a company yet:
   - Click "Create a business"
   - Company name: **"Catching Barrels"** (or your preferred name)
   - Complete company profile
   - Add logo and branding

### ✅ Checkpoint:
- [ ] Company/Business created
- [ ] Company ID noted (format: `biz_xxxxxxxxxxxxx`)

---

## STEP 2️⃣: CREATE APP SUBSCRIPTION PRODUCTS

### Navigate to Products
1. Go to: https://whop.com/dashboard
2. Click **"Products"** in left sidebar
3. Click **"+ Create product"**

---

### Product 1: Premium Monthly

1. Click **"+ Create product"**
2. **Product Name**: `Premium Monthly`
3. **Product Type**: Select **"Membership"**
4. **Pricing**:
   - **Price**: `$12.99`
   - **Billing Cycle**: `Monthly`
   - **Trial Period**: `0 days` (or set to 14 if you want free trial)
5. **Description**:
   ```
   Full 50-swing Baseline Assessment + Complete Momentum Signature Report
   
   Includes:
   • Full 50-swing baseline assessment
   • Complete Momentum Signature report
   • Detailed Ground-Engine-Weapon scores
   • Pro comparison (20+ players)
   • Personalized drill protocol
   • Quarterly reassessment
   • 90-day video storage
   • Progress tracking dashboard
   • Email support
   ```
6. **Features** (optional): Add bullet points of features
7. Click **"Create product"**
8. **IMPORTANT**: Copy the **Plan ID** (format: `plan_xxxxxxxxxxxxx`)
   - Write it down: `PREMIUM_MONTHLY_PLAN_ID = plan_______________`

---

### Product 2: Premium Annual ⭐ (BEST VALUE)

1. Click **"+ Create product"**
2. **Product Name**: `Premium Annual` (add "⭐ BEST VALUE" badge if possible)
3. **Product Type**: Select **"Membership"**
4. **Pricing**:
   - **Price**: `$79.99`
   - **Billing Cycle**: `Yearly` or `Annual`
   - **Trial Period**: `0 days`
5. **Description**:
   ```
   🎉 SAVE 49%! Only $6.67/month when billed annually.
   
   Full 50-swing Baseline Assessment + Complete Momentum Signature Report
   
   Includes:
   • Full 50-swing baseline assessment
   • Complete Momentum Signature report
   • Detailed Ground-Engine-Weapon scores
   • Pro comparison (20+ players)
   • Personalized drill protocol
   • Quarterly reassessment
   • 90-day video storage
   • Progress tracking dashboard
   • Email support
   ```
6. Click **"Create product"**
7. **IMPORTANT**: Copy the **Plan ID**
   - Write it down: `PREMIUM_ANNUAL_PLAN_ID = plan_______________`

---

### Product 3: Pro Monthly

1. Click **"+ Create product"**
2. **Product Name**: `Pro Monthly`
3. **Product Type**: Select **"Membership"**
4. **Pricing**:
   - **Price**: `$19.99`
   - **Billing Cycle**: `Monthly`
5. **Description**:
   ```
   Everything in Premium + Unlimited Swings + Advanced Analytics
   
   Premium Features PLUS:
   • Unlimited swing captures
   • Daily tracking & trending
   • Unlimited reassessments
   • 1-year video storage
   • Advanced analytics (swing-to-swing variance)
   • Drill video library (full access)
   • Weekly insight emails
   • Priority support
   • Early access to new features
   ```
6. Click **"Create product"**
7. **IMPORTANT**: Copy the **Plan ID**
   - Write it down: `PRO_MONTHLY_PLAN_ID = plan_______________`

---

### Product 4: Pro Annual

1. Click **"+ Create product"**
2. **Product Name**: `Pro Annual`
3. **Product Type**: Select **"Membership"**
4. **Pricing**:
   - **Price**: `$149.99`
   - **Billing Cycle**: `Yearly` or `Annual`
5. **Description**:
   ```
   💪 SAVE 37%! Only $12.50/month when billed annually.
   
   Everything in Premium + Unlimited Swings + Advanced Analytics
   
   Premium Features PLUS:
   • Unlimited swing captures
   • Daily tracking & trending
   • Unlimited reassessments
   • 1-year video storage
   • Advanced analytics
   • Drill video library
   • Weekly insight emails
   • Priority support
   • Early access to new features
   ```
6. Click **"Create product"**
7. **IMPORTANT**: Copy the **Plan ID**
   - Write it down: `PRO_ANNUAL_PLAN_ID = plan_______________`

---

### Product 5: Elite Monthly

1. Click **"+ Create product"**
2. **Product Name**: `Elite Monthly`
3. **Product Type**: Select **"Membership"**
4. **Pricing**:
   - **Price**: `$39.99`
   - **Billing Cycle**: `Monthly`
5. **Description**:
   ```
   Everything in Pro + Coach AI + Monthly Video Reviews + Private Community
   
   Pro Features PLUS:
   • Coach AI (ask questions about YOUR swing)
   • Monthly async video review from Coach Rick (3-5 min)
   • Custom drill protocols (AI-generated)
   • Pro swing breakdown library
   • Unlimited video storage
   • Private community access
   • Direct message support
   • Quarterly live Q&A access
   ```
6. Click **"Create product"**
7. **IMPORTANT**: Copy the **Plan ID**
   - Write it down: `ELITE_MONTHLY_PLAN_ID = plan_______________`

---

### Product 6: Elite Annual

1. Click **"+ Create product"**
2. **Product Name**: `Elite Annual`
3. **Product Type**: Select **"Membership"**
4. **Pricing**:
   - **Price**: `$299.99`
   - **Billing Cycle**: `Yearly` or `Annual`
5. **Description**:
   ```
   🏆 SAVE 37%! Only $25/month when billed annually.
   
   Everything in Pro + Coach AI + Monthly Video Reviews + Private Community
   
   Pro Features PLUS:
   • Coach AI (ask questions about YOUR swing)
   • Monthly async video review from Coach Rick
   • Custom drill protocols (AI-generated)
   • Pro swing breakdown library
   • Unlimited video storage
   • Private community access
   • Direct message support
   • Quarterly live Q&A access
   ```
6. Click **"Create product"**
7. **IMPORTANT**: Copy the **Plan ID**
   - Write it down: `ELITE_ANNUAL_PLAN_ID = plan_______________`

---

### ✅ Checkpoint:
- [ ] All 6 app subscription products created
- [ ] All 6 Plan IDs copied and saved

---

## STEP 3️⃣: CREATE COACHING PRODUCTS

### Product 7: Monthly Coaching Membership

1. Click **"+ Create product"**
2. **Product Name**: `Monthly Coaching Membership`
3. **Product Type**: Select **"Membership"**
4. **Pricing**:
   - **Price**: `$99.00`
   - **Billing Cycle**: `Monthly`
5. **Description**:
   ```
   Unlimited Elite App Access + Monthly Group Coaching with Coach Rick
   
   Includes:
   • Unlimited app access (Elite tier included)
   • Monthly group coaching calls (recorded)
   • Live Q&A sessions
   • Swing reviews
   • Industry updates & recruiting guidance
   • Private community access
   
   ⏰ Your Time: 2-4 hours/month for calls + content
   👥 Capacity: Unlimited (group format)
   ```
6. Click **"Create product"**
7. **IMPORTANT**: Copy the **Plan ID**
   - Write it down: `MONTHLY_COACHING_PLAN_ID = plan_______________`

---

### Product 8: In-Person Assessment

1. Click **"+ Create product"**
2. **Product Name**: `In-Person Assessment`
3. **Product Type**: Select **"One-time purchase"** or **"Course"**
4. **Pricing**:
   - **Price**: `$399.00`
   - **One-time payment**
5. **Availability**: Set seasonal (Nov-Feb) if Whop allows scheduling
6. **Description**:
   ```
   2-Hour In-Person Swing Assessment with Coach Rick
   
   Includes:
   • 2-hour in-person session
   • Up to 50 swings captured & analyzed
   • Full biomechanics Lab Report delivered
   • One-on-one coaching feedback
   
   📅 Available: November - February only
   📍 Location: [Your location/facility]
   ⏰ Your Time: 2 hours + processing
   ```
7. Click **"Create product"**
8. **IMPORTANT**: Copy the **Product ID** (format: `prod_xxxxxxxxxxxxx`)
   - Write it down: `IN_PERSON_PRODUCT_ID = prod_______________`

---

### Product 9: 90-Day Transformation Program

1. Click **"+ Create product"**
2. **Product Name**: `90-Day Transformation Program`
3. **Product Type**: Select **"One-time purchase"** or **"Course"**
4. **Pricing Options**:
   - Create two variants if possible:
     - **Full Payment**: `$1,299.00`
     - **Payment Plan**: `3 payments of $450.00`
   - If only one option, use: `$1,299.00`
5. **Description**:
   ```
   90-Day Elite Coaching Program with Personalized Training Plan
   
   Includes:
   • 90 days of Elite app access
   • Initial 1:1 video call with Coach Rick (30 min)
   • Personalized 90-day development plan
   • Bi-weekly async video feedback
   • Mid-point check-in call (15 min)
   • Final assessment comparison
   • Graduate to Elite at 40% off ($179.99/year ongoing)
   
   📅 Available: November - February only
   👥 Limited to 10-15 athletes per quarter
   ⏰ Your Time: ~4 hours per athlete over 90 days
   ```
6. Click **"Create product"**
7. **IMPORTANT**: Copy the **Product ID**
   - Write it down: `NINETY_DAY_PRODUCT_ID = prod_______________`

---

### ✅ Checkpoint:
- [ ] All 3 coaching products created
- [ ] All 3 Product/Plan IDs copied and saved

---

## STEP 4️⃣: CREATE TEAM PACKAGES

### Product 10: Team Starter

1. Click **"+ Create product"**
2. **Product Name**: `Team Starter (10-15 players)`
3. **Product Type**: Select **"Membership"**
4. **Pricing**:
   - **Price**: `$599.00`
   - **Billing Cycle**: `Yearly` or `Annual`
5. **Description**:
   ```
   Team Package: Premium Access for 10-15 Players
   
   💰 Only $40-60 per player/year
   
   Includes:
   • All players get Premium access
   • Team dashboard for coach
   • Aggregate team insights
   • One team consultation call
   
   Perfect for: High school teams, club teams
   ```
6. Click **"Create product"**
7. **IMPORTANT**: Copy the **Plan ID**
   - Write it down: `TEAM_STARTER_PLAN_ID = plan_______________`

---

### Product 11: Team Pro

1. Click **"+ Create product"**
2. **Product Name**: `Team Pro (10-15 players)`
3. **Product Type**: Select **"Membership"**
4. **Pricing**:
   - **Price**: `$999.00`
   - **Billing Cycle**: `Yearly` or `Annual`
5. **Description**:
   ```
   Team Package: Pro Access for 10-15 Players
   
   💰 Only $67-100 per player/year
   
   Includes:
   • All players get Pro access
   • Advanced team analytics
   • Quarterly team reviews
   • Priority support
   
   Perfect for: Competitive travel teams, academies
   ```
6. Click **"Create product"**
7. **IMPORTANT**: Copy the **Plan ID**
   - Write it down: `TEAM_PRO_PLAN_ID = plan_______________`

---

### Product 12: Team Elite

1. Click **"+ Create product"**
2. **Product Name**: `Team Elite (10-15 players)`
3. **Product Type**: Select **"Membership"**
4. **Pricing**:
   - **Price**: `$1,999.00`
   - **Billing Cycle**: `Yearly` or `Annual`
5. **Description**:
   ```
   Team Package: Elite Access for 10-15 Players
   
   💰 Only $133-200 per player/year
   
   Includes:
   • All players get Elite access
   • Monthly team video reviews
   • Custom team protocols
   • Direct coach hotline
   
   Perfect for: Elite travel teams, prep schools
   ```
6. Click **"Create product"**
7. **IMPORTANT**: Copy the **Plan ID**
   - Write it down: `TEAM_ELITE_PLAN_ID = plan_______________`

---

### Product 13: Facility License (Optional - Custom Pricing)

1. Click **"+ Create product"**
2. **Product Name**: `Facility Licensing`
3. **Product Type**: Select **"Membership"** or use contact form
4. **Pricing**:
   - **Price**: `$2,500.00` (starting price)
   - **Billing Cycle**: `Yearly` or `Annual`
   - Note: "Contact for custom pricing ($2,500-5,000/year)"
5. **Description**:
   ```
   White-Label Facility Partnership
   
   💼 Custom Pricing: $2,500-5,000/year (based on facility size)
   
   Includes:
   • White-label app option
   • Unlimited athlete assessments
   • Facility dashboard
   • Co-branded reports
   • Staff training
   • Revenue share on upgrades (optional)
   
   📞 Contact us for custom quote and onboarding
   ```
6. Click **"Create product"**
7. **IMPORTANT**: Copy the **Plan ID**
   - Write it down: `FACILITY_LICENSE_PLAN_ID = plan_______________`

---

### ✅ Checkpoint:
- [ ] All 4 team packages created
- [ ] All 4 Plan IDs copied and saved

---

## STEP 5️⃣: SET UP DEVELOPER SETTINGS (API KEYS)

### Navigate to Developer Dashboard
1. Go to: https://whop.com/dashboard/developer
2. Or click **"Developer"** in left sidebar

### Create Company API Key
1. Find the **"Company API Keys"** section
2. Click **"+ Create"** button
3. **API Key Name**: `Catching Barrels Backend API`
4. **Select Permissions**:
   - ✅ `member:basic:read`
   - ✅ `webhook_receive:memberships`
   - ✅ `payment:read`
   - ✅ `membership:read`
   - ✅ `membership:write` (if available)
5. Click **"Create API Key"**
6. **CRITICAL**: Copy the API key immediately (you can only see it once!)
   - Format: `whop_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Write it down: `WHOP_API_KEY = whop___________________________________`

---

### ✅ Checkpoint:
- [ ] API Key created
- [ ] API Key copied and saved securely

---

## STEP 6️⃣: CONFIGURE WEBHOOKS

### Note: We'll set this up together after I build the webhook endpoint

**For now, just note where the webhook settings are:**
1. Go to: https://whop.com/dashboard/developer
2. Find **"Webhooks"** section
3. Don't create yet - we'll do this together after I give you the webhook URL

**What we'll configure later:**
- Webhook URL: `https://[your-backend-url]/api/webhooks/whop`
- Events to subscribe to:
  - `membership.activated`
  - `membership.deactivated`
  - `payment.succeeded` (optional)

---

### ✅ Checkpoint:
- [ ] Located webhook settings (don't create yet)

---

## STEP 7️⃣: COPY ALL IDs AND SEND TO ME

### Fill Out This Template:

```
=== WHOP CREDENTIALS ===
WHOP_API_KEY=whop_

=== APP SUBSCRIPTION PLAN IDs ===
PREMIUM_MONTHLY_PLAN_ID=plan_
PREMIUM_ANNUAL_PLAN_ID=plan_
PRO_MONTHLY_PLAN_ID=plan_
PRO_ANNUAL_PLAN_ID=plan_
ELITE_MONTHLY_PLAN_ID=plan_
ELITE_ANNUAL_PLAN_ID=plan_

=== COACHING PRODUCT IDs ===
MONTHLY_COACHING_PLAN_ID=plan_
IN_PERSON_PRODUCT_ID=prod_
NINETY_DAY_PRODUCT_ID=prod_

=== TEAM PACKAGE PLAN IDs ===
TEAM_STARTER_PLAN_ID=plan_
TEAM_PRO_PLAN_ID=plan_
TEAM_ELITE_PLAN_ID=plan_
FACILITY_LICENSE_PLAN_ID=plan_

=== COMPANY INFO ===
WHOP_COMPANY_ID=biz_
COMPANY_NAME=
PRIMARY_DOMAIN=https://

=== BACKEND INFO ===
BACKEND_API_URL=https://  (e.g., https://api.catchingbarrels.com)
FRONTEND_URL=https://  (e.g., https://catchingbarrels.com or https://app.catchingbarrels.com)
```

---

## 🎯 WHAT HAPPENS NEXT

### Once you send me the above:

**I will (30 minutes):**
1. ✅ Update `whop_subscription.py` with your real Plan IDs
2. ✅ Create `.env` configuration file
3. ✅ Build FastAPI webhook endpoint
4. ✅ Deploy webhook endpoint (or give you deployment instructions)
5. ✅ Give you webhook URL to configure in Whop dashboard

**Then you will (5 minutes):**
1. ✅ Add webhook URL in Whop dashboard
2. ✅ Copy webhook secret
3. ✅ Send webhook secret to me

**Then I will (2 hours):**
1. ✅ Complete webhook integration
2. ✅ Build frontend pricing page with Whop embeds
3. ✅ Create subscription dashboard
4. ✅ Test end-to-end flow
5. ✅ Deploy to production

**Total time: ~3 hours from when you send the IDs!** 🚀

---

## 💡 TIPS FOR WHOP DASHBOARD

### Making Products Look Great:
- Add product images/thumbnails
- Use clear, benefit-focused descriptions
- Highlight savings on annual plans (49%, 37%)
- Use emojis sparingly for visual appeal
- Add FAQs to product pages

### Pricing Strategy:
- **Push annual plans** - make them the default/highlighted option
- Show monthly equivalent price (e.g., "$6.67/mo when billed annually")
- Display savings badges prominently
- Consider adding limited-time offers for launches

### Organization:
- Group related products (e.g., all Premium tiers together)
- Use consistent naming conventions
- Add tags or categories if Whop supports it

---

## 🆘 NEED HELP?

If you get stuck or have questions while setting up:

1. **Can't find something?** - Take a screenshot and I'll guide you
2. **Unclear on pricing?** - Refer to the pricing sheet in the marketing plan
3. **Technical issues?** - Whop support is pretty responsive
4. **Want to skip something?** - Let me know, we can come back to it

---

## ✅ FINAL CHECKLIST

Before sending me the IDs, make sure you have:

- [ ] Created all 13 products/plans on Whop
- [ ] Copied all 13 Plan/Product IDs
- [ ] Created API Key
- [ ] Noted your Company ID
- [ ] Noted your backend/frontend URLs
- [ ] Filled out the template above

**Then paste the filled template in our chat, and I'll build the integration!** 🚀

---

**Good luck! Take your time, and let me know if you need any clarification on any step.** 👍
