import numpy as np

def la2v(lengths, angles):
    alpha = angles[0] * np.pi / 180
    beta = angles[1] * np.pi / 180
    gamma = angles[2] * np.pi / 180

    a = np.array([lengths[0], 0.0, 0.0])
    b = np.array([lengths[1]*np.cos(gamma), lengths[1]*np.sin(gamma), 0.0])
    cx = lengths[2]*np.cos(beta)
    cy = lengths[2]*(np.cos(alpha) - np.cos(beta)*np.cos(gamma)) / np.sin(gamma)
    cz = np.sqrt(lengths[2]*lengths[2] - cx*cx - cy*cy)
    c = np.array([cx,cy,cz])

    v = np.array((a,b,c))
    # Make sure that all vector components that are _almost_ 0 are set exactly
    # to 0
    tol = 1e-6
    v[np.logical_and(v>-tol, v<tol)] = 0.0

    return v

def v2la(vectors):
    a = vectors[0]
    b = vectors[1]
    c = vectors[2]

    a_length = np.sqrt(np.sum(a*a))
    b_length = np.sqrt(np.sum(b*b))
    c_length = np.sqrt(np.sum(c*c))

    if min(a_length, b_length, c_length) == 0:
        a_length = 0.0
        b_length = 0.0
        c_length = 0.0
        alpha = 90.0
        beta = 90.0
        gamma = 90.0
    else:
        alpha = np.arccos(np.dot(b, c) / (b_length * c_length))
        beta = np.arccos(np.dot(c, a) / (c_length * a_length))
        gamma = np.arccos(np.dot(a, b) / (a_length * b_length))

        alpha = alpha * 180.0 / np.pi
        beta = beta * 180.0 / np.pi
        gamma = gamma * 180.0 / np.pi

    return [a_length, b_length, c_length], [alpha, beta, gamma]

