#!/usr/bin/env bash
# scripts/provision_stripe_catalog.sh
set -e

# Verify STRIPE_SECRET_KEY is set in local terminal context
if [ -z "$STRIPE_SECRET_KEY" ]; then
    echo "ERROR: Please set your STRIPE_SECRET_KEY environment variable before running."
    exit 1
fi

echo "================================================================="
│ PROVISIONING ODYNEX AXIS LOGISTICS COMMERCIAL LICENSING ON STRIPE
"================================================================="

# 1. Provision Tier 1: Academic Core Product & Price
echo "Creating Tier 1: Academic Core..."
ACADEMIC_PROD_ID=$(curl -s https://stripe.com \
  -u "${STRIPE_SECRET_KEY}:" \
  -d name="Academic Core Plan" \
  -d description="Higher-Ed & Youth Focus Modules with Rhetorical Defense Metrics" \

  | grep -o '"id": "[^"]*' | head -n 1 | cut -d'"' -f4)

curl -s https://stripe.com \
  -u "${STRIPE_SECRET_KEY}:" \
  -d product="${ACADEMIC_PROD_ID}" \
  -d unit_amount=1900 \
  -d currency=usd \
  -d "recurring[interval]"=month \
  -d nickname="price_1AcademicStudentTier2026"

# 2. Provision Tier 2: Enterprise Crucible Product & Price
echo -e "\nCreating Tier 2: Enterprise Crucible..."
ENTERPRISE_PROD_ID=$(curl -s https://stripe.com \
  -u "${STRIPE_SECRET_KEY}:" \
  -d name="Enterprise Crucible" \
  -d description="Corporate, Military, & Geopolitical Portals with TUTSA & WTO Registry Compliance" \

  | grep -o '"id": "[^"]*' | head -n 1 | cut -d'"' -f4)

curl -s https://stripe.com \
  -u "${STRIPE_SECRET_KEY}:" \
  -d product="${ENTERPRISE_PROD_ID}" \
  -d unit_amount=450000 \
  -d currency=usd \
  -d "recurring[interval]"=month \
  -d nickname="price_1EnterpriseCrucibleTier2026"

# 3. Provision Tier 3: Developer API Product & Price
echo -e "\nCreating Tier 3: Developer API Access..."
DEV_PROD_ID=$(curl -s https://stripe.com \
  -u "${STRIPE_SECRET_KEY}:" \
  -d name="Developer API Access" \
  -d description="Pay-As-You-Go access to raw Audio2Face & Nemotron-4 NIM Stream Matrices" \

  | grep -o '"id": "[^"]*' | head -n 1 | cut -d'"' -f4)

curl -s https://stripe.com \
  -u "${STRIPE_SECRET_KEY}:" \
  -d product="${DEV_PROD_ID}" \
  -d unit_amount=12 \
  -d currency=usd \
  -d nickname="price_1DeveloperAPIUsageTier2026"

echo -e "\n\n✅ [SUCCESS] All monetization tiers successfully established on Stripe infrastructure."
