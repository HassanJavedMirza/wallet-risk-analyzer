"""
FastAPI Backend for Wallet Risk Analyzer
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import Dict
from datetime import datetime
import os

from etherscan_client import EtherscanClient
from feature_extractor import WalletFeatureExtractor
from risk_model import WalletRiskModel


app = FastAPI(
    title="Wallet Risk Analyzer API",
    description="AI-powered fraud risk assessment for Ethereum wallets",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

etherscan_client = EtherscanClient()
feature_extractor = WalletFeatureExtractor()
risk_model = WalletRiskModel()


class AnalyzeRequest(BaseModel):
    wallet_address: str
    
    @validator('wallet_address')
    def validate_address(cls, v):
        if not v.startswith('0x') or len(v) != 42:
            raise ValueError('Invalid Ethereum address format')
        return v.lower()


class RiskAnalysisResponse(BaseModel):
    wallet_address: str
    risk_score: int
    risk_level: str
    risk_factors: list
    transaction_stats: Dict
    analysis_timestamp: str
    cached: bool


class HealthResponse(BaseModel):
    status: str
    timestamp: str


@app.get("/")
async def root():
    return {
        "service": "Wallet Risk Analyzer API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "analyze": "/api/v1/analyze",
            "health": "/api/v1/health",
            "docs": "/docs"
        }
    }


@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat()
    )


@app.post("/api/v1/analyze", response_model=RiskAnalysisResponse)
async def analyze_wallet(request: AnalyzeRequest):
    address = request.wallet_address
    
    try:
        print(f"Analyzing wallet: {address}")
        wallet_data = etherscan_client.get_full_wallet_data(address)
        
        features = feature_extractor.extract_all_features(wallet_data)
        risk_prediction = risk_model.predict_risk(features)
        
        transaction_stats = {
            'balance': round(features['balance'], 6),
            'total_transactions': features['total_txns'],
            'transaction_frequency': features['txn_frequency'],
            'account_age_days': features['account_age_days'],
            'unique_addresses': features['unique_addresses'],
            'token_transfers': features['token_transfer_count'],
            'contract_interactions': features['contract_interaction_count']
        }
        
        result = {
            'wallet_address': address,
            'risk_score': risk_prediction['risk_score'],
            'risk_level': risk_prediction['risk_level'],
            'risk_factors': risk_prediction['risk_factors'],
            'transaction_stats': transaction_stats,
            'analysis_timestamp': datetime.now().isoformat(),
            'cached': False
        }
        
        return RiskAnalysisResponse(**result)
        
    except Exception as e:
        print(f"Analysis error for {address}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.on_event("startup")
async def startup_event():
    print("🚀 Wallet Risk Analyzer API starting...")
    print("✅ API ready at http://0.0.0.0:8000")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
