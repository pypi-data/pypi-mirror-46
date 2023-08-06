# *-* encoding: utf-8 *-*

import numpy as np
import scipy
from .math import strictly_positify, positify, clip01
from .misc import PB

def psf(img, sx, sy=None, angle=0):
    """
    Return a Gaussian PSF of the same size as img.

    img: image (reference for the output size)
    sx: sigma value for the long axis
    sy: sigma value for the short axis. If None take the same value as sx [default]
    angle: geometric angle (in radian) of the long axis. [default: 0]
    """
    from .math import Gauss
    if sy is None:
        sy = sx
    x = np.arange(img.shape[1])
    y = np.arange(img.shape[0])
    X, Y = np.meshgrid(x,y)
    X -= img.shape[1]//2
    Y -= img.shape[0]//2
    if angle != 0:
        Xp = X*np.cos(angle) - Y*np.sin(angle)
        Yp = X*np.sin(angle) + Y*np.cos(angle)
    else:
        Xp = X
        Yp = Y
    return Gauss(Xp, 0, sx)*Gauss(Yp, 0, sy)
        
def _rl(x, image, psf, type='default', extend=True, damping=0, ndamp=10, ext_decay=0, stat='Poisson', N=1, **kargs):
    """
    Richardson-Lucy core algorithm
    Reference: L. B. Lucy / The Astronomical Journal / vol. 79 / No. 6 / June 1974 / pp. 745-754

    By giving an estimate x_k this function returns the next estimate x_{k+1}.
    
    x: x_k estimate
    image: input image to enhance
    psf: point spread functional
    """
    I = strictly_positify(convolve(x, psf, type=type, extend=extend, decay=ext_decay)) # reconvoluted estimation.
    assert stat in ['poisson','binomial','binom']
    if stat in ['binomial','binom']:
        I = 1-np.exp(-I)
        image = image / N
    if damping != 0:
        ratio = _rl_damped(I, image, damping=damping, ndamp=ndamp, **kargs)
    else:
        ratio  = image / I
    return x * convolve(ratio, psf[::-1,::-1], type=type, extend=extend, decay=ext_decay) # Correlation is the convolution of mirrored psf

    
def _rl_damped(I, image, con_var=None, damping=1, ndamp=10, **kargs):
    """ Calculate the damping ratio
    
    Parameters
    ----------
    con_var: float, int, np.ndarray
        Noise value or image
    threshold: float, int
        noise sigma threshold for dampening
    ndamp: float, int
        order of the dampening
    """
    
    from .haar import hfilter
    
    if con_var is None:
        con_var = np.sqrt(I)
    rrr = image - I
    rrr = hfilter(rrr, I+con_var, damping, ndamp=ndamp)
    rrr[np.isnan(rrr)] = 0
    ratio = 1 + rrr / (I+con_var)
    return ratio

def _rl_accelerate(x, x1, x2, g1=None, g2=None, order=1):
    """
    Accelerated Richardson-Lucy algorithm.
    Reference: David S. C. Biggs and Mark Andrews, Appl. Opt./ Vol. 36 / No. 8 / 10 March 1997 / pp. 1766-1775
    
    Notation in reference to paper:
    x  = x_k
    x1 = x_{k-1}
    x2 = x_{k_2}
    g1 = g_{k-1}
    g2 = g_{k-2}
    y  = y_k
    """
    
    if g2 is None:
        alpha = 0 # Initialization
    else:
        alpha = np.sum(g1*g2)/strictly_positify(np.sum(g2**2)) # Eq. 10
        alpha = clip01(alpha) # be sure α∈[0,1]
    if alpha == 0:
        return x # the prediction is the same as x (initialization)
    h1 = x - x1 # Eq. 7
    y = x + alpha * h1 # Eq. 6
    if order>1:
        h2 = x - 2*x1 + x2 # Eq. 17
        y += h2 * alpha**2 / 2 # Eq. 14
    return y

    
