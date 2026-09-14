# Waffarha-Style Marketplace
## Complete Product Specification

### 1. Product Definition

The platform is a **multi-sided local-commerce marketplace** connecting:

**Consumers ↔ Offers/Vouchers ↔ Merchants ↔ Payment Providers ↔ Redemption Infrastructure**

The platform should support both:

1. **Marketplace transactions**
   - Food
   - Entertainment
   - Hotels
   - Health & Beauty
   - Retail & Services
   - Gift Vouchers
   - Gaming/Digital Cards
   - Transportation/Tickets
   - Future verticals

2. **B2B/B2B2C distribution**
   - Merchant promotions
   - Corporate benefits
   - Telco loyalty programs
   - Bank/cardholder offers
   - Third-party partner marketplaces

---

# 2. Product Objectives

### Consumer objectives

- Discover attractive local offers quickly.
- Understand the real saving before purchasing.
- Find offers near the user.
- Compare merchants, prices and conditions.
- Purchase using preferred payment methods.
- Receive an immediately usable digital voucher.
- Redeem without unnecessary friction.
- Manage active, used and expired purchases.
- Receive personalized recommendations.
- Earn cashback/rewards.
- Purchase gifts for other people.

### Merchant objectives

- Acquire new customers.
- Create and manage promotions.
- Control validity, branches and availability.
- Validate vouchers.
- Track redemption.
- Monitor sales and customer acquisition.
- Receive settlement/payouts.
- Analyze campaign performance.

### Platform objectives

- Maximize GMV.
- Increase transaction frequency.
- Increase repeat purchase rate.
- Reduce voucher failure rate.
- Increase merchant retention.
- Increase average order value.
- Generate revenue through commissions, fees, promoted listings and B2B partnerships.

---

# 3. Product Ecosystem

```text
                         ┌─────────────────────┐
                         │   Consumer App/Web  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   API / Gateway     │
                         └──────────┬──────────┘
                                    │
      ┌─────────────────────────────┼──────────────────────────────┐
      │                             │                              │
      ▼                             ▼                              ▼
Marketplace Engine           Transaction Engine             Identity Engine
      │                             │                              │
 Offers                         Cart/Orders                    Accounts
 Merchants                      Payments                       Profiles
 Categories                     Vouchers                       Roles
 Search                         Refunds                        Consent
 Discovery                      Wallet                         Security
 Location                       Settlement
      │                             │
      └─────────────────────────────┼──────────────────────────────┘
                                    │
                                    ▼
                            Integration Layer
             ┌──────────────┬──────────────┬──────────────┐
             │              │              │              │
          Payments       Maps/Geo       Messaging      Partners
          Fawry/etc.       Maps         SMS/Email       Banks/Telcos
             │              │              │
             └──────────────┴──────────────┴──────────────┘

                         ┌─────────────────────┐
                         │ Admin Control Center │
                         └─────────────────────┘

                         ┌─────────────────────┐
                         │ Merchant Portal/App │
                         └─────────────────────┘
```

---

# 4. User Roles

## 4.1 Consumer

Primary marketplace customer.

Permissions:

- Browse
- Search
- Filter
- View offers
- Add to cart
- Purchase
- Pay
- View vouchers
- Redeem
- Request refund
- Use wallet
- Receive cashback
- Buy gifts
- Manage profile
- Save favorites
- Review offers
- Manage notification preferences

---

## 4.2 Merchant Owner

Permissions:

- Manage company
- Manage branches
- Create offers
- Edit offers
- Submit offers for approval
- Manage staff
- View sales
- View redemptions
- View settlements
- Export reports

---

## 4.3 Merchant Staff / Cashier

Restricted operational role.

Permissions:

- Login
- Scan voucher
- Enter voucher code
- Validate voucher
- Redeem voucher
- View basic transaction information

No access to:

- settlements
- financial reports
- company settings
- offer pricing
- other branches unless explicitly authorized

---

## 4.4 Merchant Manager

Everything a cashier can do plus:

- Branch management
- Staff management
- Offer monitoring
- Redemption reports
- Campaign analytics

---

## 4.5 Customer Support Agent

Permissions:

- Search customer
- Search orders
- Search vouchers
- View payment state
- View redemption state
- Issue authorized refunds
- Resend vouchers
- Extend validity where policy permits
- Add goodwill credit
- Create support tickets
- Escalate disputes

---

## 4.6 Content Manager

Permissions:

- Manage banners
- Categories
- Collections
- Campaigns
- Landing pages
- Featured merchants
- Homepage merchandising

---

## 4.7 Finance User

Permissions:

- Payments
- refunds
- settlements
- merchant balances
- commissions
- reconciliation
- payout files

---

## 4.8 Platform Admin

Full access.

---

## 4.9 Super Admin

System-level configuration:

- RBAC
- integrations
- feature flags
- security
- system configuration
- audit logs

---

# 5. Consumer App Sitemap

