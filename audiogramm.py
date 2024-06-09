import matplotlib.pyplot as plt
import numpy as np


def create_audiogram(freqs, right_values, left_values):
    """Erstellt ein Audiogramm basierend auf den gegebenen Frequenzen und Hörschwellenwerten.

    Args:
        freqs (list of int): Eine Liste von Frequenzen in Hertz.
        right_values (list of int): Eine Liste von Hörschwellen in dB HL vom rechten Ohr.
        left_values (list of int): Eine Liste von Hörschwellen in dB HL vom linken Ohr
            
    """
    plt.figure(figsize=(10, 6))
    
    # Bereichsfarben hinzufügen
    plt.axhspan(-10, 20, facecolor='lightgreen', alpha=0.3)
    plt.axhspan(20, 40, facecolor='lightskyblue', alpha=0.3)
    plt.axhspan(40, 70, facecolor='yellow', alpha=0.3)
    plt.axhspan(70, 90, facecolor='orange', alpha=0.3)
    plt.axhspan(90, 120, facecolor='red', alpha=0.3)

    # Text für die Hörgrade direkt neben die y-Achse setzen
    plt.text(52, 15, 'Normalhörigkeit', ha='left', va='center', fontsize=8, color='black')
    plt.text(52, 35, 'Leichte Schwerhörigkeit', ha='left', va='center', fontsize=8)
    plt.text(52, 65, 'Mittlere Schwerhörigkeit', ha='left', va='center', fontsize=8)
    plt.text(52, 85, 'Schwere Schwerhörigkeit', ha='left', va='center', fontsize=8)
    plt.text(52, 115, 'Hochgradige Schwerhörigkeit', ha='left', va='center', fontsize=8)

    # Plot der Hörschwellen
    plt.plot(freqs, right_values, marker='o', linestyle='-', color='b', label='rechtes Ohr')
    plt.plot(freqs, left_values, marker='x', linestyle='-', color='r', label='linkes Ohr')
    plt.gca().invert_yaxis()  # Invertiert die y-Achse, da tiefere dB-Werte besseres Hören anzeigen
    plt.title('Audiogramm')
    plt.xlabel('Frequenzen (Hz)')
    plt.ylabel('Hörschwelle (dB HL)')
    plt.ylim(120,-10)
    plt.xscale('log')  # Logarithmische Skala für die Frequenzen
    plt.xticks([63, 125, 250, 500, 1000, 2000, 4000, 8000], ['63', '125', '250', '500', '1000', '2000', '4000', '8000'])
    plt.yticks(np.arange(0, 121, 10))
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Raster für bessere Lesbarkeit
    plt.legend(loc='upper right')
   
    plt.show()

# Beispielwerte
freq = [63, 125, 250, 500, 1000, 2000, 4000, 8000]
dummy_right = [10, 15, 20, 25, 30, 35, 40, 45]
dummy_left = [5, 10, 15, 20, 25, 30, 35, 40]
# Audiogramm erstellen
create_audiogram(freq, dummy_right, dummy_left)

