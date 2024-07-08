import matplotlib.pyplot as plt
import numpy as np

def create_audiogram(freqs, left_values=None, right_values=None, binaural=False, save=False, name="audiogram.png"):
    """Erstellt ein Audiogramm basierend auf den gegebenen Frequenzen und Hörschwellenwerten mit benutzerdefinierten x-Achsen-Beschriftungen.

    Args:
        freqs (list of int): Eine Liste von Frequenzen in Hertz.
        right_values (list of int): Eine Liste von Hörschwellen in dB HL vom rechten Ohr.
        left_values (list of int): Eine Liste von Hörschwellen in dB HL vom linken Ohr
        save (bool): Ob das Diagramm gespeichert werden soll
        name (str): Der Name der Datei, wenn das Diagramm gespeichert werden soll
    """
    print("Creating audiogram with frequencies:", freqs)
    print("Left ear values:", left_values)
    print("Right ear values:", right_values)

    fig, ax = plt.subplots(figsize=(10, 6))  # Größeres Diagramm

    # Bereichsfarben hinzufügen
    ax.axhspan(-10, 20, facecolor='lightgreen', alpha=0.3)
    ax.axhspan(20, 40, facecolor='lightskyblue', alpha=0.3)
    ax.axhspan(40, 70, facecolor='yellow', alpha=0.3)
    ax.axhspan(70, 90, facecolor='orange', alpha=0.3)
    ax.axhspan(90, 120, facecolor='red', alpha=0.3)

    # Text für die Hörgrade direkt neben die y-Achse setzen
    ax.text(8, 15, 'Normalhörigkeit', ha='left', va='center', fontsize=10, color='black')
    ax.text(8, 30, 'Leichte Schwerhörigkeit', ha='left', va='center', fontsize=10)
    ax.text(8, 55, 'Mittlere Schwerhörigkeit', ha='left', va='center', fontsize=10)
    ax.text(8, 80, 'Schwere Schwerhörigkeit', ha='left', va='center', fontsize=10)
    ax.text(8, 105, 'Hochgradige Schwerhörigkeit', ha='left', va='center', fontsize=10)

    # Plot der Hörschwellen
    if binaural:
        ax.plot(range(len(freqs)), left_values, marker='o', markersize=10, linestyle='-', color='black', markerfacecolor='none')
        ax.plot(range(len(freqs)), left_values, marker='x', markersize=8, linestyle='None', color='black')
    
    else: 
        if right_values:
            ax.plot(range(len(freqs)), right_values, markersize=12, marker='o', linestyle='-', linewidth=2, color='firebrick', label='rechtes Ohr', markerfacecolor='white')

        if left_values:
            ax.plot(range(len(freqs)), np.array(left_values)+0.4,  markersize=12, marker='x', linestyle='-', linewidth=2, color='dodgerblue', label='linkes Ohr')

    # Achse invertieren und beschriften
    ax.invert_yaxis()  
    ax.set_title('Audiogramm', fontsize=16)
    ax.set_xlabel('Frequenzen (Hz)', fontsize=14)
    ax.set_ylabel('Hörschwelle (dB HL)', fontsize=14)
    ax.set_ylim(120, -10)

    # Benutzerdefinierte x-Achsen-Ticks
    ax.set_xticks(range(len(freqs)))  # Setze die Ticks auf gleichmäßige Abstände
    ax.set_xticklabels([f"{int(freq)}" for freq in freqs], fontsize=12)  # Benutzerdefinierte Beschriftungen

    ax.set_yticks(np.arange(0, 121, 10))
    ax.set_yticklabels(np.arange(0, 121, 10), fontsize=12)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)  # Grid for better readability
    
    if not binaural:
        ax.legend(loc='upper right', fontsize=12)

    if save:
        plt.savefig(name)
        print(f"Saved audiogram as {name}")
        return name
    
    print("Displaying audiogram")
    return fig