```text
HOME
│
├── Search
│
├── Location
│
├── Categories
│   ├── Food & Beverage
│   ├── Fun & Activities
│   ├── Hotels & Aqua Parks
│   ├── Health & Beauty
│   ├── Retail & Services
│   ├── Gift Vouchers
│   ├── Gaming
│   ├── Travel / Tickets
│   └── More
│
├── Collections
│   ├── Hot Deals
│   ├── Top Picks
│   ├── Best Sellers
│   ├── New
│   ├── Near You
│   ├── Bundles
│   └── Seasonal
│
├── Offer Details
│   ├── Description
│   ├── Pricing
│   ├── Discount
│   ├── Merchant
│   ├── Branches
│   ├── Map
│   ├── Conditions
│   ├── Reviews
│   └── Purchase
│
├── Cart
│
├── Checkout
│
├── My Orders
│   ├── Active
│   ├── Upcoming
│   ├── Used
│   ├── Expired
│   └── Cancelled
│
├── My Wallet
│
├── Cashback
│
├── Favorites
│
├── Rewards / Loyalty
│
├── Gift Vouchers
│
├── Notifications
│
├── Support
│
└── Profile
    ├── Personal Information
    ├── Addresses
    ├── Payment Methods
    ├── Preferences
    ├── Privacy
    └── Security
```

---

# 6. Consumer Modules

## 6.1 Authentication

Methods:

- Mobile number + OTP
- Email + password
- Social login
- Apple
- Google

Recommended:

**Progressive registration**

Allow browsing without an account.

Ask for account creation at:

- checkout
- voucher saving
- favorites
- cashback
- personalized recommendations

---

# 7. Home Page

The homepage should be dynamic rather than static.

Recommended structure:

```text
[Location: Cairo ▼]

[Search for food, fun, beauty...]

[Hero Banner]

Near You
────────────
Offer cards →

Recommended For You
────────────────────
Offer cards →

Hot Deals
─────────
Offer cards →

Food
────
Offer cards →

Activities
──────────
Offer cards →

Gift Cards
──────────

Bundles
───────

Best Sellers
────────────

Recently Viewed
───────────────
```

The marketplace should support personalized merchandising similar to Waffarha's current move toward personalized discovery, bundles, sorting and targeted collections. 

---

# 8. Search Engine

Search should understand:

- Merchant names
- Offer names
- Category
- Cuisine
- Activity
- Area
- City
- Brand
- Product
- Service

Example:

> "pizza maadi"

should return:

**Pizza offers + Maadi branches**

Recommended search stack:

- PostgreSQL full-text for MVP
- Elasticsearch/OpenSearch for scale
- Typo tolerance
- synonyms
- Arabic + English normalization
- transliteration support

Example:

```text
مطعم
restaurant
resturant
resto
```

should resolve intelligently.

---

# 9. Discovery & Recommendation Engine

Recommendation inputs:

- current location
- selected city
- previous purchases
- viewed offers
- search behavior
- favorite categories
- price range
- time/day
- merchant affinity
- redemption history
- seasonality

Recommendation types:

### Near You

Distance-first.

### For You

Behavior-first.

### Trending

Transaction-volume-first.

### Best Value

Discount + rating + conversion.

### Complete the Experience

Cross-sell.

Example:

```text
User buys cinema ticket
         ↓
Recommend
pizza + dessert + parking
```

---

# 10. Location Engine

The platform should support:

- GPS
- manually selected city
- manually selected area
- branch coordinates
- radius search
- distance sorting
- map view
- directions
- branch phone call

Offer location model:

```text
Country
  └── City
       └── Area
            └── Merchant
                 └── Branch
```

Each branch should contain:

- latitude
- longitude
- address
- phone
- opening hours
- holidays
- services
- supported offers

Waffarha's current product includes interactive branch maps and one-tap calling/directions, making this an important first-class component rather than a simple address field. 

---

# 11. Merchant Profile

Merchant page:

```text
Logo
Merchant Name
Rating
Category
Description

[Follow] [Share]

Current Offers
───────────────

Branches
────────

About
─────

Opening Hours

Reviews

Map
```

Merchant-level SEO pages should also exist on the web.

---

# 12. Offer Model

Every offer should contain:

### Commercial information

- title
- short title
- description
- original price
- selling price
- discount %
- taxes
- fees
- minimum quantity
- maximum quantity

### Inventory

- stock count
- daily quota
- total quota
- branch-specific inventory
- redemption limit
- customer purchase limit

### Scheduling

- sale start
- sale end
- validity start
- validity end
- blackout dates
- allowed days
- allowed hours

### Redemption

- online
- in-store
- reservation required
- QR
- code
- barcode
- PIN
- merchant validation

### Restrictions

- minimum age
- maximum users
- days excluded
- branch restrictions
- gender restrictions if legally appropriate
- customer eligibility

---

# 13. Offer Lifecycle

