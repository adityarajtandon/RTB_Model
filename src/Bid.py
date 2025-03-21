from BidRequest import BidRequest
from Bidder import Bidder
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import random

class Bid(Bidder):

    def __init__(self, total_budget, campaign_duration):
        self.total_budget = total_budget
        self.remaining_budget = total_budget
        self.q_table = {}

        # Load trained models
        self.dnn_ctr = load_model("/Users/adityarajtandon/Documents/RTB_MODEL/models/dnn_ctr_model.h5")
        self.dnn_cvr = load_model("/Users/adityarajtandon/Documents/RTB_MODEL/models/dnn_cvr_model.h5")


    def getBidPrice(self, bidRequest: BidRequest) -> int:
        """Determine the optimal bid price, ensuring we stop bidding if the budget is exhausted."""
        if self.remaining_budget <= 10:
            print("Budget exhausted. Stopping bids.")
            return -99  # Stop bidding when budget is exhausted

        features = np.array([bidRequest.getFeatures()]).astype(float)

        # Predict CTR, CVR
        pCTR = self.dnn_ctr.predict(features)[0][0]
        pCVR = self.dnn_cvr.predict(features)[0][0]

        # Get actual PayingPrice (fixing NoneType issue)
        paying_price = bidRequest.getPayingPrice()
        if paying_price is None:
            print(f"Skipping bid {bidRequest.bidId}: Missing PayingPrice.")
            return -1  # Skip this bid if PayingPrice is unavailable

        # Compute Expected Value
        expected_value = pCTR * (1 + 10 * pCVR)

        # Optimize bid price using Q-learning
        bidPrice = self.q_learning_optimizer(expected_value, paying_price)

        # **Ensure we only deduct budget if we win the bid**
        if bidPrice >= paying_price:
            if bidPrice > self.remaining_budget:
                print(f"Skipping bid: {bidPrice} exceeds remaining budget {self.remaining_budget}")
                return -1

            # Deduct the second-highest bid (actual PayingPrice) as per second-price auction
            self.remaining_budget -= paying_price
            print(f"Winning bid: {bidPrice}, Paying: {paying_price}, Remaining Budget: {self.remaining_budget}")
            return int(bidPrice)

        # If bid does not win, return -1 (no bid placed)
        print(f"Losing bid: {bidPrice} < Market Price: {paying_price}, No deduction.")
        return -1

    def q_learning_optimizer(self, expected_value, paying_price):
        """Optimize bid price using Q-learning with budget constraint."""
        state = (self.remaining_budget, expected_value, paying_price)
        
        # Ensure paying_price is valid before using it
        if paying_price is None:
            print("Error: PayingPrice is None in q_learning_optimizer.")
            return -1  # Skip invalid bids

        actions = [paying_price * 0.8, paying_price, paying_price * 1.2, paying_price * 1.5]

        # Initialize Q-table for this state if not exists
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in actions}

        epsilon = 0.1
        if random.uniform(0, 1) < epsilon:
            selected_action = random.choice(actions)
        else:
            selected_action = max(self.q_table[state], key=self.q_table[state].get)

        reward = expected_value - selected_action
        learning_rate = 0.1
        discount_factor = 0.9
        max_future_q = max(self.q_table[state].values())

        self.q_table[state][selected_action] += learning_rate * (reward + discount_factor * max_future_q - self.q_table[state][selected_action])

        return int(selected_action)