def richardson_lucy(image, psf, iterations, damping=0, ndamp=10,
        core='default', acceleration=2, init='mean', extend=True, clip=False, ext_decay=0, stat='Poisson', pb_callback=None, **kargs):
    """
    Richardson-Lucy algorithm
    image:
        the image to enhance (numpy 2d array)
    psf:
        the Point Spread Function (numpy 2d array)
    iterations:
        The number of iterations to perform. It can be either an integer or a list of integer.
        For the later case, the returned solution is a dictionary with keys K and value being the enhancement after K interations.
    core:
        default: default R-L algorithm using convolve from scipy.signal (I think that scipy switch automatically to convolve if faster)
        fft: performs a fftconvolution (I think that scipy switch automatically to convolve if faster)
        accurate: real integral calculation (slow)
        fft2: real 2D fft
    acceleration:
        0: (No acceleration. standard R-L)
        1: First order acceleration     
        2: (default) Second order acceleration
        higher orders are not yet implemented
    damping:
        damping factor. (0= no damping)
    stat: Poisson or Binomial
        Statistics used for the restoration. The default is the traditional Poisson statistics.
    init:
        'mean': (default) The start value for x is the mean of the image
        'image': the start value x is the image itself
        numpy array: if init is a 2d numpy array, its value will be used as init value for x
    ext_decay:
        the exponential decay factor used in the img_extended for each convolution
    """
    assert core in ['default', 'fft', 'accurate', 'fft2']
        
    image = image.astype(np.float)
    psf = psf.astype(np.float)
    psf /= np.sum(psf) # Normalize the psf ⇒ ∫∫ psf(x,y) dx dy = 1
    stat = stat.lower()
    assert stat in ['poisson','binomial','binom']
    
    if init is 'mean':
        if stat in ['binomial','binom']:
            assert 'N' in kargs
            # Perform the Poisson-correction to the data if the statistics is Binomial
            # Note that the Poisson-correction term is a convention in the ToF-SIMS community, but its name is inaccurate as it is a Binomial-Poisson-correction
            x = np.full(image.shape, -np.log(1-np.fmin(np.mean(image)/kargs['N'], .999)))
        else:
            x = np.full(image.shape, np.mean(image))
    elif init is 'image':
        x = np.copy(image)
    else:
        x = init
            
    # Is iterations a number of a list of number?
    dict_output = True
    if type(iterations) is int:
        dict_output = False
        iterations = [iterations]
  
    N = max(iterations)
        
    results = {}
    x1 = x2 = None
    g1 = g2 = None
    Ns = range(N)
    if kargs.get('prog', False):
        Ns = PB(Ns)
        
    for i in Ns:
        if pb_callback is not None:
            pb_callback(i)
        if acceleration:
            y = _rl_accelerate(x, x1, x2, g1, g2, order=acceleration)
        else:
            y = x
        x_new = _rl(positify(y), image=image, psf=psf, extend=extend, type=core, damping=damping, ndamp=ndamp, ext_decay=ext_decay, stat=stat, **kargs)
        g2 = g1
        g1 = x_new - y
        x, x1, x2 = x_new, x, x1 # rotate elements for next iteration
        if clip:
            x[x<0] = 0
            x[x>clip] = clip
        if i+1 in iterations:
            results[i+1] = np.copy(x)
    if dict_output:
        return results
    return results[N]
    
def img_extend(img, margin, block=1, decay=0):
    """
    Pad the image and use the mean value of its border to fill the new pixels
    img:
        The image to pad/extend
    margin: int (in pixel)
        The number of pixel to extend (in every direction, so the image will be larger by 2*margin)
    block: int (in pixel) [default: 1]
        the number of pixels to use to calculate the average
    decay: float [default: 0]
        A decay value to have the value slowly decaying at the border.
        0 means no decay
    """
    if block == 1:
        I = np.pad(img, margin, 'edge')
    else:
        I = np.pad(img, margin, 'constant')
        xr = margin-np.arange(margin)
        x = np.arange(margin)
        X,Y = np.meshgrid(x,x)
        Xr,Yr = np.meshgrid(xr,xr)
        if decay > 0:
            for i in range(img.shape[1]):
                I[:margin, i+margin] = np.mean(img[:block, i])*np.exp(-xr*decay)
                I[-margin:, i+margin] = np.mean(img[-block:, i])*np.exp(-x*decay)
            for i in range(img.shape[0]):
                I[i+margin, :margin] = np.mean(img[i, :block])*np.exp(-xr*decay)
                I[i+margin, -margin:] = np.mean(img[i, -block:])*np.exp(-x*decay)
            I[:margin, :margin] = np.mean(img[:block, :block])*np.exp(-np.sqrt(Xr**2+Yr**2)*decay)
            I[:margin, -margin:] = np.mean(img[:block, -block:])*np.exp(-np.sqrt(X**2+Yr**2)*decay)
            I[-margin:, :margin] = np.mean(img[-block:, :block])*np.exp(-np.sqrt(Xr**2+Y**2)*decay)
            I[-margin:, -margin:] = np.mean(img[-block:, -block:])*np.exp(-np.sqrt(X**2+Y**2)*decay)
        else:
            for i in range(img.shape[1]):
                I[:margin, i+margin] = np.mean(img[:block, i])
                I[-margin:, i+margin] = np.mean(img[-block:, i])
            for i in range(img.shape[0]):
                I[i+margin, :margin] = np.mean(img[i, :block])
                I[i+margin, -margin:] = np.mean(img[i, -block:])
            I[:margin, :margin] = np.mean(img[:block, :block])
            I[:margin, -margin:] = np.mean(img[:block, -block:])
            I[-margin:, :margin] = np.mean(img[-block:, :block])
            I[-margin:, -margin:] = np.mean(img[-block:, -block:])
    return I
    
def convolve(img, psf, type_='default', extend=True, mode='same', extend_margin=100, decay=0, **kargs):
    """
    Compute the convolution of two 2D signals: img and psf
    type:
        define the convolution type
    """
    if type(extend) in [tuple, list]:
        extend_margin = extend[0]
        block = extend[1]
    else:
        block = 1
    if extend is int:
        extend_margin = extend
       
    if extend:
        img = img_extend(img, extend_margin, decay=decay, block=block)
        if type_ is 'fft2':
            psf =  np.pad(psf, extend_margin, 'constant')
        
    if type_ is 'fft':
        from scipy.signal import fftconvolve as conv
        I = conv(img, psf, mode)
    elif type_ is 'default':
        from scipy.signal import convolve as conv
        I = conv(img, psf, mode)
    elif type_ is 'accurate':
        from scipy.signal import convolve2d as convolve
        I = conv(img, psf, mode)
    elif type_ is 'fft2':
        I = np.fft.fftshift((np.fft.irfft2(np.fft.rfft2(img) * np.fft.rfft2(psf))))
    
    if extend:
        I = I[extend_margin:-extend_margin, extend_margin:-extend_margin]
        
    return I
