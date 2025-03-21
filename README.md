# **Real-Time Bidding (RTB) Model - Project Overview**  

## **Introduction**  
This project implements an offline-simulated Real-Time Bidding (RTB) system using Q-learning and Deep Learning models to optimize bidding strategies in programmatic advertising.

The goal is to maximize advertiser performance (clicks + weighted conversions) under a fixed budget constraint, using historical bidding logs provided in the iPinYou dataset. The system simulates ad auctions using past bid, impression, click, and conversion logs to evaluate how effectively the model selects optimal bid prices.

While this project currently runs in a simulation environment, it lays the groundwork for deployment in a real-time ad exchange setting by replicating a realistic auction flow, including second-price auctions and budget pacing.

---

## **How RTB Works**  
- **Bidding Process**: Advertisers participate in an auction where they bid to display ads to users.  
- **Winning a Bid**: The highest bidder wins, but they pay the second-highest price (**Second Price Auction**).  
- **Conversion Tracking**: Once an ad is displayed, user engagement (clicks) and conversions (successful actions) are tracked.  

---

## **Project Workflow**  
### **1️⃣ Data Processing & Model Training**
- **Dataset** includes:
  - **Bid logs**: All bids submitted by advertisers.  
  - **Impression logs**: Bids that won and resulted in an ad impression.  
  - **Click logs**: Impressions where users clicked the ad.  
  - **Conversion logs**: Clicks that led to a successful conversion.  
- Three models are trained using **deep learning**:
  - **CTR Model**: Predicts the probability of a user clicking the ad.  
  - **CVR Model**: Predicts the probability of a user converting after clicking.  
  - **Market Model**: Predicts the market price of an impression.  

### **2️⃣ Bid Optimization with Q-learning**
- **State**: `(Remaining budget, Expected value, Market price)`.  
- **Actions**: Bid prices `[pMarket * 0.8, pMarket, pMarket * 1.2, pMarket * 1.5]`.  
- **Reward Function**:  
  - `reward = (CTR * (1 + 10 * CVR)) - Bid Price`  
  - The reward encourages bidding higher for impressions likely to convert while avoiding overspending.  
- The model updates the **Q-table** dynamically, adjusting bids to maximize performance.

### **3️⃣ Simulation & Evaluation**
- The model is tested using **historical auction data** to determine **how accurately it predicts winning bids**.  
- If the predicted bid is **higher than the market price**, it wins the bid.  
- The **Hackathon Score** is calculated based on **clicks and conversions** using a weighted advertiser-based scoring system:
  - `Score = Total Clicks + (N * Total Conversions)`  
  - **N** is advertiser-specific (e.g., Local e-commerce has N=0, Software has N=2).  

---

## **Key Features**
✅ **Deep Learning-based CTR, CVR, and Market Price Models**  
✅ **Q-learning-based bidding optimization**  
✅ **Real-time budget handling to prevent overspending**  
✅ **Second-price auction mechanism implementation**  
✅ **Evaluates bid performance using actual impression logs**  

---

## **Project Structure**
📂 **`src/`** - Codebase  
- **`Bid.py`** → Implements bidding strategy with Q-learning.  
- **`BidRequest.py`** → Parses incoming bid requests.  
- **`Bidder.py`** → Abstract class defining a generic bidder.  
- **`run_bidder.py`** → Runs the simulation using real bid data.  
- **`train_models.ipynb`** → Notebook for training CTR, CVR, and Market models.  

📂 **`dataset/`** *(Ignored in GitHub)* - Contains bid, impression, click, and conversion logs.  

📄 **`.gitignore`** - Excludes large datasets from GitHub.  

📄 **`requirements.txt`** - List of dependencies.  

---

## **Installation & Setup**
### **🔹 1. Clone the Repository**
```bash
git clone https://github.com/adityarajtandon/RTB_Model.git
cd RTB_Model
```

### **🔹 2. Create a Virtual Environment**
```bash
python -m venv rtb_env
source rtb_env/bin/activate  # On macOS/Linux
rtb_env\Scripts\activate     # On Windows
```

### **🔹 3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **🔹 4. Train the Models**
Run the training script to generate the CTR, CVR, and Market models:
```bash
python train_models.py
```

### **🔹 5. Simulate Bidding**
Run the **bidder simulation** to test model performance:
```bash
python run_bidder.py
```

---

## **Dependencies**
All required dependencies are listed in `requirements.txt`.  
You can install them using:
```bash
pip install -r requirements.txt
```

### **Main Libraries Used**
| Library          | Purpose |
|-----------------|---------|
| `numpy`        | Numerical computations |
| `pandas`       | Data processing |
| `tensorflow`   | Deep learning (CTR, CVR, Market models) |
| `scikit-learn` | Data preprocessing |
| `matplotlib`   | Visualization |
| `random`       | Q-learning exploration-exploitation |

---

## **Expected Outcomes**
📌 **Improved Bid Efficiency**: Optimized bidding strategy ensures high-impact ads win at minimal cost.  
📌 **Higher Click & Conversion Rates**: CTR & CVR predictions help bid more effectively.  
📌 **Budget Optimization**: Prevents overspending by dynamically adjusting bids.  

---

## **Future Enhancements**
🔹 **Deep Q-Network (DQN)**: Replace the Q-table with a neural network for better bid optimization.  
🔹 **Multi-Agent Bidding**: Simulate competition between multiple advertisers.  
🔹 **Ad Contextual Targeting**: Improve bid strategy using user behavior patterns.  

🚀**This project is a foundation for AI-driven ad bidding strategies that can be expanded into real-world programmatic advertising.**
