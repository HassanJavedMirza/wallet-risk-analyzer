"""
Machine Learning Risk Scoring Model
"""

import numpy as np
from typing import Dict, List


class WalletRiskModel:
    
    def __init__(self):
        self.is_trained = False
    
    def predict_risk(self, features: Dict) -> Dict:
        return self._rule_based_prediction(features)
    
    def _rule_based_prediction(self, features: Dict) -> Dict:
        risk_score = 0
        risk_factors = []
        
        if features.get('is_new_account', 0) == 1 and features.get('total_txns', 0) > 50:
            risk_score += 30
            risk_factors.append("New account with high activity")
        
        if features.get('txn_frequency', 0) > 10:
            risk_score += 20
            risk_factors.append("High transaction frequency")
        
        if features.get('high_variance', 0) == 1:
            risk_score += 15
            risk_factors.append("High transaction value volatility")
        
        if features.get('failed_txn_ratio', 0) > 0.1:
            risk_score += 25
            risk_factors.append("High failed transaction ratio")
        
        if features.get('incoming_txn_ratio', 0) > 0.7 and features.get('total_txns', 0) > 20:
            risk_score += 25
            risk_factors.append("Mixer-like behavior pattern")
        
        risk_score = min(risk_score, 100)
        
        if risk_score >= 67:
            risk_level = "high"
        elif risk_score >= 34:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        if not risk_factors:
            risk_factors = ["No significant risk factors detected"]
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors
        }
