# ArchCostEstimator

**Cloud Cost Intelligence Platform for Pre-Startup Architecture Planning**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Overview

ArchCostEstimator is a comprehensive cloud cost estimation tool that helps you make informed architectural decisions before committing to infrastructure. Get accurate cost projections across 17+ cloud providers with detailed CapEx and OpEx insights.

## Features

### Core Capabilities
- **Multi-Cloud Comparison**: Compare costs across 17+ providers including AWS, Azure, GCP, DigitalOcean, and more
- **Architecture-Based Estimation**: Optimized calculations for Monolith, Microservices, and Serverless architectures
- **Real-Time Pricing**: Auto-updated pricing data from official provider APIs
- **Business Metrics**: OpEx/CapEx analysis, cost-per-user, ROI projections
- **3-Year Forecasting**: Growth-adjusted cost projections with configurable growth rates

### Export & Collaboration
- **PDF Export**: Professional reports with charts and breakdowns
- **CSV Export**: Raw data for custom analysis
- **URL Sharing**: Share configurations with team via URL parameters

### User Experience
- **Interactive Onboarding**: First-time user tour
- **Contextual Help**: Searchable FAQ and documentation
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Accessibility**: WCAG 2.1 AA compliant

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+ (for backend)
- Docker & Docker Compose (optional, for containerized deployment)

### Local Development

**Frontend:**
```bash
cd frontend
npm install
ng serve
# App runs at http://localhost:4200
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# API runs at http://localhost:8000
```

### Production Deployment

```bash
docker-compose -f docker-compose.prod.yml up -d
```

See [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) for detailed deployment instructions.

## Technology Stack

**Frontend:**
- Angular 17
- Tailwind CSS + Custom Design System
- TypeScript
- RxJS for reactive programming

**Backend:**
- FastAPI (Python)
- MongoDB for pricing data
- Redis for caching
- Official cloud provider APIs

## Documentation

- **[User Guide](USER_GUIDE.md)** - How to use ArchCostEstimator
- **[Implementation Plan](C:\Users\bhatn\.gemini\antigravity\brain\8f9c9d3c-b0e8-495f-8a40-f96ccb2f3fe3\implementation_plan.md)** - Development roadmap
- **[Accessibility Testing](C:\Users\bhatn\.gemini\antigravity\brain\8f9c9d3c-b0e8-495f-8a40-f96ccb2f3fe3\accessibility-testing.md)** - A11y compliance guide
- **[Walkthrough](C:\Users\bhatn\.gemini\antigravity\brain\8f9c9d3c-b0e8-495f-8a40-f96ccb2f3fe3\walkthrough.md)** - Recent implementations

## Architecture

```
archcost/
├── frontend/          # Angular app
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/
│   │   │   │   ├── shared/        # Reusable components
│   │   │   │   │   ├── tooltip/
│   │   │   │   │   ├── help-modal/
│   │   │   │   │   └── onboarding/
│   │   │   │   ├── home/
│   │   │   │   └── ...
│   │   │   └── services/
│   │   ├── design-system.css      # Design tokens & components
│   │   └── styles.css
│   └── angular.json
│
├── backend/           # FastAPI server
│   ├── main.py
│   ├── estimation_service.py
│   ├── pricing_fetcher.py
│   └── requirements.txt
│
└── docker-compose.prod.yml
```

## Design System

ArchCostEstimator uses a comprehensive design system for consistency:

- **10 Color Scales**: Primary, secondary, accent, success, warning, error, info
- **Typography**: Inter font family with 9 size scales
- **Spacing**: 20+ consistent spacing tokens
- **Components**: Pre-built buttons, forms, cards, badges, tooltips

See [`design-system.css`](frontend/src/design-system.css) for details.

## API Reference

**Base URL:** `https://archcostestimator.com/api` (production) or `http://localhost:8000` (local)

### Endpoints

**POST /api/estimate**
```json
{
  "traffic": {
    "daily_active_users": 10000,
    "api_requests_per_user": 50,
    "storage_per_user_mb": 10
  },
  "architecture": "microservices",
  "currency": "USD"
}
```

**GET /api/providers**  
Returns list of supported cloud providers

**GET /api/pricing-status**  
Returns last pricing update timestamp

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow Angular style guide for frontend
- Use PEP 8 for backend Python code
- Write tests for new features
- Update documentation as needed

## Testing

**Functional Testing:**
```bash
# Frontend
ng test

# Backend
pytest
```

**Accessibility Testing:**
```bash
npm install -g pa11y
pa11y http://localhost:4200
```

See [Accessibility Testing Guide](C:\Users\bhatn\.gemini\antigravity\brain\8f9c9d3c-b0e8-495f-8a40-f96ccb2f3fe3\accessibility-testing.md) for detailed procedures.

## Performance

**Target Metrics:**
- Lighthouse Performance Score: 90+
- Lighthouse Accessibility Score: 95+
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s

**Optimization Features:**
- Debounced calculations (300ms)
- Lazy-loaded routes
- Optimized production builds
- PWA support for offline access

## Browser Support

| Browser | Version |
|---------|---------|
| Chrome | 90+ |
| Firefox | 88+ |
| Safari | 14+ |
| Edge | 90+ |
| iOS Safari | 14+ |
| Android Chrome | 90+ |

## SEO

ArchCostEstimator is optimized for search engines with:
- Comprehensive meta tags
- Open Graph & Twitter Cards
- JSON-LD structured data
- Semantic HTML
- Sitemap & robots.txt

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: See [USER_GUIDE.md](USER_GUIDE.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/archcost/issues)
- **Contact**: [Contact Page](/contact-us)

## Roadmap

### Q1 2025
- [x] Design system implementation
- [x] Help modal & onboarding
- [x] SEO & PWA support
- [ ] Infrastructure-as-Code import (Terraform, CloudFormation)
- [ ] Quick estimate mode

### Q2 2025
- [ ] Comparison tool (side-by-side configurations)
- [ ] Enhanced PDF reports with branding
- [ ] Email export
- [ ] Cost alerts & monitoring integration

## Acknowledgments

- Cloud pricing data from official provider APIs
- Icons from [Heroicons](https://heroicons.com)
- Font: [Inter](https://rsms.me/inter/)

---

**Built with ❤️ for the cloud architecture community**

*Last Updated: December 2025 | Version: 1.1*