```text
DRAFT
  ↓
SUBMITTED
  ↓
UNDER REVIEW
  ↓
APPROVED
  ↓
SCHEDULED
  ↓
LIVE
  ↓
PAUSED
  ↓
EXPIRED
  ↓
ARCHIVED
```

Possible rejection:

```text
UNDER REVIEW
      ↓
   REJECTED
      ↓
Merchant edits
      ↓
SUBMITTED
```

---

# 14. Voucher Engine

This is one of the most important backend components.

## Voucher creation

When payment succeeds:

```text
Order
 ↓
Paid
 ↓
Generate Voucher
 ↓
Assign Unique Token
 ↓
Generate QR
 ↓
Generate Human-readable Code
 ↓
Activate Voucher
```

Each voucher should have:

```text
voucher_id
order_id
customer_id
offer_id
merchant_id
branch_scope
code
qr_token
status
issued_at
valid_from
valid_until
redeemed_at
redeemed_by
```

---

# 15. Voucher States

```text
CREATED
PAID
AVAILABLE
RESERVED
REDEMPTION_PENDING
REDEEMED
CANCELLED
REFUNDED
EXPIRED
SUSPENDED
```

Never allow a voucher to move backward from:

**REDEEMED → AVAILABLE**

without an explicit admin reversal workflow.

---

# 16. Redemption Engine

### Primary flow

```text
Merchant scans QR
        ↓
API validates token
        ↓
Check:
- voucher exists
- paid
- active
- not expired
- correct merchant
- correct branch
- correct offer
- redemption limit
        ↓
     VALID
        ↓
Merchant confirms
        ↓
Transaction locked
        ↓
Voucher = REDEEMED
        ↓
Customer notified
```

### Double-redemption protection

Use database transaction locking:

```sql
SELECT *
FROM vouchers
WHERE id = ?
FOR UPDATE;
```

Then perform:

1. validate
2. mark redeemed
3. commit

This prevents two merchant devices from redeeming the same voucher simultaneously.

---

# 17. QR Design

Do not encode sensitive information directly into the QR.

Recommended:

```text
https://redeem.example.com/v/8f2K7...
```

The token maps server-side to:

**voucher_id**

Use:

- cryptographically random token
- expiration
- signed redemption request
- optional one-time challenge

---

# 18. Offline Redemption

Because real-world venues can have poor connectivity, support a controlled offline mechanism.

Recommended approach:

### Merchant device

Periodically downloads:

- valid voucher IDs
- validity windows
- merchant scope
- redemption blacklist

Offline redemption:

```text
Scan
 ↓
Local validation
 ↓
Create signed redemption event
 ↓
Store locally
 ↓
Sync later
```

Important:

Offline redemption should be restricted to low-risk offer types or enforce an offline transaction limit.

---

# 19. Checkout

Recommended checkout flow:

```text
Cart
 ↓
Customer Information
 ↓
Promo / Wallet / Cashback
 ↓
Payment Method
 ↓
Payment
 ↓
3DS / OTP if required
 ↓
Payment Confirmation
 ↓
Order Created
 ↓
Voucher Issued
```

The payment page should prominently show:

```text
Original value          EGP 500
Offer price             EGP 299
Discount                EGP 201
Fees                     EGP  10
Wallet discount         -EGP 20
--------------------------------
Total                   EGP 289
```

This is extremely important for a savings-focused brand because unexpected fees can damage trust.

---

# 20. Payment Architecture

Use a payment abstraction layer.

```text
Checkout
   ↓
Payment Service
   ↓
Payment Router
   ├── Card Gateway
   ├── Wallet Gateway
   ├── Fawry
   ├── BNPL Provider
   ├── Installment Provider
   └── Alternative Payment
```

The application should not couple order logic directly to one payment provider.

---

# 21. Payment State Machine

```text
INITIATED
   ↓
PENDING
   ↓
AUTHORIZED
   ↓
CAPTURED
   ↓
SETTLED
```

Alternative:

```text
PENDING
  ↓
FAILED
```

Refund:

```text
CAPTURED
   ↓
REFUND_REQUESTED
   ↓
REFUND_PROCESSING
   ↓
REFUNDED
```

Partial refund:

```text
CAPTURED
   ↓
PARTIALLY_REFUNDED
```

---

# 22. Webhook Architecture

Every payment gateway must support:

```text
POST /webhooks/payments/{provider}
```

Webhook handler:

1. Verify signature.
2. Validate event ID.
3. Check idempotency.
4. Update payment.
5. Update order.
6. Issue/refund voucher as appropriate.
7. Publish event.
8. Return 200.

Never issue a voucher merely because the frontend says payment succeeded.

---

# 23. Wallet

Wallet should support:

- promotional credit
- cashback
- refunds
- goodwill credit
- gift balances

Use a ledger rather than just:

```text
wallet.balance = 100
```

Use:

```text
wallet_ledger
-------------
credit
debit
refund
cashback
expiration
adjustment
reference
```

