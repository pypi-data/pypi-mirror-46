# coding: utf8
from __future__ import division
import os, time, numbers, math, io, warnings, sys
import pygame
import requests
import cache
from .utils import cached_property, get_resource

# colors from http://clrs.cc/
color_map = {
    'aqua': (127, 219, 255),
    'blue': (0, 116, 217),
    'navy': (0, 31, 63),
    'teal': (57, 204, 204),
    'green': (46, 204, 64),
    'olive': (61, 153, 112),
    'lime': (1, 255, 112),
    'yellow': (255, 220, 0),
    'orange': (255, 133, 27),
    'red': (255, 65, 54),
    'fuchsia': (240, 18, 190),
    'purple': (177, 13, 201),
    'maroon': (133, 20, 75),
    'white': (255, 255, 255),
    'silver': (221, 221, 221),
    'gray': (170, 170, 170),
    'grey': (170, 170, 170),
    'black': (0, 0, 0),
}

broken_image_file = get_resource('broken_image.png')

def _xy_add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def _xy_subtract(t1, t2):
    return (t1[0] - t2[0], t1[1] - t2[1])

def _xy_multiply(t1, t2):
    return (t1[0] * t2[0], t1[1] * t2[1])

def _xy_magnitude(t):
    return math.hypot(t[0], t[1])

def _xy_normalize(t):
    '''
    Returns a vector in the same direction but with length 1
    '''
    mag = float(_xy_magnitude(t))
    return (t[0]/mag, t[1]/mag)

def _xy_rotate_90_degrees(t):
    '''
    Returns a rotated vector 90 degrees in the anti-clockwise direction
    '''
    return (-t[1], t[0])

def _color(identifier_or_tuple):
    try:
        return color_map[identifier_or_tuple]
    except KeyError:
        return identifier_or_tuple

def _scale(scale):
    """ Given a numeric input, return a 2-tuple with the number repeated.
        Given a 2-tuple input, return the input

    >>> _scale(2)
    (2, 2)
    >>> _scale((1, 2,))
    (1, 2)
    >>> _scale('nonsense')
    Traceback (most recent call last):
        ...
    TypeError: argument should be a number or a tuple
    >>> _scale((1,2,3))
    Traceback (most recent call last):
        ...
    ValueError: scale should be a 2-tuple
    """
    if isinstance(scale, tuple):
        if len(scale) != 2:
            raise ValueError('scale should be a 2-tuple')
        return scale
    elif isinstance(scale, numbers.Real):
        return (scale, scale)
    else:
        raise TypeError('argument should be a number or a tuple')

def _font(font, font_size, antialias):
    pygame.font.init()
    if font is None:
        font = get_resource('Geneva.ttf')
        if antialias is None:
            antialias = (font_size < 9 or 17 < font_size)

    if antialias is None:
        antialias = True

    return pygame.font.Font(font, font_size), antialias

def _anchor(align):
    mapping = {
        'topleft': (0, 0),
        'left': (0, 0.5),
        'bottomleft': (0, 1),
        'top': (0.5, 0),
        'center': (0.5, 0.5),
        'bottom': (0.5, 1),
        'topright': (1, 0),
        'right': (1, 0.5),
        'bottomright': (1, 1),
    }

    return mapping[align]

def _xy_from_align(align, surface_size):
    return _xy_multiply(surface_size, _anchor(align))

def _topleft_from_aligned_xy(xy, align, size, surface_size):
    if xy is None:
        xy = _xy_from_align(align, surface_size)

    anchor_offset = _xy_multiply(_anchor(align), size)
    return _xy_subtract(xy, anchor_offset)

image_cache = cache.ImageCache()

