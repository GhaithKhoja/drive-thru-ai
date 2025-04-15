import unittest
from ai import AI

class TestAIOrderSystem(unittest.TestCase):
    def setUp(self):
        # In-memory order system for testing
        self.orders = []
        self.order_id_counter = 1
        self.ai = AI()

    def add_order(self, burger_count, fries_count, drink_count):
        order = {
            "id": self.order_id_counter,
            "burger_count": burger_count,
            "fries_count": fries_count,
            "drink_count": drink_count
        }
        self.orders.append(order)
        self.order_id_counter += 1
        return order["id"]

    def delete_order(self, order_ids):
        self.orders = [order for order in self.orders if order["id"] not in order_ids]

    def test_add_order(self):
        prompt = "I want to order 2 burgers, 1 fries, and 1 drink."
        response = self.ai.generate_response(prompt)
        self.assertIn("addOrder", response)
        self.assertEqual(response["addOrder"]["burger_count"], 2)
        self.assertEqual(response["addOrder"]["fries_count"], 1)
        self.assertEqual(response["addOrder"]["drink_count"], 1)
        # Simulate adding the order
        order_id = self.add_order(**response["addOrder"])
        self.assertEqual(len(self.orders), 1)
        self.assertEqual(self.orders[0]["id"], order_id)

    def test_delete_order(self):
        # Simulate adding an order
        order_id = self.add_order(1, 1, 1)
        self.assertEqual(len(self.orders), 1)
        # Simulate AI response for deleting the order
        # Let's pretend the user says "Cancel my order with id X"
        prompt = f"Cancel my order with id {order_id}"
        response = self.ai.generate_response(prompt)
        self.assertIn("deleteOrder", response)
        self.assertIn(order_id, response["deleteOrder"]["order_ids"])
        # Simulate deleting the order
        self.delete_order(response["deleteOrder"]["order_ids"])
        self.assertEqual(len(self.orders), 0)

    def test_multiple_orders(self):
        prompts = [
            "I'd like 1 burger and 2 drinks.",
            "Add 3 fries and 2 burgers to my order.",
            "Order 2 fries, 1 drink, and 1 burger."
        ]
        for prompt in prompts:
            response = self.ai.generate_response(prompt)
            self.assertIn("addOrder", response)
            self.add_order(**response["addOrder"])
        self.assertEqual(len(self.orders), 3)

    def test_mixed_actions(self):
        # Add two orders
        id1 = self.add_order(1, 1, 1)
        id2 = self.add_order(2, 2, 2)
        prompt = f"Add 1 burger and cancel order {id2}."
        response = self.ai.generate_response(prompt)
        self.assertIn("addOrder", response)
        self.assertIn("deleteOrder", response)
        self.add_order(**response["addOrder"])
        self.delete_order(response["deleteOrder"]["order_ids"])
        self.assertEqual(len(self.orders), 2)

if __name__ == "__main__":
    unittest.main() 