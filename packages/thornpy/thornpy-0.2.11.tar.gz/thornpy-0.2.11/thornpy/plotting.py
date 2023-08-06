import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3d(x, y, z, figure=None, x_label='X', y_label='Y', z_label='Z'):    
    """Creates a 3D plot using matplotlib
    
    Parameters
    ----------
    x : list
        X values (can be :class:`numpy.array` or :class:`Pandas.Series`)
    y : list
        Y values (can be :class:`numpy.array` or :class:`Pandas.Series`)
    z : list
        Z values (can be :class:`numpy.array` or :class:`Pandas.Series`)
    figure : matplotlib.figure.Figure, optional
        Existing figure to add to (the default is None, which creates a new figure)
    x_label : str, optional
        X axis label (the default is 'X')
    y_label : str, optional
        Y axis label (the default is 'Y')
    z_label : str, optional
        Z axis label (the default is 'Z')

    Returns
    -------
    matplotlib.figure.Figure
        3D plot of x, y, and z
    
    """
    if figure is None:
        figure = plt.figure()
    axis = figure.gca(projection='3d')
    axis.plot(x, y, z, zdir='z')
    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)
    axis.set_zlabel(z_label)
    axis.axis('equal')

    return figure