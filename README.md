# 🔐 Crypto Wallet Risk Analyzer

**AI-powered fraud risk assessment for Ethereum wallets**

A production-grade system that analyzes on-chain behavior patterns to detect potentially fraudulent Ethereum wallets. Built with FastAPI, Machine Learning, and real-time Etherscan data.

---

## 🎯 What It Does

- **Analyzes any Ethereum wallet address** for fraud risk patterns
- **ML-powered risk scoring** (0-100 scale) with explainable factors
- **Real-time on-chain data** from Etherscan API
- **Sub-3-second response time** with Redis caching
- **Production-ready** with Docker containerization

### Risk Detection Patterns
- New accounts with suspicious activity
- Mixer-like transaction patterns
- High transaction volatility
- Abnormal gas price usage
- Failed transaction ratios
- Contract interaction analysis

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI + Uvicorn |
| ML/AI | Scikit-learn (Random Forest) |
| Data Pipeline | Pandas + NumPy |
| Cache | Redis |
| APIs | Etherscan, CoinGecko |
| Deployment | Docker + Docker Compose |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Etherscan API key ([Get free key](https://etherscan.io/myapikey))

### 1. Clone & Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd wallet-risk-analyzer

# Copy environment template
cp .env.example .env

# Add your Etherscan API key to .env
nano .env  # Or use your preferred editor
```

### 2. Run with Docker (Recommended)

```bash
# Build and start all services
docker-compose up --build

# API will be available at http://localhost:8000
```

### 3. Run Locally (Development)

```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis (required)
docker run -d -p 6379:6379 redis:7-alpine

# Run the API
cd backend
python main.py
```

---

## 📡 API Usage

### Analyze a Wallet

**Endpoint:** `POST /api/v1/analyze`

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"wallet_address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"}'
```

**Response:**
```json
{
  "wallet_address": "0xd8da6bf26964af9d7eed9e03e53415d37aa96045",
  "risk_score": 15,
  "risk_level": "low",
  "risk_factors": [
    "No significant risk factors detected"
  ],
  "transaction_stats": {
    "balance": 0.234567,
    "total_transactions": 1234,
    "transaction_frequency": 3.45,
    "account_age_days": 357,
    "unique_addresses": 567,
    "token_transfers": 89,
    "contract_interactions": 23
  },
  "analysis_timestamp": "2024-02-18T12:34:56",
  "cached": false
}
```

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

### Interactive API Docs

Visit **http://localhost:8000/docs** for Swagger UI

---

## 🧪 Testing

### Test the API

```bash
# Test with a known wallet (Vitalik's address)
python test_api.py
```

### Test Individual Components

```bash
# Test Etherscan client
cd backend
python etherscan_client.py

# Test feature extraction
python feature_extractor.py

# Test ML model
python risk_model.py
```

---

## 🏗️ Project Structure

```
wallet-risk-analyzer/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── etherscan_client.py     # Etherscan API client
│   ├── feature_extractor.py    # ML feature engineering
│   └── risk_model.py           # Random Forest classifier
├── models/
│   └── risk_model.joblib       # Trained model (auto-generated)
├── frontend/                   # React dashboard (Phase 2)
├── data/                       # Sample data
├── Dockerfile                  # Backend container
├── docker-compose.yml          # Full stack orchestration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md
```

---

## 🎨 Frontend Dashboard (Coming Soon)

React + Next.js dashboard featuring:
- Wallet address input
- Risk score gauge visualization
- Transaction timeline charts
- Risk factors breakdown
- Export to PDF

---

## 🔒 Security Notes

- **API Key Protection**: Never commit `.env` file to Git
- **Rate Limiting**: Etherscan free tier = 5 calls/sec
- **Caching**: 24-hour TTL reduces API load
- **Input Validation**: All wallet addresses are validated

---

## 📈 Performance

- **API Response Time**: < 3 seconds (including Etherscan calls)
- **Cache Hit Rate**: > 60% after initial usage
- **ML Inference**: < 100ms
- **Concurrent Requests**: Tested up to 50 simultaneous

---

## 🚧 Roadmap

**Phase 1** (Current):
- ✅ Etherscan data pipeline
- ✅ Feature extraction
- ✅ ML risk model
- ✅ FastAPI backend
- ✅ Docker deployment

**Phase 2** (Next):
- [ ] React dashboard
- [ ] Real-time WebSocket updates
- [ ] Multi-chain support (BSC, Polygon)
- [ ] Historical risk tracking
- [ ] PDF report generation

**Phase 3** (Future):
- [ ] Advanced ML models (XGBoost, Neural Networks)
- [ ] Known scam contract database
- [ ] Email alerts for high-risk wallets
- [ ] Premium tier with extended analytics

---

## 🤝 Contributing

This is a portfolio project showcasing production-grade AI engineering. Feel free to fork and adapt for your use case.

---

## 📄 License

MIT License - See LICENSE file

---

## 👤 Author

**Hassan Javed Mirza**  
AI Engineer | FastAPI · ML Pipelines · Computer Vision

- Portfolio: [Your Portfolio URL]
- LinkedIn: [linkedin.com/in/hassan-javed-116381247](https://linkedin.com/in/hassan-javed-116381247)
- GitHub: [github.com/HassanJavedMirza](https://github.com/HassanJavedMirza)

---

## 🙏 Acknowledgments

- Etherscan for blockchain data API
- Scikit-learn for ML framework
- FastAPI for modern Python API framework

---

**Built with ❤️ for the Web3 community**
