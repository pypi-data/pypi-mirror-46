# -*- coding: utf-8 -*-
"""
Utility functions for computing triangle angles, converting between cartesian and polar coordinates, and adjusting plotting colors.

Created on Tue May 14 13:49:52 2019

@author: ecramer <eric.cramer@curie.fr>
"""

import numpy as np

def cartToPolar(x, y):
    """
    Converts (x, y) Cartesian points to polar coordinates.
    """
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return (rho, phi)

def polToCart(rho, phi):
    """
    Converts (rho, phi) polar coordinates to Cartesian coordinates.
    """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)

def lawOfCosines(a, b, c):
    """
    Returns the angle measurements of angle A (opposite to side a).
    """
    ang = np.arccos((a**2 - b**2 - c**2)/(-2.0*b*c))
    return ang

def calcCentroid(radii, angles):
    """
    Calculates the centroid of a triangle whose vertices are given polar 
    coordinates, and returns the centroid in Cartesian coordinates.
    """
    carts = [polToCart(radius, ang) for radius, ang in zip(radii, angles)]
    Cx = (1/3.0)*np.asarray([x[0] for x in carts]).sum()
    Cy = (1/3.0)*np.asarray([y[1] for y in carts]).sum()
    return (Cx, Cy)

def adjustColor(color, amount=0.5):
    """
    Adjusts the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> adjust_color('g', 0.3)
    >> adjust_color('#F034A3', 0.6)
    >> adjust_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

def _test():
    radii = 0.501145, 0.352592, 0.146263
    angles = np.deg2rad(np.asarray([90, 225, 315]))	
    centroid = list(calcCentroid(radii, angles))
    print(centroid)

if __name__ == "__main__":
    _test()