Balance:

```text
sum(credits) - sum(debits)
```

This provides auditability.

---

# 24. Cashback Engine

Example:

```text
Offer:
Spend EGP 500

Cashback:
10%

Customer:
Pays EGP 500

Cashback:
EGP 50

Condition:
Released after successful redemption
```

This is better than immediately releasing cashback because it discourages fraud and cancelled transactions.

---

# 25. Loyalty / Rewards

Recommended points model:

```text
Purchase
  ↓
Earn Points
  ↓
Redeem Points
  ↓
Discount / Voucher / Perk
```

Potential rules:

- transaction points
- first purchase
- referral
- review
- birthday
- streak
- category completion
- campaign participation

The system can later support a leaderboard similar to Waffarha's recent gamification direction. 

---

# 26. Gift Voucher Module

Gift flow:

```text
Choose Merchant
       ↓
Choose Voucher
       ↓
Choose Recipient
       ↓
Message
       ↓
Delivery Date
       ↓
Payment
       ↓
Gift Created
```

Recipient receives:

- email
- SMS
- push notification
- gift link

Gift status:

```text
CREATED
SCHEDULED
SENT
OPENED
REDEEMED
EXPIRED
CANCELLED
```

---

# 27. Bundles

Bundle entity:

```text
Bundle
 ├── Offer A
 ├── Offer B
 ├── Offer C
 └── Bundle Discount
```

Examples:

**Date Night**

- Dinner
- Cinema
- Dessert

**Family Day**

- Breakfast
- Activity
- Kids play

**Wellness**

- Massage
- Facial
- Gym day pass

This is an important merchandising engine because it converts individual offers into higher-value journeys.

---

# 28. Merchant Portal Sitemap

```text
Dashboard
│
├── Sales
├── Orders
├── Redemptions
├── Offers
│   ├── All Offers
│   ├── Create Offer
│   ├── Drafts
│   ├── Pending Approval
│   └── Live
│
├── Branches
│
├── Employees
│
├── Customers
│
├── Reports
│   ├── Sales
│   ├── Redemptions
│   ├── Revenue
│   └── Performance
│
├── Settlements
│
├── Reviews
│
├── Notifications
│
└── Company Settings
```

---

# 29. Merchant Dashboard

Top-level KPIs:

```text
Today's Sales
EGP 25,420

Orders
214

Redeemed
178

Pending Redemption
63

Conversion Rate
7.8%

Customer Rating
4.6

Settlement Due
EGP 74,300
```

Charts:

- sales by day
- purchases by offer
- redemptions by branch
- revenue by category
- customer acquisition
- average order value

---

# 30. Merchant Offer Creation

Wizard:

### Step 1
Basic Information

### Step 2
Pricing

### Step 3
Inventory

### Step 4
Branches

### Step 5
Validity

### Step 6
Restrictions

### Step 7
Redemption rules

### Step 8
Media

### Step 9
Preview

### Step 10
Submit for approval

Merchant should see:

**Customer-facing preview**

before submission.

---

# 31. Merchant Mobile App

Merchant app should focus on speed rather than management.

Home:

```text
[SCAN VOUCHER]

Today's Redemptions
23

Today's Sales
EGP 5,420
```

Primary actions:

- Scan QR
- Enter code
- Validate
- Redeem
- Search voucher
- View recent redemptions

A cashier should be able to complete a voucher redemption in **seconds**, not minutes.

---

# 32. Admin Dashboard

```text
ADMIN
│
├── Overview
│
├── Customers
│   ├── Users
│   ├── Segments
│   ├── Suspended
│   └── Support
│
├── Merchants
│   ├── Applications
│   ├── Approved
│   ├── Suspended
│   ├── Branches
│   └── Staff
│
├── Offers
│   ├── Pending Review
│   ├── Live
│   ├── Scheduled
│   ├── Expired
│   └── Flagged
│
├── Orders
├── Payments
├── Refunds
├── Vouchers
├── Redemptions
│
├── Wallet
├── Cashback
├── Loyalty
│
├── Categories
├── Collections
├── Banners
├── Campaigns
│
├── Reviews
├── Support
│
├── Finance
│   ├── Settlements
│   ├── Commissions
│   └── Reconciliation
│
├── Reports
├── Notifications
├── CMS
│
├── Integrations
├── Roles & Permissions
├── Audit Logs
└── System Settings
```

---

# 33. Admin Offer Review

Reviewer sees:

```text
Merchant
Offer
Original Price
Sale Price
Discount %
Branches
Validity
Restrictions
Images
Terms
Tax information
Legal information
```

Decision:

**Approve**

**Reject**

**Request Changes**

**Schedule**

Approval should create an immutable audit record.

---

# 34. Database Architecture

Recommended relational model:

```text
users
user_profiles
user_addresses
user_preferences
user_devices
user_sessions

merchants
merchant_profiles
merchant_staff
merchant_branches
merchant_documents
merchant_payout_accounts

categories
subcategories
tags

offers
offer_variants
offer_prices
offer_inventory
offer_branches
offer_terms
offer_media
offer_schedules

collections
collection_offers
campaigns
campaign_offers
banners

carts
cart_items

orders
order_items
payments
payment_transactions
payment_webhooks

vouchers
voucher_events
redemptions

wallets
wallet_transactions
cashback_transactions

rewards
reward_transactions

gift_vouchers

reviews
ratings

favorites

notifications
notification_templates

support_tickets
support_messages

refunds

settlements
settlement_items

audit_logs
admin_actions
```

---

# 35. Core Relationships

```text
Merchant
  1 ─── N Branches

Merchant
  1 ─── N Offers

Offer
  N ─── N Categories/Tags

Offer
  N ─── N Branches

Customer
  1 ─── N Orders

Order
  1 ─── N OrderItems

OrderItem
  1 ─── N Vouchers

Voucher
  1 ─── 0..1 Redemption

Order
  1 ─── N Payments

Order
  1 ─── N Refunds
```

---

# 36. Key Database Entities

## User

```text
id
first_name
last_name
email
phone
password_hash
status
language
country
city
date_of_birth
created_at
updated_at
```

## Merchant

```text
id
legal_name
display_name
description
logo_url
status
industry
tax_id
commercial_registration
website
phone
email
created_at
```

## Branch

```text
id
merchant_id
name
address
city
area
latitude
longitude
phone
opening_hours
status
```

## Offer

```text
id
merchant_id
category_id
title
slug
description
original_price
selling_price
discount_percentage
status
sale_start
sale_end
valid_from
valid_until
redemption_type
stock
rating
created_at
```

## Order

```text
id
user_id
subtotal
discount
fees
wallet_credit
cashback
tax
total
currency
status
created_at
```

---

# 37. API Architecture

Recommended:

**REST for transactional APIs**

plus:

**GraphQL or BFF layer for mobile/web discovery**

and:

**WebSockets/push for real-time operational events where useful.**

---

# 38. Authentication APIs

```http
POST /v1/auth/register
POST /v1/auth/login
POST /v1/auth/send-otp
POST /v1/auth/verify-otp
POST /v1/auth/refresh
POST /v1/auth/logout
POST /v1/auth/forgot-password
```

---

# 39. User APIs

```http
GET    /v1/me
PATCH  /v1/me
GET    /v1/me/preferences
PATCH  /v1/me/preferences
GET    /v1/me/orders
GET    /v1/me/vouchers
GET    /v1/me/wallet
GET    /v1/me/rewards
GET    /v1/me/favorites
```

---

# 40. Discovery APIs

```http
GET /v1/home
GET /v1/categories
GET /v1/collections
GET /v1/offers
GET /v1/offers/{id}
GET /v1/search
GET /v1/recommendations
GET /v1/nearby
```

Example:

```http
GET /v1/offers?city=cairo&area=maadi
```

---

# 41. Merchant APIs

```http
POST  /v1/merchants/apply
GET   /v1/merchant/dashboard
GET   /v1/merchant/offers
POST  /v1/merchant/offers
PATCH /v1/merchant/offers/{id}
POST  /v1/merchant/offers/{id}/submit
GET   /v1/merchant/branches
POST  /v1/merchant/branches
GET   /v1/merchant/redemptions
GET   /v1/merchant/settlements
```

---

# 42. Redemption APIs

```http
POST /v1/redemption/validate
POST /v1/redemption/redeem
POST /v1/redemption/reverse
GET  /v1/redemption/{voucher_id}
```

Validate response:

```json
{
  "valid": true,
  "voucher_id": "VCH-123",
  "offer": "2-for-1 Burger",
  "customer": "Khaled",
  "expires_at": "2026-10-10T23:59:59Z",
  "requires_confirmation": true
}
```

---

# 43. Payment APIs

```http
POST /v1/checkout
POST /v1/payments/create
POST /v1/payments/{id}/confirm
GET  /v1/payments/{id}
POST /v1/payments/{id}/refund
POST /v1/payments/{id}/cancel
```

Webhook:

```http
POST /v1/webhooks/payments/{provider}
```

---

# 44. Order API Example

```json
{
  "order_id": "ORD-100021",
  "status": "PAID",
  "subtotal": 500,
  "discount": 150,
  "fees": 10,
  "wallet": 20,
  "total": 340,
  "currency": "EGP",
  "items": [
    {
      "offer_id": "OFF-8821",
      "quantity": 2,
      "unit_price": 170
    }
  ]
}
```

---

# 45. Event-Driven Architecture

Use domain events:

```text
UserRegistered
OfferPublished
CartCreated
OrderCreated
PaymentAuthorized
PaymentCaptured
OrderPaid
VoucherIssued
VoucherRedeemed
VoucherExpired
RefundRequested
RefundCompleted
CashbackEarned
SettlementCreated
ReviewCreated
```

