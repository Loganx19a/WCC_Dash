from assets.color_palettes import ACTIVE_PALETTE

# Figure layout to use for all plots
my_figlayout = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'color': ACTIVE_PALETTE['text']},
    'margin': {'b': 10, 'l': 50, 'r': 8, 't': 50, 'pad': 0},
    'xaxis': {
        'linewidth': 1,
        'linecolor': 'rgba(0, 0, 0, 0.35)',
        'showgrid': False,
        'zeroline': False
    },
    'yaxis': {
        'linewidth': 1,
        'linecolor': 'rgba(0, 0, 0, 0.35)',
        'showgrid': True,
        'gridwidth': 1,
        'gridcolor': ACTIVE_PALETTE['grid'],
        'zeroline': False
    }
}

# Line style for plots
my_linelayout = {
    'width': 2,
    'color': ACTIVE_PALETTE['primary']
}