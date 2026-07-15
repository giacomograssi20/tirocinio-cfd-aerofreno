import os
import matplotlib.pyplot as plt
import numpy as np

def calcola_scostamento(valore_attuale, valore_precedente):
    if valore_precedente == 0:
        return 0.0
    return ((valore_attuale - valore_precedente) / valore_precedente) * 100

def estrai_ultimo_cd(filepath):
    """Legge il file unendo le righe spezzate su due linee."""
    if not os.path.exists(filepath):
        return [], []
    
    iterazioni, cd_valori = [], []
    raw_lines = []
    
    with open(filepath, 'r') as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith('#') or linea.startswith('Time'):
                continue
            raw_lines.append(linea)
    
    i = 0
    while i < len(raw_lines):
        parti = raw_lines[i].split()
        if parti and parti[0].isdigit():
            # Se la riga dopo inizia con un segno meno o un valore numerico continuo, uniscile
            if i + 1 < len(raw_lines) and (raw_lines[i+1].startswith('-') or raw_lines[i+1].startswith('.')):
                linea_completa = raw_lines[i] + " " + raw_lines[i+1]
                righe_unite = linea_completa.split()
                i += 2
            else:
                righe_unite = parti
                i += 1
            
            try:
                iterazioni.append(int(righe_unite[0]))
                cd_valori.append(float(righe_unite[1])) # Il Cd è il primo valore dopo l'iterazione
            except (ValueError, IndexError):
                continue
        else:
            i += 1
            
    return iterazioni, cd_valori

# --- PERCORSO FILE ---
percorso_file = "postProcessing/forceCoeffs/0/coefficient.dat"
if not os.path.exists(percorso_file) and os.path.exists("postProcessing/forceCoeffs/0/coefficient.txt"):
    percorso_file = "postProcessing/forceCoeffs/0/coefficient.txt"

print("--- AVVIO AUTOMATIZZAZIONE POST-PROCESSING ---")
iterazioni, cd_valori = estrai_ultimo_cd(percorso_file)

if len(cd_valori) >= 200:
    # Calcolo della media degli ultimi 200 passi come voleva il professore
    ultimi_cd = cd_valori[-200:]
    media_cd = np.mean(ultimi_cd)
    scostamento = calcola_scostamento(cd_valori[-1], cd_valori[-2])
    
    print("\n==========================================")
    print(f"Iterazione Corrente: {iterazioni[-1]}")
    print(f"Cd Istantaneo:       {cd_valori[-1]:.5f}")
    print(f"Media Cd (ultimi 200): {media_cd:.5f}")
    print(f"Scostamento:         {scostamento:.4f}%")
    print("==========================================\n")
    
    # Grafico logaritmico completo
    plt.figure(figsize=(10, 6))
    plt.semilogy(iterazioni, cd_valori, label='Cd Istantaneo', color='blue')
    plt.axhline(y=media_cd, color='red', linestyle='--', label=f'Media ultimi 200 ({media_cd:.4f})')
    plt.xlabel('Iterazioni')
    plt.ylabel('Coefficiente di Drag (Cd) - Scala Log')
    plt.title('Andamento di Convergenza del Cx / Cd')
    plt.grid(True, which="both", ls="-")
    plt.legend()
    plt.savefig('andamento_cd_convergito.png')
    print("Grafico salvato con successo!")
else:
    print(f"Dati insufficienti per la media dei 200 passi. Trovati solo {len(cd_valori)} valori.")