# 🧩 GutPattern: Bi-Modal Dietary Trigger Identification

**GutPattern** is an AI-powered journaling and analysis tool designed to uncover hidden dietary sensitivities. Unlike standard food diaries that only look at immediate reactions, GutPattern uses a bi-modal mathematical algorithm to detect both instant and delayed triggers.

---

## 🧬 The Science: Bi-Modal Time Decay

The core of this project is a pattern-recognition algorithm that evaluates meals against two distinct physiological response windows. The total weight $W$ for any given time $\Delta t$ is calculated as:

$$W(\Delta t) = \alpha e^{-\lambda \Delta t} + \beta e^{-\frac{(\Delta t - \mu)^2}{2\sigma^2}}$$

### 📊 Response Windows
| Pattern Type | Window | Logic | Targets |
| :--- | :--- | :--- | :--- |
| **Immediate** | 0–6 Hours | Exponential Decay | Acute sensitivities (e.g., Capsaicin) |
| **Delayed** | 30–42 Hours | Gaussian (Bell) Curve | Systemic/Digestive delays (e.g., Omega-6) |

---

## 🚀 Key Features

* **Natural Language Logging:** Describe your meal in plain English (e.g., *"Spicy burger with fries"*).
* **AI Ingredient Parsing:** Uses **Gemini-2.0-Flash** (via Poe API) to break down meals into chemical components.
* **Automated Correlation:** Mathematically links flare-up severity (1–10) to specific ingredients consumed in the days prior.
* **Risk Forecasting:** Predicts the safety of future meals based on your unique historical patterns.

---

## 🛠️ Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/pokercstem-ui/geminiaiediarydemo.git](https://github.com/pokercstem-ui/geminiaiediarydemo.git)
cd geminiaiediarydemo```

### 2. Install Dependencies
Ensure you have Python 3.9+ installed. It is recommended to use a virtual environment. Run the following command to install the required libraries:
```bash
pip install -r requirements.txt  ```

### 3. Configure API Key
The app requires access to the Poe API to parse meal descriptions. Open app.py in your code editor and locate the api_key variable within the get_components_from_ai function. Replace the placeholder string with your actual Poe API Key:
```python
api_key = "your-poe-api-key-here"```

### 4. Launch the Application
Start the Streamlit server to view the app in your browser:
```bash
streamlit run app.py```

