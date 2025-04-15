from langchain_core.tools import tool
from typing import List
@tool
def addOrder(burger_count: int = 0, fries_count: int = 0, drink_count: int = 0) -> None:
   """Add an order to the system."""
   return

@tool
def deleteOrder(order_ids: List[int]) -> None:
   """Delete a orders from the system."""
   return

tools = [addOrder, deleteOrder]