class Surface(object):
    """
    The base class for the :py:class:`Screen` and :py:class:`Image` classes, and the
    :py:data:`screen` object.
    """
    def __init__(self, surface=None):
        if surface is None:
            if not hasattr(self, '_create_surface'):
                raise TypeError('surface must not be nil')
        else:
            self.surface = surface

    @cached_property
    def surface(self):
        # this function is only called once if a surface is not set in the constructor
        surface = self._create_surface()

        if not surface:
            raise TypeError('_create_surface should return a pygame Surface')

        return surface

    @property
    def size(self):
        """The size of the surface in pixels as a tuple (width, height)"""
        return self.surface.get_size()

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    def _fill(self, color, rect=None):
        if len(color) <= 3:
            self.surface.fill(color, rect)
        elif len(color) >= 4:
            tmp_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            tmp_surface.fill(color)
            self.surface.blit(tmp_surface, rect)

    def fill(self, color):
        """
        Fills the entire surface with a solid color
        """
        self._fill(_color(color), self.surface.get_rect())

    def text(self, string, xy=None, color='grey', align='center', font=None, font_size=32, 
             antialias=None, max_width=sys.maxsize, max_height=sys.maxsize, max_lines=sys.maxsize):
        """
        Draws text to the surface.

        Args:
            string: The text to draw.
            xy (tuple): The position (x, y) to draw the text, as measured from the top-left.
            color (tuple or str): The color (r, g, b) or color name.
            align (str): How to align the text relative to `xy`, or relative to the drawing surface
                if `xy` is None. Defaults to 'center'.
            font (str): The filename of the font to use.
            font_size (int): The size to render the font.
            antialias (bool): Set to false to draw pixel fonts.
            max_width (int): The maximum width of the text in pixels.
                If `xy` is not specified, defaults to the width of the drawing surface. Otherwise,
                defaults to unlimited.
            max_height (int): The maximum height of the text in pixels.
                If `xy` is not specified, defaults to the width of the drawing surface. Otherwise,
                defaults to unlimited.
            max_lines (int): The maximum number of lines to use. Set to 1 to draw a single line
                of text. By default, unlimited.
        """
        if xy is None:
            if max_width == sys.maxsize:
                max_width = self.width
            if max_height == sys.maxsize:
                max_height = self.height

        text_image = Image.from_text(
            string,
            color=color,
            font=font,
            font_size=font_size,
            antialias=antialias,
            max_lines=max_lines,
            max_width=max_width,
            max_height=max_height,
            align=_anchor(align)[0])

        self.image(text_image, xy=xy, align=align, scale=1)

    def oval(self, xy=None, size=(150,100), color='grey', align='center'):
        """
        Draws an oval.
        
        Args:
            xy (tuple): The position (x, y) to draw the oval, as measured from the top-left.
            size (tuple): The size (width, height) of the oval.
            color (tuple or str): The color (r, g, b) or color name.
            align (str): How to align the outside box of the oval relative to `xy`, or relative to the drawing surface
                if `xy` is None. Defaults to 'center'.
        """
        if xy is not None:
            if not (hasattr(xy, '__len__')
                    and len(xy) >= 2
                    and isinstance(xy[0], numbers.Real)
                    and isinstance(xy[1], numbers.Real)):
                raise TypeError('xy should contain two numbers')
        
        if not (hasattr(size, '__len__')
                and len(size) >= 2
                and isinstance(size[0], numbers.Real)
                and isinstance(size[1], numbers.Real)):
            raise TypeError('size should contain two numbers - (width, height)')

        xy = _topleft_from_aligned_xy(xy, align, size, self.size)
        color = _color(color)
        rect = pygame.Rect(xy, size)

        if len(color) == 4 and color[3] < 255:
            # need to draw to a second buffer then blit to have transparency
            draw_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            pygame.draw.ellipse(draw_surface, color, pygame.Rect((0, 0), rect.size), 0)
            self.surface.blit(draw_surface, rect)
        else:
            pygame.draw.ellipse(self.surface, color, rect, 0)

    def circle(self, xy=None, size=100, color='grey', align='center'):
        """
        Draws a circle.

        Args:
            xy (tuple): The position (x, y) to draw the circle, as measured from the top-left.
            size (int): The diameter of the circle.
            color (tuple or str): The color (r, g, b) or color name.
            align (str): How to align the outside box of the circle relative to `xy`, or relative to the drawing surface
                if `xy` is None. Defaults to 'center'.
        """
        if isinstance(size, numbers.Real):
            size = (size, size)
        elif hasattr(size, '__len__') and len(size) == 2:
            pass
        else:
            raise TypeError('size should be a number or a 2-tuple')

        self.oval(xy=xy, size=size, color=color, align=align)

    def rectangle(self, xy=None, size=(100, 100), color='grey', align='center'):
        """
        Draws a rectangle.

        Args:
            xy (tuple): The position (x, y) to draw the rectangle, as measured from the top-left.
            size (tuple): The size (width, height) of the rectangle.
            color (tuple or str): The color (r, g, b) or color name.
            align (str): How to align the box relative to `xy`, or relative to the drawing surface
                if `xy` is None. Defaults to 'center'.
        """
        if len(size) != 2:
            raise ValueError('size should be a 2-tuple')

        xy = _topleft_from_aligned_xy(xy, align, size, self.size)

        self._fill(_color(color), pygame.Rect(xy, size))

    def line(self, start_xy, end_xy, width=1, color='grey', antialias=True):
        """
        Draws a line between two points.

        Args:
            start_xy (tuple): The position (x, y) of the start of the line.
            end_xy (tuple):  The position (x, y) of the end of the line.
            width (int): The thickness of the line in pixels. Defaults to 1.
            color (tuple or str): The color (r, g, b) or color name.
        """
        if start_xy == end_xy:
            return

        # antialiased thick lines aren't supported by pygame, and the aaline function has some
        # strange bugs on OS X (line comes out the wrong colors, see
        # http://stackoverflow.com/q/24208783/382749) so antialiasing isn't currently supported.

        if width == 1:
            pygame.draw.line(self.surface, _color(color), start_xy, end_xy, width)
        else:
            # we use a polygon to draw thick lines because the pygame line function has a very
            # strange line cap

            delta = _xy_subtract(end_xy, start_xy)
            delta_rotated = _xy_rotate_90_degrees(delta)

            # this is a hack to draw line the correct size - pygame.draw.polygon seems to outline
            # the polygons it draws as well as fill them, making the lines too thick.
            width -= 1

            perpendicular_offset = _xy_multiply(_xy_normalize(delta_rotated), _scale(width*0.5))

            points = (
                _xy_add(start_xy, perpendicular_offset),
                _xy_add(end_xy, perpendicular_offset),
                _xy_subtract(end_xy, perpendicular_offset),
                _xy_subtract(start_xy, perpendicular_offset),
            )

            pygame.draw.polygon(self.surface, _color(color), points)

    def image(self, image, xy=None, scale='shrinkToFit', alpha=1.0, align='center',
              max_width=sys.maxsize, max_height=sys.maxsize, raise_error=True):
        """screen.image(image, xy=None, scale='shrinkToFit', alpha=1.0, align='center', max_width=sys.maxsize, max_height=sys.maxsize, raise_error=True)

        Draws an image to the screen.

        Args:
            image (str or Image): A filename, URL or `Image` object to draw. If `image` is
                a URL, then it will attempt to download and display it.
            xy (tuple): The position (x, y) to draw the text, as measured from the top-left.
            scale (str or number): a number that changes the size of the image e.g. scale=2
                makes the image bigger, scale=0.5 makes the image smaller. There are also
                special values 'fit' and 'fill', which will fit or fill the image according
                to max_width and max_height. Defaults to 'shrinkToFit', which will fit an image 
                without enlarging.
            alpha (number): The opacity of the image - 0.0 means fully transparent, 1.0 is fully
                opaque.
            max_width (int): When `scale` is 'fit', 'fill', 'shrinkToFit' used to size the image.
            max_height (int): When `scale` is 'fit', 'fill', 'shrinkToFit' used to size the image.
            raise_error (bool): When loading an image from a URL, whether to raise an error if
                loading fails. Defaults to True. If false, a placeholder image will be substituted.

        Images can be animated GIFs. Draw them in a draw() function to see them animate.

        Images referred to by filename or URL are cached, so this can be called in a loop without
        performance concerns.

        Raises:
            requests.exceptions.RequestException: The image couldn't be loaded from URL.
        """

        if isinstance(image, basestring):
            try:
                image = image_cache.get_image(image)
            except IOError:
                if raise_error:
                    raise
                else:
                    image = image_cache.get_image(broken_image_file)

        if hasattr(image, 'surface'):
            image_size = image.size
            surface = image.surface
        else:
            # maybe the caller passed `image` as a pygame surface
            surface = image
            image_size = surface.get_size()

        if scale in ('fit', 'fill', 'shrinkToFit'):
            if max_width == sys.maxsize:
                max_width = self.width
            if max_height == sys.maxsize:
                max_height = self.height

            fit_scale = min(max_width / image_size[0], max_height / image_size[1])
            fill_scale = max(max_width / image_size[0], max_height / image_size[1])

            if scale == 'shrinkToFit':
                if fit_scale < 1:
                    scale = fit_scale
                else:
                    scale = 1
            elif scale == 'fit':
                scale = fit_scale
            elif scale == 'fill':
                scale = fill_scale

        scale = _scale(scale)

        # blit_surface is a temporary variable to minimise copying on each tranformation
        blit_surface = surface

        if scale != (1, 1):
            image_size = _xy_multiply(image_size, scale)
            image_size = tuple(int(d) for d in image_size)
            try:
                blit_surface = pygame.transform.smoothscale(surface, image_size)
            except ValueError:
                blit_surface = pygame.transform.scale(surface, image_size)

        if alpha < 1.0:
            # only copy the surface if required
            if blit_surface is surface:
                blit_surface = surface.copy()

            # multipling the pixels' color components with white does nothing, so this only
            # changes the alpha of the image
            blit_surface.fill((255, 255, 255, alpha*255), None, pygame.BLEND_RGBA_MULT)

        xy = _topleft_from_aligned_xy(xy, align, image_size, self.size)

        self.surface.blit(blit_surface, xy)


