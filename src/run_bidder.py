import pandas as pd
from BidRequest import BidRequest
from Bid import Bid

# Load bid requests
days = ["11", "12"]
df_bid_list = []
for day in days:
    df_bid = pd.read_csv(f"/Users/adityarajtandon/Documents/RTB_MODEL/dataset/bid.{day}.txt", sep="\t", header=None, low_memory=False)
    df_bid.columns = ["BidID", "Timestamp", "VisitorID", "UserAgent", "IP",
                      "Region", "City", "AdExchange", "Domain", "URL", "AnonURLID",
                      "AdslotID", "AdslotWidth", "AdslotHeight", "AdslotVisibility",
                      "AdslotFormat", "AdslotFloorPrice", "CreativeID", "BiddingPrice", "AdvertiserID", "UserTags"]
    df_bid.drop(columns=["UserTags"], inplace=True)
    df_bid_list.append(df_bid)
df_bid = pd.concat(df_bid_list, ignore_index=True)

# Load impression logs (to get PayingPrice)
df_val_list = []
for day in days:
    temp_val = pd.read_csv(f"/Users/adityarajtandon/Documents/RTB_MODEL/dataset/imp.{day}.txt", sep="\t", header=None, low_memory=False)
    temp_val.columns = ["BidID", "Timestamp", "Logtype", "VisitorID", "UserAgent", "IP",
                        "Region", "City", "AdExchange", "Domain", "URL", "AnonURLID",
                        "AdslotID", "AdslotWidth", "AdslotHeight", "AdslotVisibility",
                        "AdslotFormat", "AdslotFloorPrice", "CreativeID", "BiddingPrice",
                        "PayingPrice", "KeypageURL", "AdvertiserID", "ExtraColumn"]
    df_val_list.append(temp_val)
df_val = pd.concat(df_val_list, ignore_index=True)

# Load clicks & conversions
df_clk_list = []
df_conv_list = []
for day in days:
    temp_clk = pd.read_csv(f"/Users/adityarajtandon/Documents/RTB_MODEL/dataset/clk.{day}.txt", sep="\t", header=None)[[0]]
    temp_clk.columns = ["BidID"]
    temp_clk["Clicked"] = 1
    df_clk_list.append(temp_clk)

    temp_conv = pd.read_csv(f"/Users/adityarajtandon/Documents/RTB_MODEL/dataset/conv.{day}.txt", sep="\t", header=None)[[0]]
    temp_conv.columns = ["BidID"]
    temp_conv["Converted"] = 1
    df_conv_list.append(temp_conv)

df_clk = pd.concat(df_clk_list, ignore_index=True)
df_conv = pd.concat(df_conv_list, ignore_index=True)

# Merge Clicks & Conversions with Impressions
df_val = df_val.merge(df_clk, on="BidID", how="left").fillna(0)
df_val = df_val.merge(df_conv, on="BidID", how="left").fillna(0)

# Merge bids and impressions
df_merged = df_bid.merge(df_val[["BidID", "PayingPrice", "Clicked", "Converted", "AdvertiserID"]], on="BidID", how="left")

print(f"Total Clicks in Validation Set: {df_merged['Clicked'].sum()}")
print(f"Total Conversions in Validation Set: {df_merged['Converted'].sum()}")

#print values with clicks = 1
df_merged_clicks = df_merged[df_merged['Clicked'] == 1]
print(df_merged_clicks)

# # Initialize Bid model
# bid = Bid(total_budget=10000, campaign_duration=50)  # Example budget

# # Simulate bidding
# results = []
# for _, row in df_merged.iterrows():
#     bid_request = BidRequest(row)
#     bid_price = bid.getBidPrice(bid_request)

#     if bid_price == -99:  # Stop bidding if budget is exhausted
#         break

#     if bid_price != -1:  # Append only valid bids
#         results.append({
#             "BidID": row["BidID"],
#             "BidPrice": bid_price
#         })

# # Convert results to DataFrame
# df_results = pd.DataFrame(results)

# # Ensure merging Clicked & Converted correctly for score calculation
# df_results = df_results.merge(df_val[["BidID", "Clicked", "Converted", "AdvertiserID"]], on="BidID", how="left").fillna(0)

# # Compute Hackathon Score
# # Advertiser-to-N mapping
# advertiser_n_mapping = {
#     1458: 0,  # Local e-commerce
#     3358: 2,  # Software
#     3386: 0,  # Global e-commerce
#     3427: 0,  # Oil
#     3476: 10  # Tire
# }

# # Add the N column based on AdvertiserID
# df_results["N"] = df_results["AdvertiserID"].map(advertiser_n_mapping)

# # Compute the Hackathon Score dynamically
# df_results["WeightedConversions"] = df_results["Converted"] * df_results["N"]
# score = df_results["Clicked"].sum() + df_results["WeightedConversions"].sum()

# print(f"Final Hackathon Score: {score}")
# print(f"Total Remaining Budget: {bid.remaining_budget}")
