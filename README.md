
# 🕸️ Scrapipy – AI Web Scraper Dashboard

Scrapipy is a powerful AI-powered web scraping dashboard built using **Streamlit**, **Selenium**, and **LangChain**. It allows users to extract, summarize, and analyze web content with a user-friendly interface and LLM integration.

Visit Here-
https://scrapipy.streamlit.app/
---

## 🚀 Features

- 🔍 Input a website URL and extract clean text using Selenium & BeautifulSoup
- 🧠 Analyze and summarize content using LLMs via `langchain_together`
- 📊 Interactive UI with Streamlit
- 🌐 Environment-secure configuration via `.env` or Streamlit Secrets
- 💬 Modular design for easy LLM and model integration

---

## 🛠️ Tech Stack

- `Streamlit` – For building the web UI
- `Selenium` + `BeautifulSoup` – For scraping dynamic and static content
- `LangChain` + `langchain_together` – For LLM integration
- `Python-dotenv` – For environment variables
- `OpenAI` / `Together API` – For running language models

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/akarshmi/Scrapipy.git
cd Scrapipy
```

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the root folder:

```env
OPENAI_API_KEY=your_openai_key_here
TOGETHER_API_KEY=your_together_api_key_here
```

Alternatively, add them securely on **[Streamlit Cloud](https://streamlit.io/cloud)** under **Secrets**.

---

## ▶️ Run the App

```bash
streamlit run main.py
```

---

## 🌐 Deployment

This app can be deployed instantly using [Streamlit Cloud](https://streamlit.io/cloud):

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click “New App”
4. Select your repo and `main.py` as the entry point
5. Add secrets (API keys), then deploy 🎉

---

## 📁 Project Structure

```
Scrapipy/
├── main.py
├── parse.py
├── utils/
│   └── dom_utils.py
├── requirements.txt
└── README.md
```

---

## 🧠 Credits

Created with 💻 by [Akarsh Mishra](http://akarshmi.netlify.app)  
Feel free to fork, star ⭐ and contribute!

---

## 📜 License

This project is licensed under the MIT License.
