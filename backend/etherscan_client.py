"""
Etherscan API Client - V2 Compatible
"""

import os
import time
import requests
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class EtherscanClient:
    BASE_URL = "https://api.etherscan.io/v2/api"
    RATE_LIMIT_DELAY = 0.2
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ETHERSCAN_API_KEY", "YourApiKeyToken")
        self.session = requests.Session()
        self.last_call_time = 0
        
    def _rate_limit(self):
        elapsed = time.time() - self.last_call_time
        if elapsed < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - elapsed)
        self.last_call_time = time.time()
        
    def _make_request(self, params: Dict) -> Dict:
        self._rate_limit()
        params['apikey'] = self.api_key
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == '0' and data.get('message') == 'NOTOK':
                error_msg = data.get('result', 'Unknown error')
                raise Exception(f"Etherscan API Error: {error_msg}")
                
            return data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def get_account_balance(self, address: str) -> float:
        params = {
            'chainid': '1',
            'module': 'account',
            'action': 'balance',
            'address': address,
            'tag': 'latest'
        }
        data = self._make_request(params)
        balance_wei = int(data.get('result', '0'))
        return balance_wei / 1e18
    
    def get_normal_transactions(self, address: str, start_block: int = 0) -> List[Dict]:
        params = {
            'chainid': '1',
            'module': 'account',
            'action': 'txlist',
            'address': address,
            'startblock': start_block,
            'endblock': 99999999,
            'page': 1,
            'offset': 10000,
            'sort': 'asc'
        }
        data = self._make_request(params)
        result = data.get('result', [])
        return result if isinstance(result, list) else []
    
    def get_erc20_transfers(self, address: str) -> List[Dict]:
        params = {
            'chainid': '1',
            'module': 'account',
            'action': 'tokentx',
            'address': address,
            'startblock': 0,
            'endblock': 99999999,
            'page': 1,
            'offset': 10000,
            'sort': 'asc'
        }
        data = self._make_request(params)
        result = data.get('result', [])
        return result if isinstance(result, list) else []
    
    def get_full_wallet_data(self, address: str) -> Dict:
        print(f"Fetching data for wallet: {address}")
        
        data = {
            'address': address,
            'balance': self.get_account_balance(address),
            'normal_txns': self.get_normal_transactions(address),
            'erc20_transfers': self.get_erc20_transfers(address),
            'fetched_at': datetime.now().isoformat()
        }
        
        print(f"Fetched {len(data['normal_txns'])} transactions")
        return data
