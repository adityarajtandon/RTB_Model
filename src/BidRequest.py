import pandas as pd
class BidRequest:
    """ Represents a single bid request and stores all relevant bid attributes. """

    def __init__(self, bid_data):
        """Initialize bid request attributes from raw bid data."""

        # Extract primary bid details
        self.bidId = bid_data["BidID"]
        self.timestamp = bid_data["Timestamp"]
        self.userAgent = bid_data["UserAgent"]
        
        # Convert categorical & numeric fields safely
        self.region = int(bid_data["Region"]) if not pd.isna(bid_data["Region"]) else 0
        self.city = int(bid_data["City"]) if not pd.isna(bid_data["City"]) else 0
        self.adExchange = int(bid_data["AdExchange"]) if not pd.isna(bid_data["AdExchange"]) else 0
        self.adSlotWidth = int(bid_data["AdslotWidth"])
        self.adSlotHeight = int(bid_data["AdslotHeight"])
        self.adSlotVisibility = bid_data["AdslotVisibility"]
        self.adSlotFormat = bid_data["AdslotFormat"]
        self.adSlotFloorPrice = float(bid_data["AdslotFloorPrice"]) if not pd.isna(bid_data["AdslotFloorPrice"]) else 0

        # **NEW:** Store actual PayingPrice from impression logs
        self.payingPrice = float(bid_data["PayingPrice"]) if "PayingPrice" in bid_data and not pd.isna(bid_data["PayingPrice"]) else None

    def getFeatures(self):
        """ Extracts features for ML model predictions. """
        return [
            self.adSlotWidth,
            self.adSlotHeight,
            self.region,
            self.city,
            self.adExchange,
            self.adSlotVisibility,
            self.adSlotFormat,
            self.adSlotFloorPrice
        ]

    def getAdSlotFloorPrice(self):
        """ Returns the floor price for the ad slot. """
        return self.adSlotFloorPrice

    def getPayingPrice(self):
        """ Returns the actual PayingPrice if available, otherwise None. """
        return self.payingPrice
