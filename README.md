# RiskFlow

**Financial Risk & Compliance Analytics Platform**

RiskFlow is a full-stack financial analytics application that combines **ASP.NET Core** and **Python** to evaluate portfolio risk and apply configurable compliance rules.

The application uses **.NET as the primary business and API layer**, while a dedicated **Python FastAPI analytics service** performs quantitative portfolio analysis using libraries such as NumPy and Pandas.

The project demonstrates how multiple technologies can work together in a distributed system while maintaining clear separation of responsibilities.

---

## Overview

Financial applications often need both traditional business logic and specialized analytical processing.

RiskFlow separates these responsibilities into two services:

* **ASP.NET Core API** — manages users, clients, portfolios, holdings, persistence, business workflows, and compliance rules.
* **Python Analytics Service** — performs portfolio calculations, risk scoring, diversification analysis, and other quantitative operations.

The React frontend communicates with the ASP.NET Core API, while the .NET backend communicates with the Python analytics service through REST APIs.

---

## Architecture

```text
┌───────────────────────────────┐
│        React Frontend         │
│      React + TypeScript       │
└───────────────┬───────────────┘
                │
                │ REST API
                ▼
┌───────────────────────────────┐
│       ASP.NET Core API        │
│              C#               │
│                               │
│  • Client Management          │
│  • Portfolio Management       │
│  • Holdings                   │
│  • Compliance Rules           │
│  • Audit / Analysis Records   │
│  • Business Logic             │
└──────────┬─────────────┬──────┘
           │             │
           │             │ HTTP / REST
           ▼             ▼
┌─────────────────┐  ┌────────────────────────┐
│   SQL Server    │  │ Python Analytics API   │
│                 │  │       FastAPI          │
│ Entity Framework│  │                        │
│      Core       │  │ • NumPy                │
│                 │  │ • Pandas               │
│                 │  │ • Risk Calculations    │
└─────────────────┘  │ • Portfolio Analytics  │
                     └────────────────────────┘
```

---

# Tech Stack

## Frontend

* React
* TypeScript
* Vite
* CSS / Tailwind CSS

## Main Backend

* C#
* ASP.NET Core Web API
* Entity Framework Core
* RESTful APIs

## Analytics Service

* Python
* FastAPI
* NumPy
* Pandas

## Database

* SQL Server
* Azure SQL Database

## Testing

* xUnit
* pytest

## DevOps

* Git
* GitHub
* GitHub Actions
* Docker

## Cloud

* Microsoft Azure
* Azure SQL
* Azure App Service / Azure Container Apps

---

# MVP Features

RiskFlow V1 will focus on a small set of features.

## 1. Client Management

Users can create and view client profiles containing information such as:

* Name
* Age
* Risk tolerance
* Investment horizon
* Portfolio value

Example:

```json
{
  "name": "Demo Client",
  "age": 58,
  "riskTolerance": "Moderate",
  "investmentHorizonYears": 8
}
```

---

## 2. Portfolio Management

Each client can have a portfolio containing multiple holdings.

Example:

```json
{
  "portfolioName": "Retirement Portfolio",
  "holdings": [
    {
      "symbol": "TECH",
      "assetType": "Equity",
      "allocation": 45
    },
    {
      "symbol": "BOND",
      "assetType": "Bond",
      "allocation": 35
    },
    {
      "symbol": "CASH",
      "assetType": "Cash",
      "allocation": 20
    }
  ]
}
```

---

## 3. Python Risk Analysis

The ASP.NET Core API sends portfolio information to the Python analytics service.

Example request:

```http
POST /api/analytics/portfolio-risk
```

```json
{
  "holdings": [
    {
      "assetType": "Equity",
      "allocation": 45
    },
    {
      "assetType": "Bond",
      "allocation": 35
    },
    {
      "assetType": "Cash",
      "allocation": 20
    }
  ]
}
```

The Python service calculates metrics such as:

* Portfolio risk score
* Risk classification
* Diversification score
* Concentration risk
* Estimated volatility
* Portfolio warnings

Example response:

```json
{
  "riskScore": 67,
  "riskLevel": "High",
  "diversificationScore": 72,
  "estimatedVolatility": 0.16,
  "warnings": [
    "Portfolio contains a high allocation to equity assets."
  ]
}
```

