import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
# from matplotlib.offsetbox import OffsetImage, AnnotationBbox (für costum marker)


COLOR_LEFT = 'dodgerblue'
COLOR_RIGHT = 'firebrick'
COLOR_BINAURAL = 'black'
LINE_WIDTH = 2
MARKER_SIZE = 12
MARKER_EDGE_WIDTH = LINE_WIDTH
SHIFT = 0.4
MARKER_LEFT = 'x'
MARKER_RIGHT = 'o'
NOT_HEARD_MARKER = '|' # es können auch costum Marker verwendet werden (.png ohne Hintergrund)


freq_levels = {125: 20, 250: 20, 500: 20, 1000: 20, 2000: 20, 4000: 20, 8000: 20}

def split_values(x_vals, values, target_values):
    heard = np.array([[i, int(v)] for i, v in zip(x_vals, values) if v != 'NH']).T
    if len(heard) == 0:
        heard_i, heard_level = [], []
    else:
        heard_i, heard_level = heard

    not_heard = np.array([[i, t] for i, v, t in zip(x_vals, values, target_values) if v == 'NH']).T
    if len(not_heard) == 0:
        not_heard_i, not_heard_level = [], []
    else:
        not_heard_i, not_heard_level = not_heard

    return np.array(heard_i, dtype=int), np.array(heard_level, dtype=int), np.array(not_heard_i, dtype=int), np.array(not_heard_level, dtype=int)


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

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.axhspan(-10, 20, facecolor='lightgreen', alpha=0.2)
    ax.axhspan(20, 40, facecolor='lightskyblue', alpha=0.2)
    ax.axhspan(40, 70, facecolor='yellow', alpha=0.2)
    ax.axhspan(70, 90, facecolor='orange', alpha=0.2)
    ax.axhspan(90, 120, facecolor='red', alpha=0.2)

    t1 = ax.text(6.4, 5, 'Normalhörigkeit', ha='left', va='center', fontsize=8)
    t2 = ax.text(6.4, 30, 'Leichte\nSchwerhörigkeit', ha='left', va='center', fontsize=8)
    t3 = ax.text(6.4, 55, 'Mittlere\nSchwerhörigkeit', ha='left', va='center', fontsize=8)
    t4 = ax.text(6.4, 80, 'Schwere\nSchwerhörigkeit', ha='left', va='center', fontsize=8)
    t5 = ax.text(6.4, 105, 'Hochgradige\nSchwerhörigkeit', ha='left', va='center', fontsize=8)

    x_vals = range(len(freqs))
    target_values = np.array(list(freq_levels.values()))
    left_values, right_values = np.array(left_values), np.array(right_values)

    if 'NH' in left_values or 'NH' in right_values:
        
        heard_i_left, heard_level_left, not_heard_i_left, not_heard_level_left = split_values(x_vals, left_values, target_values)
        heard_i_right, heard_level_right, not_heard_i_right, not_heard_level_right = split_values(x_vals, right_values, target_values)
        
        if binaural:
            ax.plot(x_vals, target_values, linestyle='-', color=COLOR_BINAURAL)
            ax.plot(heard_i_left, heard_level_left, marker=MARKER_RIGHT, markersize=MARKER_SIZE, linestyle='-', color=COLOR_BINAURAL, markerfacecolor='none')
            ax.plot(heard_i_left, heard_level_left, marker=MARKER_LEFT, markersize=MARKER_SIZE, linestyle='None', color=COLOR_BINAURAL, label='gehört')
            ax.plot(not_heard_i_left, not_heard_level_left, marker=NOT_HEARD_MARKER, markersize=MARKER_SIZE, linestyle='None', color=COLOR_BINAURAL, label='nicht gehört')
        else:
            ax.plot(x_vals, target_values, linestyle='-', color=COLOR_RIGHT)
            ax.plot(heard_i_right, heard_level_right, marker=MARKER_RIGHT, markersize=MARKER_SIZE, linestyle='None', linewidth=LINE_WIDTH, color=COLOR_RIGHT, markerfacecolor='none', markeredgewidth=MARKER_EDGE_WIDTH, label='rechts gehört')
            ax.plot(not_heard_i_right, not_heard_level_right, marker=NOT_HEARD_MARKER, markersize=MARKER_SIZE, linestyle='None', linewidth=LINE_WIDTH, color=COLOR_RIGHT, markeredgewidth=MARKER_EDGE_WIDTH, label='rechts nicht gehört')
            
            ax.plot(x_vals, target_values+SHIFT, linestyle='-', color=COLOR_LEFT)
            ax.plot(heard_i_left, heard_level_left+SHIFT, marker=MARKER_LEFT, markersize=MARKER_SIZE, linestyle='None', linewidth=LINE_WIDTH, color=COLOR_LEFT, markeredgewidth=MARKER_EDGE_WIDTH, label='links gehört')
            ax.plot(not_heard_i_left, not_heard_level_left+SHIFT, marker=NOT_HEARD_MARKER, markersize=MARKER_SIZE, linestyle='None', linewidth=LINE_WIDTH, color=COLOR_LEFT, markeredgewidth=MARKER_EDGE_WIDTH, label='links nicht gehört')
    else:
        if binaural:
            ax.plot(x_vals, left_values, marker=MARKER_RIGHT, markersize=MARKER_SIZE, linestyle='-', color=COLOR_BINAURAL, markerfacecolor='none')
            ax.plot(x_vals, left_values, marker=MARKER_LEFT, markersize=MARKER_SIZE, linestyle='None', color=COLOR_BINAURAL)
        else: 
            ax.plot(x_vals, right_values, marker=MARKER_RIGHT, markersize=MARKER_SIZE, linestyle='-', linewidth=LINE_WIDTH, color=COLOR_RIGHT, markeredgewidth=MARKER_EDGE_WIDTH, label='rechtes Ohr')
            ax.plot(x_vals, left_values+SHIFT, marker=MARKER_LEFT, markersize=MARKER_SIZE, linestyle='-', linewidth=LINE_WIDTH, color=COLOR_LEFT, markeredgewidth=MARKER_EDGE_WIDTH, label='linkes Ohr')

    ax.invert_yaxis()  
    ax.set_title('Audiogramm', fontsize=16)
    ax.set_xlabel('Frequenzen (Hz)', fontsize=14)
    ax.set_ylabel('Hörschwelle (dB HL)', fontsize=14)
    ax.set_ylim(120, -10)

    ax.set_xticks(range(len(freqs))) 
    ax.set_xticklabels([f"{int(freq)}" for freq in freqs], fontsize=12) 

    ax.set_yticks(np.arange(0, 121, 10))
    ax.set_yticklabels(np.arange(0, 121, 10), fontsize=12)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5) 
    
    lgd = ax.legend(loc='upper left', bbox_to_anchor=(1.15, 0.205), fontsize=11, frameon=False)
    fig.savefig(name, bbox_extra_artists=(lgd, t1, t2, t3, t4, t5), bbox_inches='tight')
    plt.close(fig)


# Beispielaufruf
freqs = [125, 250, 500, 1000, 2000, 4000, 8000]
left_values = [20, 'NH', 20, 20, 20, 20, 20]
right_values = [20, 'NH', 20, 'NH', 20, 'NH', 20]
freq_levels = {125: 20, 250: 20, 500: 20, 1000: 20, 2000: 20, 4000: 20, 8000: 20}

create_audiogram(freqs, left_values=left_values, right_values=right_values, binaural=False)