class Screen(Surface):
    """
    The class of the singleton :py:data:`screen` object.
    """
    def __init__(self):
        super(Screen, self).__init__()
        self.needs_update = False
        self.has_surface = False
        self._brightness = 75

    def _create_surface(self):
        from . import platform_specific
        surface = platform_specific.create_main_surface()
        self.has_surface = True
        return surface

    def ensure_display_setup(self):
        # setup pygame.display by calling the self.surface getter
        self.surface

    def update(self):
        pygame.display.update()
        self.needs_update = False

    def fill(self, *args, **kwargs):
        super(Screen, self).fill(*args, **kwargs)
        self.needs_update = True

    def text(self, *args, **kwargs):
        super(Screen, self).text(*args, **kwargs)
        self.needs_update = True

    def oval(self, *args, **kwargs):
        super(Screen, self).oval(*args, **kwargs)
        self.needs_update = True

    def circle(self, *args, **kwargs):
        super(Screen, self).circle(*args, **kwargs)
        self.needs_update = True

    def rectangle(self, *args, **kwargs):
        super(Screen, self).rectangle(*args, **kwargs)
        self.needs_update = True

    def line(self, *args, **kwargs):
        super(Screen, self).line(*args, **kwargs)
        self.needs_update = True

    def image(self, *args, **kwargs):
        super(Screen, self).image(*args, **kwargs)
        self.needs_update = True

    def update_if_needed(self):
        if self.needs_update:
            self.update()

    @property
    def brightness(self):
        """
        The brightness of the backlight of the screen, from 0 to 100. 0 is off, 100 is full
        brightness. Defaults to 75.
        """
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        from . import platform_specific

        if brightness < 0:
            brightness = 0
        if brightness > 100:
            brightness = 100

        self._brightness = brightness
        platform_specific.set_backlight(brightness)


