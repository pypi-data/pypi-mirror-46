
from IPython.display import Image, display


def display_colormap():
    """ Display basic color map in ipython"""
    url = 'https://python-graph-gallery.com/wp-content/uploads/100_Color_names_python.png'
    i = Image(url,width=1200, height=1200)
    display(i)