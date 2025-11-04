# 🎯 Crash Game Stochastic Analyzer

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

A **real-time stochastic analyzer** that models and predicts the frequency of high multipliers (≥ ×10) in the *Crash* game using **Poisson processes** and **random process theory**.

This project combines **probability theory**, **data visualization**, and **real-time statistical computation** to illustrate how stochastic processes can be used to study random events in real-world systems.

---

## 🧠 Overview

The program allows you to manually record, every minute, how many times the game’s multiplier reaches or exceeds **×10**.  
It then performs a **Poisson process analysis** to estimate:

- The **average intensity (λ)** of events per minute  
- The **variance** and **dispersion index**  
- The **autocorrelation** between consecutive minutes  
- A simple **stationarity test**  
- The **probability** of observing at least one ×10 during the next minute  

Each result is explained in **clear French**, so it’s perfect for learning or presenting stochastic concepts.

---

## 🧩 Features

✅ **Manual data entry with real 60-second timer**  
✅ **Real-time stochastic analysis (Poisson-based)**  
✅ **Automatic probability prediction** for next interval  
✅ **Dynamic graph** of counts and moving average  
✅ **French-language interpretation** of results  
✅ **Automatic CSV saving** of all analyses  
✅ **Historical visualization** (λ and autocorrelation trends)

---

## 📸 Screenshots (coming soon)

_Add screenshots of your UI and graphs here!_

---

## 🖥️ Technologies Used

| Component | Purpose |
|------------|----------|
| **Python 3** | Core language |
| **Tkinter** | GUI (real-time timer and input) |
| **NumPy** | Statistical computation |
| **SciPy** | Poisson distribution modeling |
| **Pandas** | Data management and CSV export |
| **Matplotlib** | Real-time graph visualization |
| **Statsmodels** | Autocorrelation and process analysis |

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/crash-analyzer.git
cd crash-analyzer
2. Install dependencies
pip install -r requirements.txt

3. Run the application
python crash_analyzer.py

📂 Project Structure
crash-analyzer/
│
├── crash_analyzer.py           # Main Python script (GUI + analysis)
├── README.md                   # Project documentation
├── requirements.txt             # Python dependencies
└── data/
    └── historique_crash_manual.csv  # Saved historical results

📊 Example Output

After several minutes of observation, you’ll get results such as:

Minutes enregistrées : 12
Intensité moyenne (λ) : 0.83
Variance : 1.14
Autocorrélation (lag=1) : 0.21
Stationnarité : Oui (stable)
Probabilité d'au moins un ×10 : 56.9%

INTERPRÉTATION :
- Processus stationnaire : comportement stable dans le temps.
- Légère dépendance temporelle observée.
- Quelques ×10 par minute attendus (flux modéré).

📚 Mathematical Concept

This project is based on the Poisson stochastic process, which models the number of events occurring in a fixed time interval under the following assumptions:

Events occur independently.

The average rate (λ) is constant.

Two events cannot happen at the exact same instant.

The program also performs a stationarity test, autocorrelation computation, and gives a human-readable interpretation of the process dynamics.

🧾 License

This project is licensed under the MIT License.
See the LICENSE
 file for details.

🧑‍💻 Author

[Your Name]
📍 Béjaïa, Algeria
💡 Student in Computer Science — ESI Béjaïa
🔗 GitHub: https://github.com/yourusername

🌟 Contributing

Pull requests are welcome!
If you have suggestions or improvements (UI, data automation, statistical features), feel free to fork the repository and open a PR.

🧮 Future Improvements

🔁 Add automatic data collection via web scraping (if allowed)

🎵 Add sound alerts when the minute ends

🌐 Add multilingual interface (English/French)

🧠 Add advanced models (Markov or exponential processes)

“Model randomness to understand order.” — Project Motto


---

### 💡 Next steps for you:
1. Create your repo on GitHub (name: `crash-analyzer`).
2. Add your three files:
   - `crash_analyzer.py`
   - `requirements.txt`
   - `README.md`
3. Commit & push:
   ```bash
   git add .
   git commit -m "Initial commit: Crash Game Stochastic Analyzer"
   git push origin main
