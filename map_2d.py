import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
"""
Plot discrete square 2d map
"""
def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
            
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)
def plot_2d_map(n_res,
                matrix,
                highlight_matrix=None,
                ):
    """
    Plot square 2d map.
      
    Parameters
    ----------

    n_res : int
    Size of a square grid. The plot produzed has each axis devided into `grid_size` elements 

    matrix : 2d numpy array n_res x n_res
            Matrix with values to be plotted with colormap

    highlight_matrix : 2d numpy array n_res x n_res. default None
                      Contains 1.0 for grid elements to be highlighted and 0.0 otherwise


    """
    
    fig = plt.figure(figsize=(12,10))

    matplotlib.rcParams.update({"font.size":20})
    matplotlib.rcParams.update({"xtick.labelsize":12})
    matplotlib.rcParams.update({"ytick.labelsize":12})

    plt.xlabel("i", size=20)
    plt.ylabel("j", size=20)
    plt.tick_params(labelsize=15)
    plt.axis([0.5, n_res+0.5, 0.5, n_res+0.5])
    
    xx = np.arange(0,n_res+2,0.1)
    for idx in range(1,n_res+1):
        plt.plot(xx*0.+idx, xx, linewidth=0.05, color ='gray',alpha=0.2,zorder=3)
        plt.plot(xx, xx*0.+idx, linewidth=0.05, color ='gray',alpha=0.2,zorder=3)
        
    for idx in range(0,n_res+1,10):
        plt.plot(xx*0.+idx, xx, linewidth=0.5, color ='gray',alpha=0.8,zorder=3)
        plt.plot(xx, xx*0.+idx, linewidth=0.5, color ='gray',alpha=0.8,zorder=3)
    

    vmin = np.min(matrix)
    vmax = np.max(matrix) 
    string = "%s%8.3f%s%8.3f" % ('Value Min = ', vmin, 'Value Max =', vmax)
    print(string)

    dv=vmax+abs(vmin)
    mid = abs(vmin)/dv

    c = mcolors.ColorConverter().to_rgb
    frac = 1.-abs(vmin)/vmax
    cred = (1, frac, frac)
    rvb = make_colormap([cred, c('white'),  mid, c('white'), c('blue')])

    plt.register_cmap(name=rvb.name, cmap=rvb)
    plt.register_cmap(name='rvb', cmap=rvb)
    plt.set_cmap(rvb)
    
    tol = 1e-06
    
    edges = np.arange(0.5, n_res+1, 1)
    
    qmesh = plt.pcolormesh(edges, edges, matrix.T, vmin=vmin, vmax=vmax, cmap='rvb',zorder=2)
    plt.plot([0, n_res + 1], [0, n_res + 1], color="k", linewidth=2, zorder=4)
    cb = plt.colorbar(qmesh)
    cb.set_label("Contact energy, kJ/(K*mol)", size=16)

    if highlight_matrix is not None:
        for idx in range(n_res):
            for jdx in range(0,n_res):
                if (highlight_matrix[idx, jdx] == 1.):
                     plt.plot([idx+1],[jdx+1], marker='s', ms=7, color='black', fillstyle='none', zorder=5, linewidth=0.)
    return fig, cb
