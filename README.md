# 🎯 Crash Game Stochastic Analyzer

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

A **real-time stochastic analyzer** that models and predicts the frequency of high multipliers (\u2265 \u00d710) in the *Crash* game using **Poisson processes** and **stochastic process theory**.

This project brings together **probability theory**, **data visualization**, and **real-time analysis** to demonstrate how stochastic models can describe random event behavior in dynamic systems.

---

## 🧠 Overview

The application allows the user to manually record, every minute, how many times the game multiplier reaches or exceeds \u00d710. It then performs a **Poisson-based stochastic analysis** to estimate:

* **Average event intensity (\u03bb)** per minute
* **Variance** and **dispersion index (var/\u03bb)**
* **Autocorrelation** between consecutive minutes
* A **stationarity test** to detect stability over time
* **Probability prediction** of at least one \u00d710 in the next minute

Each analysis is automatically interpreted in **plain French**, making this project ideal for learning and teaching stochastic process theory.

---

## 🧩 Features

| Feature                 | Description                                                                  |
| ----------------------- | ---------------------------------------------------------------------------- |
| ⏱️ Real-time timer      | Automatic 60-second countdown for each observation period                    |
| 🧮 Poisson analysis     | Real-time computation of \u03bb, variance, and dispersion index              |
| 📈 Dynamic graph        | Displays event counts, moving averages, and \u03bb line                      |
| 🗣️ French explanations | Natural-language summaries of statistical results                            |
| 🗃️ CSV export          | Automatically saves data and analyses to `/data/historique_crash_manual.csv` |
| 🧠 Historical analysis  | Visualize \u03bb and autocorrelation trends over multiple sessions           |

---

## 🧰 Technologies

| Library         | Purpose                                 |
| --------------- | --------------------------------------- |
| **Tkinter**     | Interactive GUI and real-time timer     |
| **NumPy**       | Statistical and mathematical operations |
| **SciPy**       | Poisson distribution modeling           |
| **Statsmodels** | Autocorrelation and stochastic testing  |
| **Pandas**      | Data handling and CSV management        |
| **Matplotlib**  | Visualization and live chart updates    |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/crash-analyzer.git
cd crash-analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the analyzer

```bash
python crash_analyzer.py
```

---

## 📂 Project Structure

```
crash-analyzer/
│
├── crash_analyzer.py              # Main application (GUI + analysis)
├── requirements.txt               # Dependencies
├── README.md                      # Documentation
└── data/
    └── historique_crash_manual.csv  # Automatically generated historical file
```

---

## 📊 Example Output

```
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
```

---

## 📚 Theoretical Background

This project relies on **Poisson stochastic processes**, used to model the number of random events within fixed intervals under the following assumptions:

1. Events occur independently.
2. The average rate (\u03bb) remains constant.
3. Two events cannot happen simultaneously.

Additionally, the tool computes:

* **Autocorrelation (lag=1):** measures dependence between successive minutes.
* **Stationarity ratio:** evaluates if the mean and variance remain stable across time.

Together, these metrics provide insight into whether the game’s behavior follows a stationary Poisson process or shows temporal dependencies.

---

## 🧾 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for details.

---

## 🧑‍💻 Author

**[Hellal Danis]**
📍 Béjaïa, Algeria
🎓 Student in Computer Science — ESTIN Béjaïa
🔗 GitHub: [https://github.com/Hellaldanis](https://github.com/Hellaldanis)

---

## 🌱 Future Improvements

* 🔁 **Automated data collection** (via APIs or web scraping if permitted)
* 🔔 **Sound alerts** when the minute interval ends
* 🌐 **Multi-language support** (English/French)
* 🧮 **Advanced models**: Markov chains, exponential processes

---

> “Model randomness to understand order.” — *Crash Analyzer Project*

