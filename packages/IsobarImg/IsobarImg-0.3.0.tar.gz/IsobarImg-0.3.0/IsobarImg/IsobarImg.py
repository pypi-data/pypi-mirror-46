# -*- coding: utf-8 -*-
#
# IsobarImg.py
#
# Usage:
#    import IsobarImg
#    o = IsobarImg.overlayImage(bg_fn="bg.jpg", fg_fn="title.png")
#    o.save("test.png")

import cv2
from PIL import Image, ImageOps, ImageEnhance

def overlayImage(bg_fn, fg_fn):
    """overlay an transparent image
    
    Arguments:
        bg_fn {str} -- bg image filename
        fg_fn {str} -- fg image filename
    
    Returns:
        image -- PIL image object
    """
    bg = Image.open(bg_fn)
    fg = Image.open(fg_fn)
    if bg.mode == 'RGB':
        bg = bg.convert("RGBA")
    if fg.mode == 'RGB':
        fg = fg.convert("RGBA")
    return Image.alpha_composite(bg, fg)

def denoiseImage(img_fn, d=5, sigma_color=30, sigma_space=30):
    """denoise an image
    
    Arguments:
        img_fn {str} -- image filename
    
    Keyword Arguments:
        d {int} -- diameter of each pixel neighborhood (default: {5}) 5,9
        sigma_color {int} -- sigma in color space (default: {30}) 30,50,75
        sigma_space {int} -- sigma in coordinate space (default: {30}) 30,50,75
    
    Returns:
        image -- PIL image object
    """
    img = cv2.imread(img_fn)
    out = cv2.bilateralFilter(img, d, sigma_color, sigma_space)
    return Image.fromarray(out[:,:,(2,1,0)])

def getScale(size, w, h):
    """calculate the scale of image
    
    Arguments:
        size {tuple} -- image size
        w {float} -- width
        h {float} -- height
    
    Returns:
        [type] -- [description]
    """

    scale = min(w/size[0], h/size[1])
    if scale > 1.0:
        return int((w-size[0])*0.5),int((h-size[1])*0.5)
    else:
        return int((w-size[0]*scale)*0.5),int((h-size[1]*scale)*0.5)

def aspectFit(img_fn, fillColor=(255,255,255), w=1080.0, h=1920.0):
    """scale the image to fit
    
    Arguments:
        img_fn {str} -- image filename
    
    Keyword Arguments:
        fillColor {tuple} -- fill color (default: {(255,255,255)})
        w {float} -- width (default: {1080.0})
        h {float} -- height (default: {1920.0})
    
    Returns:
        image -- PIL image object
    """
    img = Image.open(img_fn)
    s = getScale(img.size, w, h)
    return ImageOps.expand(img, (s[0],s[1],s[0],s[1]), fill=fillColor)

def beautifyImage(img_fn):
    """beautify the image
    
    Arguments:
        img_fn {str} -- image filename
    
    Returns:
        image -- PIL image object
    """
    img = denoiseImage(img_fn)
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(1.1)