---

# 4. Compliance Rules Engine

After receiving the Python analysis, the .NET backend evaluates the portfolio against business rules.

Example:

```text
Client Risk Tolerance:
Moderate

Portfolio Risk:
High

Result:
WARNING
```

Initial rules may include:

### Rule 1 — Risk Tolerance

A portfolio should not significantly exceed the client's declared risk tolerance.

### Rule 2 — Concentration

A single holding or asset category should not exceed a configured allocation threshold.

### Rule 3 — Investment Horizon

High-risk portfolios may not be appropriate for clients with short investment horizons.

### Rule 4 — Diversification

Poorly diversified portfolios should generate a warning.

### Rule 5 — Equity Exposure

Equity exposure may be restricted based on client risk characteristics.

---

# Compliance Results

RiskFlow will use three compliance statuses:

```text
PASS
WARNING
FAIL
```

Example:

```json
{
  "status": "WARNING",
  "riskScore": 67,
  "messages": [
    "Portfolio risk exceeds client risk tolerance.",
    "Technology equity concentration exceeds recommended threshold."
  ]
}
```

---

# Main Workflow

```text
Create Client
      ↓
Create Portfolio
      ↓
Add Holdings
      ↓
Run Risk Analysis
      ↓
ASP.NET Core sends portfolio to Python
      ↓
Python performs quantitative analysis
      ↓
Python returns risk metrics
      ↓
.NET evaluates compliance rules
      ↓
PASS / WARNING / FAIL
      ↓
Store analysis in SQL Server
      ↓
Display results in React
```

---

# Database Design

Initial entities:

```text
Client
Portfolio
Holding
RiskAnalysis
ComplianceResult
ComplianceViolation
```

Relationship overview:

```text
Client
  │
  └── Portfolio
        │
        ├── Holding
        │
        └── RiskAnalysis
              │
              └── ComplianceResult
                    │
                    └── ComplianceViolation
```

---

# Proposed Models

## Client

```text
Id
Name
Age
RiskTolerance
InvestmentHorizonYears
CreatedAt
```

## Portfolio

```text
Id
ClientId
Name
CreatedAt
UpdatedAt
```

## Holding

```text
Id
PortfolioId
Symbol
AssetType
AllocationPercentage
```

## RiskAnalysis

```text
Id
PortfolioId
RiskScore
RiskLevel
DiversificationScore
EstimatedVolatility
CreatedAt
```

## ComplianceResult

```text
Id
RiskAnalysisId
Status
CreatedAt
```

## ComplianceViolation

```text
Id
ComplianceResultId
RuleName
Severity
Message
```

---

# Proposed Repository Structure

```text
RiskFlow/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── backend/
│   ├── RiskFlow.Api/
│   ├── RiskFlow.Application/
│   ├── RiskFlow.Domain/
│   ├── RiskFlow.Infrastructure/
│   └── RiskFlow.Tests/
│
├── analytics/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── services/
│   │   └── routes/
│   │
│   ├── tests/
│   └── requirements.txt
│
├── docker/
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

# API Design

## Clients

```http
GET    /api/clients
GET    /api/clients/{id}
POST   /api/clients
PUT    /api/clients/{id}
DELETE /api/clients/{id}
```

## Portfolios

```http
GET    /api/portfolios/{id}
POST   /api/portfolios
PUT    /api/portfolios/{id}
DELETE /api/portfolios/{id}
```

## Holdings

```http
POST   /api/portfolios/{portfolioId}/holdings
PUT    /api/holdings/{id}
DELETE /api/holdings/{id}
```

## Analysis

```http
POST /api/portfolios/{portfolioId}/analyze
```

The .NET API internally communicates with:

```http
POST /api/analytics/portfolio-risk
```

on the Python FastAPI service.

---

# Testing Strategy

## .NET

xUnit will be used for:

* Business-rule testing
* Compliance-rule testing
* API testing
* Service-layer testing

Example:

```text
Given:
Client risk tolerance = Moderate

And:
Portfolio risk level = High

