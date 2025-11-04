import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import csv, os, pandas as pd
from statsmodels.tsa.stattools import acf
from scipy.stats import poisson

# --- Configuration ---
DUREE_MINUTE = 60  # durée réelle en secondes
FICHIER_HIST = "historique_crash_manual.csv"

# --- Données et état ---
donnees = []  # liste des entiers : nombre de cotes >=10 par minute
count_minute = 0
timer_running = False
seconds_left = DUREE_MINUTE

# --- Fonctions utilitaires ---
def moyenne_mobile(x, w=5):
    if len(x) < w:
        return np.array(x, dtype=float)
    return np.convolve(x, np.ones(w)/w, mode='same')

def test_stationnarite(x):
    # score simple : écart-type des moyennes par blocs / moyenne globale
    x = np.array(x)
    if len(x) < 10:
        return None  # pas assez d'info
    blocs = [np.mean(x[i:i+10]) for i in range(0, len(x)-9, 10)]
    mean_blocs = np.mean(blocs)
    if mean_blocs == 0:
        return None
    return float(np.std(blocs) / mean_blocs)

def sauvegarder_analyse(lambda_est, var, autocorr, stationnaire):
    existe = os.path.exists(FICHIER_HIST)
    with open(FICHIER_HIST, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if not existe:
            w.writerow(["Date","Heure","Nb_minutes","Lambda","Variance","Autocorr(1)","Stationnarité","Série"])
        w.writerow([
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().strftime("%H:%M:%S"),
            len(donnees),
            round(lambda_est,3),
            round(var,3),
            round(autocorr,3) if autocorr is not None else "",
            "oui" if stationnarite_score_is_ok(stationnaire) else "non" if stationnarire_defined(stationnaire) else "",
            str(list(donnees))
        ])

def stationnarire_defined(score):
    return score is not None

def stationnarite_score_is_ok(score):
    return (score is not None) and (score < 0.2)

# --- Analyse principale et affichage ---
def analyser():
    if len(donnees) == 0:
        lbl_explanation.set("Aucune donnée encore enregistrée.")
        return

    x = np.array(donnees, dtype=float)
    n = len(x)
    lambda_est = float(np.mean(x))
    var = float(np.var(x, ddof=1)) if n > 1 else 0.0
    dispersion = (var / lambda_est) if lambda_est != 0 else float('inf')
    station_score = test_stationnarite(x)  # None si pas assez
    stationnaire = "Oui (stable)" if stationnarite_score_is_ok(station_score) else ("Non (instable)" if stationnarire_defined(station_score) and not stationnarite_score_is_ok(station_score) else "Données insuffisantes pour tester")
    # autocorr lag 1
    try:
        acf_vals = acf(x, nlags=min(10, max(1, n-1)), fft=False)
        autocorr = float(acf_vals[1]) if len(acf_vals) > 1 else 0.0
    except Exception:
        autocorr = None

    # prédiction à la minute suivante (Poisson homogene)
    pred_next_mean = lambda_est
    prob_at_least_1 = 1.0 - poisson.pmf(0, lambda_est) if lambda_est >= 0 else 0.0

    # Mise à jour du widget résultat
    texte = []
    texte.append(f"Minutes enregistrées : {n}")
    texte.append(f"Intensité moyenne (λ) estimée : {lambda_est:.3f} (nombre moyen de ×10 par minute)")
    texte.append(f"Variance empirique : {var:.3f}")
    texte.append(f"Indice de dispersion (var/λ) : {'∞' if dispersion==float('inf') else f'{dispersion:.2f}'}")
    texte.append(f"Autocorrélation (lag=1) : {('%.3f' % autocorr) if autocorr is not None else 'indéterminée'}")
    texte.append(f"Stationnarité (test simple) : {stationnaire}")
    texte.append("")
    texte.append("PRÉDICTION (modèle Poisson simple) :")
    texte.append(f"  → Nombre moyen attendu la minute suivante : {pred_next_mean:.2f}")
    texte.append(f"  → Probabilité d'avoir au moins 1 ×10 : {prob_at_least_1*100:.1f}%")
    texte.append("")
    # traduction / explication en français simple
    texte.append("INTERPRÉTATION (FR) :")
    if n < 5:
        texte.append("  - Trop peu de données pour une interprétation fiable (moins de 5 minutes).")
    else:
        if stationnarite_score_is_ok(station_score):
            texte.append("  - Le phénomène semble STATIONNAIRE : la moyenne ne varie pas fort dans le temps.")
        elif stationnarire_defined(station_score):
            texte.append("  - Le phénomène semble NON STATIONNAIRE : la moyenne varie selon les blocs de 10 minutes.")
        else:
            texte.append("  - Pas assez d'infos pour décider de la stationnarité.")

        if autocorr is not None:
            if abs(autocorr) > 0.4:
                texte.append("  - Forte dépendance temporelle entre minutes consécutives (les épisodes se suivent).")
            elif abs(autocorr) > 0.1:
                texte.append("  - Légère dépendance temporelle.")
            else:
                texte.append("  - Faible dépendance : les minutes sont assez indépendantes.")
        else:
            texte.append("  - Autocorrélation impossible à estimer sur si peu de données.")

        if pred_next_mean > 1.5:
            texte.append("  - Attendu : plusieurs ×10 par minute en moyenne (flux élevé).")
        elif pred_next_mean > 0.5:
            texte.append("  - Attendu : quelques ×10 par minute (flux modéré).")
        else:
            texte.append("  - Attendu : rare, généralement 0 ou 1 ×10 par minute (flux faible).")

    lbl_explanation.set("\n".join(texte))

    # Graphique de la série et moyenne mobile
    plt.clf()
    plt.plot(range(1, n+1), x, marker='o', label='Comptage ×10 par minute')
    mm = moyenne_mobile(x, w=5)
    if len(mm) > 0:
        plt.plot(range(1, n+1), mm, linestyle='-', label='Moyenne mobile (w=5)')
    plt.axhline(lambda_est, color='r', linestyle='--', label=f'λ={lambda_est:.2f}')
    plt.xlabel("Minute")
    plt.ylabel("Nombre de ×10")
    plt.title("Évolution du comptage de cotes ≥10")
    plt.legend()
    plt.grid(True)
    plt.pause(0.01)

    # Sauvegarde périodique (toutes les 10 entrées)
    if n % 10 == 0:
        save_needed = True
    else:
        save_needed = False
    if save_needed:
        try:
            sauvegarder_analyse(lambda_est, var, autocorr if autocorr is not None else 0.0, station_score)
        except Exception as e:
            print("Erreur sauvegarde :", e)

# --- Timer (compte à rebours) ---
def tick():
    global seconds_left, timer_running
    if not timer_running:
        return
    if seconds_left > 0:
        seconds_left -= 1
        lbl_timer.set(f"Temps restant : {seconds_left} s")
        root.after(1000, tick)
    else:
        # minute terminée : activer saisie
        lbl_timer.set("⏰ Minute terminée — entre le nombre et clique 'Valider'")
        entry_valeur.config(state='normal')
        btn_valider.config(state='normal')
        # stopper le timer (attente validation)
        timer_stop_for_entry()

def demarrer_minuteur():
    global timer_running, seconds_left
    if timer_running:
        messagebox.showinfo("Minuteur", "Le minuteur est déjà en cours.")
        return
    # (re)initialiser
    seconds_left = DUREE_MINUTE
    timer_running = True
    lbl_timer.set(f"Temps restant : {seconds_left} s")
    root.after(1000, tick)

def timer_stop_for_entry():
    global timer_running
    timer_running = False
    # notifier l'utilisateur
    status.set("En attente de saisie pour cette minute...")

def valider_entre():
    global seconds_left
    s = entry_valeur.get().strip()
    if s == "":
        messagebox.showerror("Erreur", "Entre un nombre entier (0,1,2...).")
        return
    try:
        val = int(s)
        if val < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erreur", "Valeur invalide. Entre un entier >= 0.")
        return
    donnees.append(val)
    entry_valeur.delete(0, tk.END)
    entry_valeur.config(state='disabled')
    btn_valider.config(state='disabled')
    compteur_var.set(f"Minutes saisies : {len(donnees)}")
    status.set("Donnée enregistrée — analyse en cours...")
    analyser()
    # redémarrer le minuteur automatiquement pour la minute suivante
    seconds_left = DUREE_MINUTE
    timer_running = True
    status.set("Minuteur redémarré pour la minute suivante.")
    root.after(1000, tick)

def annuler_minuteur():
    global timer_running, seconds_left
    if not timer_running:
        seconds_left = DUREE_MINUTE
        lbl_timer.set("Minuteur réinitialisé.")
    else:
        timer_running = False
        seconds_left = DUREE_MINUTE
        lbl_timer.set("Minuteur arrêté et réinitialisé.")
    entry_valeur.config(state='disabled')
    btn_valider.config(state='disabled')
    status.set("Minuteur annulé ou réinitialisé.")

def voir_historique():
    if not os.path.exists(FICHIER_HIST):
        messagebox.showinfo("Historique", "Aucun historique trouvé.")
        return
    try:
        df = pd.read_csv(FICHIER_HIST)
        if df.empty:
            messagebox.showinfo("Historique", "Fichier historique vide.")
            return
        plt.figure(figsize=(9,5))
        if "Lambda" in df.columns:
            plt.plot(df["Lambda"], marker='o', label='Lambda estimé')
        if "Autocorr(1)" in df.columns:
            try:
                plt.plot(df["Autocorr(1)"], marker='s', label='Autocorr(1)')
            except Exception:
                pass
        plt.title("Historique des analyses")
        plt.xlabel("Analyse #")
        plt.legend()
        plt.grid(True)
        plt.show()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir l'historique : {e}")

# --- Interface TKinter ---
root = tk.Tk()
root.title("Analyseur manuel Crash — minuteur réel + explication")
root.geometry("780x700")

# Top controls
frame_top = tk.Frame(root)
frame_top.pack(pady=8)

btn_start = tk.Button(frame_top, text="▶ Démarrer minuteur (60s)", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", command=demarrer_minuteur)
btn_start.grid(row=0, column=0, padx=6)

btn_cancel = tk.Button(frame_top, text="✖ Annuler / Réinit", font=("Arial", 11), bg="#E53935", fg="white", command=annuler_minuteur)
btn_cancel.grid(row=0, column=1, padx=6)

btn_hist = tk.Button(frame_top, text="📜 Voir historique", font=("Arial", 11), bg="#2196F3", fg="white", command=voir_historique)
btn_hist.grid(row=0, column=2, padx=6)

lbl_timer = tk.StringVar(value=f"Temps restant : {DUREE_MINUTE} s")
lbl_timer_widget = tk.Label(root, textvariable=lbl_timer, font=("Arial", 14), bg="#fff3e0", width=40)
lbl_timer_widget.pack(pady=8)

# Entry zone (disabled until minute over)
frame_entry = tk.Frame(root)
frame_entry.pack(pady=6)

tk.Label(frame_entry, text="Nombre de cotes ≥10 observées dans la minute :", font=("Arial", 11)).grid(row=0, column=0, padx=6)
entry_valeur = tk.Entry(frame_entry, font=("Arial", 14), width=8, state='disabled')
entry_valeur.grid(row=0, column=1, padx=6)

btn_valider = tk.Button(frame_entry, text="Valider", font=("Arial", 11, "bold"), bg="#009688", fg="white", state='disabled', command=valider_entre)
btn_valider.grid(row=0, column=2, padx=6)

# Counter and status
compteur_var = tk.StringVar(value="Minutes saisies : 0")
lbl_compteur = tk.Label(root, textvariable=compteur_var, font=("Arial", 12))
lbl_compteur.pack(pady=6)

status = tk.StringVar(value="Statut : en attente (cliquez Démarrer).")
lbl_status = tk.Label(root, textvariable=status, font=("Arial", 11, "italic"))
lbl_status.pack(pady=4)

# Explanation box
lbl_explanation = tk.StringVar(value="Explication : aucune analyse pour le moment.")
txt_explanation = tk.Label(root, textvariable=lbl_explanation, justify="left", font=("Consolas", 10), bg="#f0f4c3", width=92, height=14, anchor="nw")
txt_explanation.pack(padx=10, pady=10)

# Matplotlib area: we will use interactive window
plt.ion()
plt.figure(figsize=(9,4))
plt.show(block=False)

# Start the Tk loop
root.mainloop()
