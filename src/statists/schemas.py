from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class PriceTrendRequest(BaseModel):
    seller_id: int
    start_date: datetime
    end_date: datetime
    product_ids: Optional[List[int]] = None
