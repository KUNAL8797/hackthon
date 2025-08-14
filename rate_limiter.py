# rate_limiter.py
import asyncio
import time
from typing import Optional

class GeminiRateLimiter:
    def __init__(self, requests_per_minute: int = 15):
        self.requests_per_minute = requests_per_minute
        self.min_interval = 60.0 / requests_per_minute
        self.last_request_time: Optional[float] = None
        
    async def wait_if_needed(self) -> None:
        """
        Wait if necessary to respect rate limits
        """
        current_time = time.time()
        
        if self.last_request_time is not None:
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < self.min_interval:
                wait_time = self.min_interval - time_since_last
                print(f"⏱️ Rate limiting: waiting {wait_time:.1f}s...")
                await asyncio.sleep(wait_time)
        
        self.last_request_time = time.time()