Example:

```text
PaymentCaptured
       ↓
OrderPaid
       ↓
IssueVoucher
       ↓
SendNotification
       ↓
UpdateAnalytics
```

This makes the platform easier to scale.

---

# 46. Technology Architecture

Recommended production stack:

### Frontend

Consumer Web:
- Next.js
- React
- TypeScript

Consumer App:
- Flutter or React Native

Merchant App:
- Flutter/React Native

Admin:
- React / Next.js

### Backend

Option A:

- NestJS
- TypeScript

Option B:

- Java/Spring Boot

For a fast modern implementation, I recommend:

**NestJS + PostgreSQL + Redis + OpenSearch**

---

# 47. Infrastructure

```text
Cloud Load Balancer
        ↓
API Gateway
        ↓
Application Services
        ↓
PostgreSQL
Redis
Object Storage
OpenSearch
Message Queue
```

Use:

- AWS / Azure / GCP
- CDN
- object storage
- managed database
- Redis
- queue/event broker

---

# 48. Suggested Microservices

Do not begin with 20 microservices.

MVP:

```text
Core API
Marketplace
Orders
Payments
Voucher
Merchant
Notification
Admin
```

At scale split:

```text
Identity Service
Catalog Service
Search Service
Recommendation Service
Order Service
Payment Service
Voucher Service
Wallet Service
Loyalty Service
Merchant Service
Settlement Service
Notification Service
Support Service
Analytics Service
```

---

# 49. Caching Strategy

Cache:

- home feed
- categories
- merchant profiles
- offer details
- popular offers
- city/area lists

Do not blindly cache:

- payment status
- voucher status
- wallet balance
- redemption state

Those require authoritative database reads.

---

# 50. Notification System

Channels:

- Push
- SMS
- Email
- WhatsApp where legally/commercially appropriate

Triggers:

```text
Order Paid
Voucher Issued
Voucher Expiring
Voucher Redeemed
Payment Failed
Refund Complete
New Nearby Deal
Price Drop
Wishlist Deal
Gift Sent
Campaign
```

---

# 51. Support System

The platform needs a proper support engine rather than only a generic chat screen.

Ticket types:

- Payment issue
- Voucher issue
- Merchant refused voucher
- Refund
- Account issue
- Cancellation
- Duplicate payment
- Gift issue
- Technical issue

Ticket states:

```text
OPEN
IN_PROGRESS
WAITING_CUSTOMER
WAITING_MERCHANT
ESCALATED
RESOLVED
CLOSED
```

---

# 52. Critical Support Workflow

For:

> “Merchant says my coupon is invalid.”

Agent should see one screen:

```text
Customer
Order
Payment
Voucher
Merchant
Branch
Offer
Validity
Redemption attempts
Previous support tickets
```

Then actions:

**Validate**

**Reissue**

**Extend**

**Refund**

**Credit Wallet**

**Escalate**

This directly addresses one of the biggest operational risks identified in current Waffarha customer feedback. 

---

# 53. Finance & Settlement

Merchant settlement must calculate:

```text
Gross Sales
- Commission
- Payment Fees
- Refunds
- Adjustments
= Net Merchant Settlement
```

Settlement cycle options:

- weekly
- bi-weekly
- monthly

Merchant dashboard:

```text
Pending
Available
Paid
Held
Disputed
```

---

# 54. Anti-Fraud Engine

Rules:

### Customer

- excessive purchases
- repeated cancellations
- multiple accounts
- suspicious cards
- device fingerprint
- abnormal redemption velocity

### Merchant

- abnormal redemption rates
- self-redemption patterns
- repeated same-device transactions
- suspicious refund patterns
- coupon reselling

### Voucher

- duplicate redemption attempt
- invalid branch
- expired voucher
- impossible geographic movement
- multiple redemptions within seconds

---

# 55. Reviews

Only allow:

**verified purchasers**

to review an offer.

Review:

- rating
- comment
- optional photos

Merchant can:

- reply
- report

Admin can:

- moderate
- hide
- restore

---

# 56. Analytics

Track:

### Acquisition

- install
- visit
- registration
- first purchase

### Funnel

```text
Impression
 ↓
Offer View
 ↓
Add to Cart
 ↓
Checkout
 ↓
Payment Attempt
 ↓
Paid
 ↓
Redeemed
```

### Core KPIs

- GMV
- revenue
- AOV
- conversion rate
- CAC
- LTV
- repeat purchase rate
- redemption rate
- refund rate
- failed payment rate
- voucher failure rate
- merchant churn
- contribution margin

---

# 57. Event Tracking

Recommended event names:

```text
app_opened
location_selected
search_performed
category_viewed
offer_viewed
offer_favorited
cart_created
item_added
checkout_started
payment_started
payment_succeeded
payment_failed
voucher_viewed
voucher_redeemed
refund_requested
review_submitted
gift_purchased
cashback_earned
```