screen = Screen()


class Image(Surface):
    """
    An image that can be loaded from a file, or created and drawn to separately from the screen.
    """
    @classmethod
    def load(cls, filename):
        """
        Open a local file as an Image.

        Args:
            filename (str): The filename of the image.
        """
        return cls.load_filename(filename)

    @classmethod
    def load_filename(cls, filename):
        with open(filename, 'rb') as image_file:
            return cls.load_file(image_file, name_hint=filename)

    @classmethod
    def load_url(cls, url):
        """
        Loads an image from a URL.

        Returns:
            An Image or GIFImage object, that can be used with screen.image() for example.

        Raises:
            requests.exceptions.RequestException: The image couldn't be loaded from URL.
        """
        response = requests.get(url)
        response.raise_for_status()
        image_file = io.BytesIO(response.content)
        return cls.load_file(image_file, name_hint=url)

    @classmethod
    def load_file(cls, file_object, name_hint='', loader='auto'):
        """
        Loads a file-like object as an image.

        Args:
            file_object (filelike): an open file-like object
            name_hint (str): the name of the file, used to guess the loader to use
            loader (str): How to load the image, either 'gif', 'pil', 'pygame', or 'auto'.
                If 'gif', a GIFImage will be returned. If 'auto', the name_hint is used to
                choose the best loader.

        Returns:
            An Image or GIFImage object, that can be used with screen.image() for example.
        """

        if loader == 'auto':
            _, extension = os.path.splitext(name_hint)

            if extension.lower() == '.gif':
                # if it's a gif, load it using the special GIFImage class
                loader = 'gif'
            elif extension.lower() in ['.jpg', '.jpeg'] and sys.platform == 'darwin':
                # There's a bug with pygame on Mac, JPEGs are distorted on load.
                # (it's actually a bug in SDL_Image)
                # https://bitbucket.org/pygame/pygame/issues/284/max-osx-el-capitan-using-the-deprecated
                # Working around by loading with PIL instead.
                loader = 'pil'
            else:
                loader = 'pygame'

        if loader == 'gif':
            return GIFImage(image_file=file_object)
        elif loader == 'pil':
            from PIL import Image as PILImage
            return cls.from_pil_image(PILImage.open(file_object))
        elif loader == 'pygame':
            # ensure the screen surface has been created (otherwise pygame doesn't know the 'video mode')
            screen.ensure_display_setup()

            surface = pygame.image.load(file_object)
            surface = surface.convert_alpha()
        else:
            raise ValueError('Unknown image loader: %r' % loader)

        return cls(surface=surface)

    @classmethod
    def from_text(cls, string, color='grey', font=None, font_size=32, antialias=None,
                  max_lines=sys.maxsize, max_width=sys.maxsize, max_height=sys.maxsize, align=0):
        """
        Draws text to the surface.

        Args:
            string: The text to draw.
            color (tuple or str): The color (r, g, b) or color name.
            font (str): The filename of the font to use.
            font_size (int): The size to render the font.
            antialias (bool): Set to `False` to draw pixel fonts.
            max_lines (int): The maximum number of lines to use. Set to 1 to draw a single line
                of text. By default, unlimited.
            max_width (int): The maximum width of the text in pixels.
                Defaults to unlimited.
            max_height (int): The maximum height of the text in pixels.
                Defaults to unlimited.
            align (number): A number specifying the horizontal alignment of the text. 0.0 is left
                aligned, 0.5 is centered, 1.0 is right.
        """

        font, antialias = _font(font, font_size, antialias)
        color = _color(color)
        string = unicode(string)

        from .typesetter import render_text

        if max_height != sys.maxsize:
            line_height = font.get_linesize()
            max_lines_by_height = int(max_height//line_height)

            if max_lines_by_height < 1:
                # never collapse the text to zero lines because of the height restriction
                max_lines_by_height = 1

            max_lines = min(max_lines, max_lines_by_height)

        surface = render_text(string, font, antialias, color, max_lines, max_width, ellipsis=u'…', align=align)

        return cls(surface=surface)

    @classmethod
    def from_pil_image(cls, pil_image):
        """
        Loads an image from a PIL Image.
        """
        screen.ensure_display_setup()

        try:  # account for different versions of Pillow
            pygame_image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)
        except AttributeError:
            pygame_image = pygame.image.fromstring(pil_image.tostring(), pil_image.size, pil_image.mode)

        pygame_image.convert_alpha()

        return cls(surface=pygame_image)

    def __init__(self, surface=None, size=None):
        pygame.init()
        surface = surface or pygame.Surface(size, flags=pygame.SRCALPHA)
        super(Image, self).__init__(surface)

    def get_memory_usage(self):
        return self.surface.get_buffer().length

