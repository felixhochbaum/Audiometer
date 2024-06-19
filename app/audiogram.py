import matplotlib.pyplot as plt
import numpy as np


def create_audiogram(freqs, right_values, left_values, save=True):
    """Erstellt ein Audiogramm basierend auf den gegebenen Frequenzen und Hörschwellenwerten.

    Args:
        freqs (list of int): Eine Liste von Frequenzen in Hertz.
        right_values (list of int): Eine Liste von Hörschwellen in dB HL vom rechten Ohr.
        left_values (list of int): Eine Liste von Hörschwellen in dB HL vom linken Ohr
            
    """

    #TODO save figure
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # Bereichsfarben hinzufügen
    ax.axhspan(-10, 20, facecolor='lightgreen', alpha=0.3)
    ax.axhspan(20, 40, facecolor='lightskyblue', alpha=0.3)
    ax.axhspan(40, 70, facecolor='yellow', alpha=0.3)
    ax.axhspan(70, 90, facecolor='orange', alpha=0.3)
    ax.axhspan(90, 120, facecolor='red', alpha=0.3)

    # Text für die Hörgrade direkt neben die y-Achse setzen
    ax.text(52, 15, 'Normalhörigkeit', ha='left', va='center', fontsize=8, color='black')
    ax.text(52, 35, 'Leichte Schwerhörigkeit', ha='left', va='center', fontsize=8)
    ax.text(52, 65, 'Mittlere Schwerhörigkeit', ha='left', va='center', fontsize=8)
    ax.text(52, 85, 'Schwere Schwerhörigkeit', ha='left', va='center', fontsize=8)
    ax.text(52, 115, 'Hochgradige Schwerhörigkeit', ha='left', va='center', fontsize=8)

    # Plot der Hörschwellen
    ax.plot(np.log2(freqs), right_values, marker='o', linestyle='-', color='firebrick', label='rechtes Ohr')
    ax.plot(np.log2(freqs), left_values, marker='x', linestyle='-', color='dodgerblue', label='linkes Ohr')

    # Achsne invertieren und beschriften
    ax.invert_yaxis()  
    ax.set_title('Audiogramm')
    ax.set_xlabel('Frequenzen (Hz)')
    ax.set_ylabel('Hörschwelle (dB HL)')
    ax.set_ylim(120, -10)

    # Benutzerdefinierte x-Achsen-Ticks
    x_ticks = np.log2(freq)
    x_labels = [f"{int(freq)} Hz" for freq in freqs]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels)


    ax.set_yticks(np.arange(0, 121, 10))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)  # Grid for better readability
    ax.legend(loc='upper right')
    
    return fig

#Beispielwerte
freq = [63, 125, 250, 500, 1000, 2000, 4000, 8000]
dummy_right = [10, 15, 20, 25, 30, 35, 40, 45]
dummy_left = [5, 10, 15, 20, 25, 30, 35, 40]
# # Audiogramm erstellen
create_audiogram(freq, dummy_right, dummy_left)
plt.show()

