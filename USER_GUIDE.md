# ArchCostEstimator User Guide

## Welcome to ArchCostEstimator! 👋

ArchCostEstimator is your go-to tool for estimating cloud infrastructure costs across 17+ providers before you commit to an architecture. Get accurate CapEx and OpEx insights to make informed decisions.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Understanding Architecture Types](#understanding-architecture-types)
3. [Configuration Guide](#configuration-guide)
4. [Interpreting Results](#interpreting-results)
5. [Export & Sharing](#export--sharing)
6. [FAQs](#faqs)
7. [Troubleshooting](#troubleshooting)
8. [Glossary](#glossary)

---

## Getting Started

### Quick Start (3 minutes)

1. **Select Your Architecture**
   -Choose from Monolith, Microservices, or Serverless
   - Each architecture has different cost implications

2. **Configure Requirements**
   - Enter expected daily active users
   - Specify storage and traffic needs
   - Add advanced features if needed

3. **View Results**
   - See cost breakdowns across all providers
   - Compare monthly, yearly, and 3-year projections
   - Review optimization suggestions

### First-Time User Tour

If this is your first time, our interactive onboarding will guide you through the key features. You can restart the tour anytime from the Help menu.

---

## Understanding Architecture Types

### Monolith
**Best for:** Startups, MVPs, small teams

**Characteristics:**
- Single codebase
- Simple deployment
- Lower operational complexity
- Easier debugging
- Vertical scaling

**Cost Implications:**
- Lower initial infrastructure costs
- Simpler monitoring needs
- Fewer moving parts = fewer services to pay for

**When to choose:**
- Team size < 10 developers
- Simple domain model
- Fast time to market is priority
- Limited DevOps expertise

---

### Microservices
**Best for:** Growing companies, complex domains

**Characteristics:**
- Decoupled services
- Independent deployment
- Technology diversity
- Horizontal scaling
- Higher operational complexity

**Cost Implications:**
- Higher infrastructure costs (multiple services)
- More complex monitoring and logging
- Container orchestration costs (Kubernetes, ECS)
- API gateway and service mesh costs

**When to choose:**
- Team size > 10 developers
- Complex business domain
- Need for independent scaling
- Different technology requirements per service

---

### Serverless
**Best for:** Variable workloads, event-driven apps

**Characteristics:**
- Pay-per-use pricing
- Auto-scaling
- Zero infrastructure management
- Event-driven architecture
- Vendor lock-in risk

**Cost Implications:**
- Cost-effective for variable traffic
- No infrastructure management costs
- Cold start considerations
- Can be expensive at high scale

**When to choose:**
- Unpredictable or variable traffic
- Event-driven workflows
- Want zero infrastructure management
- Rapid prototyping

---

## Configuration Guide

See the in-app help modal for detailed configuration guidance.

---

## Interpreting Results

### Cost Summary Cards

**Monthly Cost** - Your expected monthly bill based on pay-as-you-go pricing
**Cost Per User** - Monthly cost divided by DAU
**3-Year Projection** - Assumes 20% annual growth

### Provider Comparison

The best value provider for your configuration is highlighted with a "Best Value" badge.

---

## Export & Sharing

- **PDF**: Complete cost breakdown with charts
- **CSV**: Raw data for analysis
- **URL**: Share configuration with team

---

## FAQs

**Q: Is ArchCostEstimator free?**
A: Yes, completely free. No signup required.

**Q: How accurate are the estimates?**
A: We use official pricing APIs. Accuracy is typically within 5-10%.

**Q: Do you store my data?**
A: No. All calculations happen in your browser.

---

## Glossary

**CapEx** -Capital Expenditure. Upfront infrastructure costs.
**OpEx** - Operational Expenditure. Ongoing cloud service costs.
**CDN** - Content Delivery Network for faster content delivery.
**Egress** - Data transferred out of cloud provider's network.

---

*Last Updated: December 2025 | Version: 1.1*
