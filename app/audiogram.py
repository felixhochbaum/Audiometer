import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# TODO screening -> not heard

freq_levels = {125: 20, 250: 20, 500: 20, 1000: 20, 2000: 20, 4000: 20, 8000: 20}

def split_values(x_vals, values, target_values):

    heard = np.array([[i,v] for i, v in zip(x_vals, values) if v != 'NH']).T
    if len(heard) == 0: heard_i, heard_level = [], []
    else: heard_i, heard_level = heard
    
    not_heard = np.array([[i,t] for i, v, t in zip(x_vals, values, target_values) if v == 'NH']).T
    if len(not_heard) == 0: not_heard_i, not_heard_level = [], []
    else: not_heard_i, not_heard_level = not_heard
    
    return heard_i, heard_level, not_heard_i, not_heard_level


def create_audiogram(freqs, left_values=None, right_values=None, binaural=False, name="audiogram.png", freq_levels=freq_levels):
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
    t1 = ax.text(6.4, 5, 'Normalhörigkeit', ha='left', va='center', fontsize=10, color='black')
    t2 = ax.text(6.4, 30, 'Leichte Schwerhörigkeit', ha='left', va='center', fontsize=10)
    t3 = ax.text(6.4, 55, 'Mittlere Schwerhörigkeit', ha='left', va='center', fontsize=10)
    t4 = ax.text(6.4, 80, 'Schwere Schwerhörigkeit', ha='left', va='center', fontsize=10)
    t5 = ax.text(6.4, 105, 'Hochgradige Schwerhörigkeit', ha='left', va='center', fontsize=10)

    x_vals = range(len(freqs))
    target_values = list(freq_levels.values())

    # Plot der Hörschwellen
    if 'NH' in left_values or 'NH' in right_values:
        
        heard_i_left, heard_level_left, not_heard_i_left, not_heard_level_left = split_values(x_vals, left_values, target_values)
        heard_i_right, heard_level_right, not_heard_i_right, not_heard_level_right = split_values(x_vals, right_values, target_values)
        
        if binaural:
            ax.plot(x_vals, target_values, linestyle='-', color='black')
            ax.plot(heard_i_left, heard_level_left, marker='o', markersize=10, linestyle='-', color='black', markerfacecolor='none')
            ax.plot(heard_i_left, heard_level_left, marker='x', markersize=8, linestyle='None', color='black', label='gehört')
            ax.plot(not_heard_i_left, not_heard_level_left, marker='|', markersize=10, linestyle='None', color='black', label='nicht gehört')

        else:
            ax.plot(x_vals, target_values, linestyle='-', color='firebrick')
            ax.plot(x_vals,  np.array(target_values)+0.4, linestyle='-', color='dodgerblue')

            ax.plot(heard_i_right, heard_level_right, markersize=12, marker='o', linewidth=2, color='firebrick', markerfacecolor='none', label='rechts gehört', linestyle='None')
            ax.plot(heard_i_left, np.array(heard_level_left)+0.4, markersize=12, marker='x', linewidth=2, label='links gehört', color='dodgerblue', linestyle='None')
            
            ax.plot(not_heard_i_right, not_heard_level_right, markersize=12, marker='|', linewidth=2, color='firebrick', label='rechts nicht gehört', linestyle='None')
            ax.plot(not_heard_i_left, np.array(not_heard_level_left)+0.4, markersize=12, marker='|', linewidth=2, label='links nicht gehört', color='dodgerblue', linestyle='None')
    
    else:
        if binaural:
            ax.plot(x_vals, left_values, marker='o', markersize=10, linestyle='-', color='black', markerfacecolor='none')
            ax.plot(x_vals, left_values, marker='x', markersize=8, linestyle='None', color='black')
        
        else: 
            ax.plot(x_vals, right_values, markersize=12, marker='o', linestyle='-', linewidth=2, color='firebrick', label='rechtes Ohr')
            ax.plot(x_vals, np.array(left_values)+0.4,  markersize=12, marker='x', linestyle='-', linewidth=2, color='dodgerblue', label='linkes Ohr')

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
    
    # Legende außerhalb des Diagramms aber noch sichtbar im Bild
    lgd = ax.legend(loc='upper left', bbox_to_anchor=(0, -0.15), fontsize=11, frameon=False)
    #lgd = ax.legend(loc='lower left', fontsize=11)
    fig.savefig(name, bbox_extra_artists=(lgd, t1, t2, t3, t4, t5), bbox_inches='tight')
    plt.close(fig)

    

freqs = [125, 250, 500, 1000, 2000, 4000, 8000]
left_values = [20, 'NH', 20, 20, 20, 20, 20]
right_values = [20, 10, 20, 10, 20, 10, 20]
right_values = [20, 'NH', 20, 'NH', 20, 'NH', 20]
freq_levels = {125: 20, 250: 20, 500: 20, 1000: 20, 2000: 20, 4000: 20, 8000: 20}

a = create_audiogram(freqs, left_values=left_values, right_values=right_values, binaural=False)

