
# 💼 Financial Advisory Tool

## 🚀 Introduction

**Financial Advisory Tool** is an innovative, AI-powered platform designed to revolutionize the way individuals and organizations approach financial planning and investment management. By harnessing advanced agentic AI capabilities, this system enables users to create, monitor, and optimize entire investment portfolios tailored to their unique financial situations and long-term visions.

Whether you are a seasoned investor or just starting your financial journey, the Financial Advisory Tool provides a comprehensive, data-driven solution that adapts to your goals, risk appetite, and evolving market conditions. The platform goes beyond traditional advisory services by offering personalized recommendations, actionable insights, and strategic guidance—all in one intuitive interface.

---
## Table of Contents
  - [Key Features](#-key-features)
  - [Environment Variables](#-environment-variables)
  - [Installation](#-installation)
  - [Example](#example)
  - [Notes](#-notes)
  - [Contact](#-contact)


---

## ✨ Key Features <a name="-key-features"></a>

- **🔍 Personalized Portfolio Creation**  
  Instantly generate and adjust investment portfolios based on your financial profile, risk preferences, and desired time horizons.

- **🛡️ Risk-Based Design Plan**  
  Receive portfolio recommendations that align with your risk tolerance, ensuring both growth and security.

- **📊 Complete Allocation Plan**  
  Access detailed asset allocation strategies for a balanced and diversified investment approach.

- **🆘 Contingency Plan Allocation**  
  Prepare for uncertainties with robust contingency planning features.

- **💸 Tax Saving Guide**  
  Discover tailored strategies to optimize your tax liabilities and maximize returns.

- **📝 Implementation Guide**  
  Step-by-step instructions to seamlessly put your financial plan into action.

- **✅ Do’s & Don’ts**  
  Benefit from expert tips that help you avoid common pitfalls and make informed decisions.

- **💡 Investment Suggestions**  
  Get AI-driven suggestions on investment areas, leveraging analysis of the past five years of specific asset performance.

- **📚 Glossary-Driven User Profile**  
  Easily understand your financial status and plan components with a clear, glossary-style user profile.

With intelligent automation, real-time analytics, and a user-centric design, the Financial Advisory Tool empowers you to take control of your financial future with confidence and clarity.

---

## ⚙️ Environment Variables <a name="-environment-variables"></a>

- **For Backend**

  To run this project, add the following environment variables to your `.env` file:

```

WATSONX_API_KEY
WATSONX_PROJECT_ID
WATSONX_URL

```
Optional parameters , as already in defaults mode

```

LLM_ID=watsonx/meta-llama/llama-3-3-70b-instruct                   # add watsonx before model id.  watsonx/meta-llama/llama-model
TOKEN_LIMIT=10000                                                  
TEMPERATURE=0.42                                                   # keep in range of 0.38 to 0.54

```

- **For Frontend**
```
#default for local execution without docker

VITE_BACKEND_URL=http://0.0.0.0:8087/crewai

```
---

## 🛠️ Installation <a name="-installation"></a>

### Prerequisites

- Python 3.11.12 ``` https://www.python.org/downloads/release/python-31112/ ```
- Node.js & npm > v18  ``` https://nodejs.org/en/download ```

### Local Execution

1. **Download the repository**
    ```
    git clone https://github.ibm.com/Shahzad-Malik/Financial-Advisory-Tool.git
    ```

2. **Backend setup**
    ```
    cd backend
    pip install -r requirements.txt
    python app.py
    ```

3. **Frontend setup (in a new terminal)**
    ```
    cd frontend
    npm install
    npm run dev
    ```

4. **Open the provided local endpoint in your browser**

---

### Docker Deployment

1. **Deploy Backend Docker Image**
    - Retrieve the backend URL and /crewai endpoint completion
    - paste the entire url which will look like this
    - (e.g., `www.endpoint.cloud/crewai`)
2. **Frontend Deployment**
    - Use the backend URL as an environment variable during frontend deployment
3. **Access the Application**
    - Visit the deployed frontend URL and start using the tool!

---

## 📦 Example <a name="example"></a>

```
Hi, I’m Jamil from India. I earn around ₹1.5 lakh per month, with expenses of about ₹48,000.
I want to start investing for the next 8 years,
but I’m not sure where to begin and prefer to avoid high risk at the start.
```
---

## 📝 License <a name="-license"></a>

This project is licensed under the [Apache 2.0 License](LICENSE).

---

## 📒 Notes <a name="-notes"></a>

  - this is not a Conversational tool

---

## 📫 Contact <a name="-contact"></a>

For questions or support, please contact [shahzad.malik@ibm.com](mailto:shahzad.malik@ibm.com).

---

**Empower your financial future with AI-driven insights and strategies!**

---