---

# 58. UI/UX Design Direction

## Visual personality

The interface should communicate:

**Savings + Energy + Trust + Local Discovery**

Recommended design language:

- strong price hierarchy
- large discount badge
- merchant imagery
- rounded cards
- clean white/neutral foundation
- one strong brand accent
- minimal visual clutter
- clear CTA buttons

---

# 59. Offer Card

Recommended structure:

```text
┌─────────────────────────────┐
│        IMAGE                │
│                         -40%│
├─────────────────────────────┤
│ Merchant Name               │
│ 2 Burgers + Fries           │
│ ★ 4.6   1.2 km              │
│                             │
│ EGP 500   EGP 299           │
│                             │
│ [BUY NOW]        ♡          │
└─────────────────────────────┘
```

The saving should be visually stronger than the original price.

---

# 60. Offer Details UX

Top:

```text
[Hero image]
-45%

EGP 299
instead of EGP 540

Save EGP 241
```

Then:

**What you get**

**How to use**

**Branches**

**Opening hours**

**Terms**

**Reviews**

Sticky CTA:

```text
[ BUY NOW — EGP 299 ]
```

---

# 61. Checkout UX Principle

Never hide the final amount.

Show:

```text
You save EGP 201
```

next to:

```text
Final price EGP 309
```

This reinforces the brand promise.

---

# 62. My Orders UX

Use clear status cards:

### ACTIVE

```text
Burger Deal
Valid until 20 Sep

[VIEW VOUCHER]
```

### USED

```text
Cinema Deal
Redeemed 12 Sep
```

### EXPIRING SOON

```text
Spa Package
Expires tomorrow

[VIEW]
```

---

# 63. Voucher Screen

This should be one of the simplest screens in the application.

```text
██████████████
 QR CODE
██████████████

Voucher #ABC123

2-for-1 Burger

Valid until:
20 September 2026

Branch:
Maadi

[SHOW CODE]

Need help?
[CONTACT SUPPORT]
```

No unnecessary UI.

No advertising.

No distracting navigation.

---

# 64. Merchant Redemption UX

Merchant app:

```text
       REDEEM

       [SCAN QR]

or

       Enter Code

------------------

Recent

✓ 1234 Redeemed
✓ 1235 Redeemed
```

After scan:

```text
VALID VOUCHER

2-for-1 Burger
Customer: Khaled

Branch:
Maadi

Value:
EGP 299

[CONFIRM REDEMPTION]
```

After confirmation:

```text
✓ SUCCESS

Voucher Redeemed

Transaction #88392
```

---

# 65. Mobile Navigation

Recommended:

```text
Home | Explore | Orders | Wallet | Profile
```

With a floating/central:

**Search**

or search embedded at top.

Do not create ten permanent bottom-nav tabs.

---

# 66. Personalization UX

During onboarding:

```text
What do you love?

☐ Food
☐ Cinema
☐ Kids
☐ Beauty
☐ Fitness
☐ Hotels
☐ Gaming
☐ Shopping
```

Then:

```text
Where do you usually go?

Cairo
Alexandria
...
```

This provides recommendation signals without requiring a long registration form.

Waffarha's recent registration changes similarly move toward personalization while deferring non-essential profile completion. 

---

# 67. Web Strategy

The website should not simply replicate the app.

Build SEO landing pages:

```text
/food/cairo
/food/cairo/maadi
/cinema/cairo
/hotels/ain-sokhna
/spa/cairo
/restaurant/{merchant}
/offer/{offer}
```

Each page should include:

- SEO title
- structured content
- merchant information
- price
- offers
- location
- FAQ
- internal links

This gives the business a long-term organic acquisition channel.

---

# 68. Admin Merchandising Engine

Admins should be able to configure:

### Homepage

```text
Hero #1
Hero #2
Hero #3

Section:
"Near You"

Rule:
distance < 10 km

Section:
"Trending"

Rule:
orders > threshold

Section:
"Best Value"

Rule:
discount > 40%
rating > 4
```

This avoids requiring engineering work for every homepage campaign.

---

# 69. Campaign Engine

Campaign supports:

```text
Campaign Name
Start
End
Target Audience
City
Category
Merchant
Minimum Order
Discount
Promo Code
Budget
Usage Limit
```

Target audience:

- new users
- returning users
- inactive users
- high-value customers
- location
- category affinity

---

# 70. Promo Code Engine

Support:

```text
WELCOME10
RAMADAN20
BANK15
TELCO25
```

Rules:

- percentage
- fixed amount
- category
- merchant
- minimum order
- first purchase
- user segment
- usage limit
- per-user limit
- expiration

---

# 71. B2B Partner Portal

Because the model can operate through partners such as telcos/banks, build a partner layer.

Partner capabilities:

- API access
- private offers
- eligibility rules
- customer entitlement
- campaign tracking
- reporting