Expected:
Compliance result = WARNING or FAIL
```

---

## Python

pytest will be used for:

* Risk calculation tests
* Diversification tests
* Input validation
* Analytics API tests

---

# CI/CD

GitHub Actions will automatically:

```text
Push / Pull Request
        ↓
Build React
        ↓
Build .NET
        ↓
Run xUnit Tests
        ↓
Run Python Tests
        ↓
Build Docker Images
        ↓
Deploy
```

---

# Deployment

Planned Azure architecture:

```text
React Frontend
      │
      ▼
Azure Static Web Apps
      │
      ▼
ASP.NET Core API
Azure App Service
      │
      ├──────────────► Azure SQL
      │
      ▼
Python FastAPI
Azure Container Apps
```

The exact Azure services may change as the project evolves.

---

# Development Roadmap

## Phase 1 — Foundation

* [ ] Create repository structure
* [ ] Initialize React + TypeScript frontend
* [ ] Initialize ASP.NET Core API
* [ ] Initialize Python FastAPI service
* [ ] Configure SQL Server
* [ ] Configure Git

## Phase 2 — .NET Backend

* [ ] Create domain models
* [ ] Configure Entity Framework Core
* [ ] Create database migrations
* [ ] Create Client API
* [ ] Create Portfolio API
* [ ] Create Holding API

## Phase 3 — Python Analytics

* [ ] Create FastAPI application
* [ ] Create analytics request/response models
* [ ] Implement portfolio risk score
* [ ] Implement diversification score
* [ ] Implement concentration analysis
* [ ] Implement risk classification
* [ ] Add pytest tests

## Phase 4 — Service Integration

* [ ] Connect ASP.NET Core to FastAPI
* [ ] Send portfolio data from .NET to Python
* [ ] Receive analytics results
* [ ] Handle communication failures
* [ ] Store analysis results

## Phase 5 — Compliance Engine

* [ ] Implement risk tolerance rule
* [ ] Implement concentration rule
* [ ] Implement investment horizon rule
* [ ] Implement diversification rule
* [ ] Implement equity exposure rule
* [ ] Add xUnit tests

## Phase 6 — Frontend

* [ ] Client form
* [ ] Portfolio form
* [ ] Holdings interface
* [ ] Analysis button
* [ ] Risk result screen
* [ ] Compliance result screen

## Phase 7 — DevOps

* [ ] Dockerize ASP.NET Core API
* [ ] Dockerize Python service
* [ ] Configure Docker Compose
* [ ] Configure GitHub Actions
* [ ] Run automated tests in CI

## Phase 8 — Deployment

* [ ] Deploy database
* [ ] Deploy .NET API
* [ ] Deploy Python analytics service
* [ ] Deploy React frontend
* [ ] Configure production environment variables
* [ ] Test deployed application

---

# Future Improvements

Features outside the MVP may include:

* User authentication
* Advisor accounts
* Role-based authorization
* Historical market data
* Advanced portfolio volatility models
* Time-series forecasting
* Monte Carlo simulations
* Machine-learning-based risk models
* PDF compliance reports
* Configurable compliance rules
* Azure monitoring
* Audit logging
* AI-assisted portfolio explanations

These features are intentionally excluded from the initial MVP.

---

# Project Goals

RiskFlow is designed primarily as a software engineering and learning project demonstrating:

* Multi-service architecture
* C# and ASP.NET Core
* Python scientific computing
* RESTful API integration
* SQL Server
* Entity Framework Core
* React and TypeScript
* Automated testing
* Containerization
* CI/CD
* Azure deployment
* Financial technology concepts
* Clean separation between business logic and analytical workloads

---

# Disclaimer

RiskFlow is an educational software project.

All client profiles, portfolios, financial products, calculations, compliance rules, and datasets used by the application are synthetic or simulated.

RiskFlow does **not** provide financial, investment, legal, or regulatory advice and should not be used to make real financial decisions.

---

# Author

**Sushil Kumar Thanet**

GitHub: [GojoIsHere](https://github.com/GojoIsHere)

---

## Status

🚧 **In Development**

Initial development focuses on establishing communication between the React frontend, ASP.NET Core API, Python FastAPI analytics service, and SQL Server database.
