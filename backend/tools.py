from langchain_core.tools import tool

@tool
def addOrder(burger_count: int = 0, fries_count: int = 0, drink_count: int = 0) -> None:
   """Add an order to the system."""
   return

@tool
def deleteOrder(order_id: int) -> None:
   """Delete an order from the system."""
   return

tools = [addOrder, deleteOrder]