import json
import time
from typing import Any, Dict
from datetime import datetime

def load_test_data(file_path: str) -> Any:
    """Load test data from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_response(response_data: Dict, filename: str) -> None:
    """Save API response to file for debugging"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename}_{timestamp}.json"
    
    with open(f"debug/{filename}", 'w', encoding='utf-8') as file:
        json.dump(response_data, file, indent=2)

def validate_response_time(response, max_time_ms: int = 1000) -> bool:
    """Validate response time meets requirements"""
    return response.elapsed.total_seconds() * 1000 <= max_time_ms

def generate_test_description(test_name: str, **kwargs) -> str:
    """Generate dynamic test descriptions"""
    if kwargs:
        params = ', '.join(f"{k}={v}" for k, v in kwargs.items())
        return f"{test_name} [{params}]"
    return test_name