class GIFImage(Surface):
    def __init__(self, image_file): # image_file can be either a file-like object or filename
        pygame.init()
        from PIL import Image as PILImage
        self.frames = self._get_frames(PILImage.open(image_file))
        self.total_duration = sum(f[1] for f in self.frames)

    def _get_frames(self, pil_image):
        result = []

        pal = pil_image.getpalette()
        base_palette = []
        for i in range(0, len(pal), 3):
            rgb = pal[i:i+3]
            base_palette.append(rgb)

        all_tiles = []
        try:
            while 1:
                if not pil_image.tile:
                    pil_image.seek(0)
                if pil_image.tile:
                    all_tiles.append(pil_image.tile[0][3][0])
                pil_image.seek(pil_image.tell() + 1)
        except EOFError:
            pil_image.seek(0)

        all_tiles = tuple(set(all_tiles))

        while 1:
            try:
                duration = pil_image.info["duration"] * 0.001
            except KeyError:
                duration = 0.1

            if all_tiles:
                if all_tiles in ((6,), (7,)):
                    pal = pil_image.getpalette()
                    palette = []
                    for i in range(0, len(pal), 3):
                        rgb = pal[i:i+3]
                        palette.append(rgb)
                elif all_tiles in ((7, 8), (8, 7)):
                    pal = pil_image.getpalette()
                    palette = []
                    for i in range(0, len(pal), 3):
                        rgb = pal[i:i+3]
                        palette.append(rgb)
                else:
                    palette = base_palette
            else:
                palette = base_palette
            try:  # account for different versions of Pillow
                pygame_image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)
            except AttributeError:
                pygame_image = pygame.image.fromstring(pil_image.tostring(), pil_image.size, pil_image.mode)

            screen.ensure_display_setup()
            pygame_image.set_palette(palette)

            if "transparency" in pil_image.info:
                pygame_image.set_colorkey(pil_image.info["transparency"])

            result.append([pygame_image, duration])
            try:
                pil_image.seek(pil_image.tell() + 1)
            except EOFError:
                break

        return result

    @property
    def surface(self):
        current_time = time.time()

        if not hasattr(self, 'start_time'):
            self.start_time = current_time

        try:
            gif_time = (current_time - self.start_time) % self.total_duration
        except ZeroDivisionError:
            gif_time = 0

        frame_time = 0

        for surface, duration in self.frames:
            frame_time += duration

            if frame_time >= gif_time:
                return surface

    def get_memory_usage(self):
        return sum(x[0].get_buffer().length for x in self.frames)