Example:

```text
e& Customer
   ↓
My e& App
   ↓
Waffarha API
   ↓
Private Offer
   ↓
Voucher
   ↓
Merchant
```

Waffarha already demonstrates this type of B2B2C distribution through major partnerships, so this is strategically important for a next-generation implementation. 

---

# 72. API Security

Required:

- OAuth2 / JWT
- refresh tokens
- MFA for admins
- RBAC
- device/session management
- API rate limiting
- webhook signature verification
- encryption at rest
- TLS
- secrets management
- audit logs

---

# 73. Data Privacy

Support:

- consent management
- privacy policy
- marketing opt-in
- location permission
- data export
- account deletion
- notification opt-out

The platform should clearly distinguish:

**Required data**

from

**Personalization data**

rather than forcing unnecessary profile completion.

---

# 74. Performance Targets

Recommended:

### API

p95:

**< 300 ms**

for standard read APIs.

### Search

p95:

**< 500 ms**

### Checkout

Target:

**< 2 seconds before payment gateway interaction**

### App launch

Target:

**< 2.5 seconds perceived startup**

### Redemption

Target:

**< 2 seconds**

This is especially important for merchant-side operations.

---

# 75. Reliability Targets

Core components:

### Marketplace

99.9%

### Checkout

99.95%

### Voucher validation

99.99%

### Redemption

Highest priority.

A customer should not be denied access to an already-paid product because a non-critical service is temporarily unavailable.

---

# 76. MVP Scope

Do NOT build everything in phase one.

### MVP

Consumer:

- registration
- home
- search
- categories
- offers
- merchant pages
- location
- cart
- checkout
- cards/wallet
- orders
- vouchers
- QR redemption
- notifications
- support

Merchant:

- onboarding
- branches
- offer management
- redemption
- sales dashboard

Admin:

- merchant approval
- offer approval
- orders
- payments
- vouchers
- users
- CMS
- support
- reports

---

# 77. Phase 2

Add:

- wallet
- cashback
- gift vouchers
- bundles
- favorites
- reviews
- recommendation engine
- merchant analytics
- additional payment providers

---

# 78. Phase 3

Add:

- loyalty
- points
- leaderboard
- bus/ticketing
- health marketplace
- gaming cards
- B2B partner APIs
- corporate benefits

---

# 79. Phase 4

Add:

- AI recommendations
- predictive offers
- merchant campaign optimization
- dynamic pricing
- advanced fraud detection
- personalization engine
- autonomous merchandising

---

# 80. Recommended KPIs by Stakeholder

## CEO

- GMV
- net revenue
- active users
- transacting users
- merchant count
- repeat purchase rate

## CMO

- CAC
- conversion
- retention
- campaign ROI
- referral rate

## Marketplace Team

- active offers
- offer conversion
- merchant sell-through
- inventory utilization

## Operations

- voucher redemption success
- support tickets/order
- failed redemption
- refund rate

## Finance

- GMV
- take rate
- payment fees
- merchant settlement
- contribution margin

## Merchant

- orders
- revenue
- redemptions
- new customers
- repeat customers

---

# 81. North-Star Metric

The recommended north-star metric is:

## Successful Redeemed Transactions

Not:

- downloads
- page views
- coupons sold

A transaction is truly successful only when:

**customer paid + merchant accepted + service delivered**

This aligns the interests of all three sides.

---

# 82. Most Important Product Principle

The platform should optimize:

> **Discovery → Purchase → Redemption → Repeat Purchase**

rather than only:

> **Discovery → Purchase**

The redemption moment is the actual proof that marketplace value was delivered.

---

# 83. Recommended Product Architecture Summary

```text
                 CONSUMER
                    │
        ┌───────────┴───────────┐
        │                       │
      WEB                    MOBILE
        │                       │
        └───────────┬───────────┘
                    │
                 API GATEWAY
                    │
        ┌───────────┼─────────────┐
        │           │             │
    Discovery    Commerce      Identity
        │           │             │
    Search       Cart          Auth
    Offers       Orders        Profile
    Location     Payments      Preferences
    CMS          Vouchers
                 Wallet
                 Refunds
                    │
          ┌─────────┴─────────┐
          │                   │
      MERCHANT            PLATFORM
       PORTAL               ADMIN
          │                   │
          └─────────┬─────────┘
                    │
              INTEGRATIONS
                    │
       ┌────────────┼────────────┐
       │            │            │
   Payments       Maps       Messaging
       │            │            │
       └────────────┼────────────┘
                    │
                 ANALYTICS
```

---

# 84. Final Product Positioning

The strongest version of this platform should not market itself simply as:

**“Discounts.”**

The positioning should be:

> **One place to discover, save, buy, and enjoy more of what you love.**

The product architecture should therefore evolve toward:

**Deal Marketplace → Lifestyle Marketplace → Transaction Platform → Loyalty Ecosystem**

That is the scalable strategic direction.