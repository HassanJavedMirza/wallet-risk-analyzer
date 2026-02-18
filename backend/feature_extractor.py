"""
Feature Engineering for Wallet Risk Analysis
"""

import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List
from collections import Counter


class WalletFeatureExtractor:
    
    @staticmethod
    def _parse_timestamp(timestamp_str: str) -> datetime:
        try:
            return datetime.fromtimestamp(int(timestamp_str))
        except (ValueError, TypeError):
            return datetime.now()
    
    @staticmethod
    def _wei_to_eth(wei_str: str) -> float:
        try:
            return int(wei_str) / 1e18
        except (ValueError, TypeError):
            return 0.0
    
    def extract_transaction_features(self, transactions: List[Dict]) -> Dict:
        if not transactions:
            return {
                'total_txns': 0,
                'txn_frequency': 0,
                'avg_txn_value': 0,
                'txn_value_variance': 0,
                'max_txn_value': 0,
                'incoming_txn_ratio': 0,
                'unique_addresses': 0,
                'account_age_days': 0,
                'avg_gas_price': 0,
                'failed_txn_ratio': 0
            }
        
        df = pd.DataFrame(transactions)
        df['timestamp'] = df['timeStamp'].apply(self._parse_timestamp)
        df['value_eth'] = df['value'].apply(self._wei_to_eth)
        df['gasPrice'] = df['gasPrice'].apply(lambda x: int(x) / 1e9)
        
        first_txn = df['timestamp'].min()
        account_age_days = (datetime.now() - first_txn).days
        
        if account_age_days > 0:
            txn_frequency = len(df) / account_age_days
        else:
            txn_frequency = len(df)
        
        avg_txn_value = df['value_eth'].mean()
        txn_value_variance = df['value_eth'].var()
        max_txn_value = df['value_eth'].max()
        
        incoming_txns = df[df['to'].str.lower() == df.iloc[0]['to'].lower()].shape[0]
        incoming_txn_ratio = incoming_txns / len(df) if len(df) > 0 else 0
        
        unique_addresses = len(set(df['from'].tolist() + df['to'].tolist()))
        avg_gas_price = df['gasPrice'].mean()
        
        failed_txns = df[df['isError'] == '1'].shape[0] if 'isError' in df.columns else 0
        failed_txn_ratio = failed_txns / len(df) if len(df) > 0 else 0
        
        return {
            'total_txns': len(df),
            'txn_frequency': round(txn_frequency, 4),
            'avg_txn_value': round(avg_txn_value, 6),
            'txn_value_variance': round(txn_value_variance, 6),
            'max_txn_value': round(max_txn_value, 6),
            'incoming_txn_ratio': round(incoming_txn_ratio, 4),
            'unique_addresses': unique_addresses,
            'account_age_days': account_age_days,
            'avg_gas_price': round(avg_gas_price, 2),
            'failed_txn_ratio': round(failed_txn_ratio, 4)
        }
    
    def extract_token_features(self, erc20_transfers: List[Dict]) -> Dict:
        if not erc20_transfers:
            return {
                'token_transfer_count': 0,
                'unique_tokens': 0,
                'token_diversity_score': 0
            }
        
        df = pd.DataFrame(erc20_transfers)
        unique_tokens = df['tokenSymbol'].nunique() if 'tokenSymbol' in df.columns else 0
        
        if 'tokenSymbol' in df.columns:
            token_counts = Counter(df['tokenSymbol'])
            total = sum(token_counts.values())
            probs = [count/total for count in token_counts.values()]
            diversity_score = -sum(p * np.log2(p) for p in probs if p > 0)
        else:
            diversity_score = 0
        
        return {
            'token_transfer_count': len(df),
            'unique_tokens': unique_tokens,
            'token_diversity_score': round(diversity_score, 4)
        }
    
    def extract_all_features(self, wallet_data: Dict) -> Dict:
        features = {
            'address': wallet_data['address'],
            'balance': wallet_data['balance']
        }
        
        txn_features = self.extract_transaction_features(wallet_data.get('normal_txns', []))
        features.update(txn_features)
        
        token_features = self.extract_token_features(wallet_data.get('erc20_transfers', []))
        features.update(token_features)
        
        features['contract_interaction_count'] = 0
        features['unique_contracts'] = 0
        
        features['is_new_account'] = 1 if features['account_age_days'] < 30 else 0
        features['high_frequency'] = 1 if features['txn_frequency'] > 10 else 0
        features['high_variance'] = 1 if features['txn_value_variance'] > 1 else 0
        
        return features
