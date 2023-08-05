import os
from pkg_resources import resource_filename

import kivy
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Scale
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from kivy.metrics import sp
from kivy.uix.image import Image, AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior, FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty
from kivy.config import Config
from kivy.utils import get_color_from_hex

# make sure we are on updated version of kivy
kivy.require('1.10.0')

normalfont = resource_filename(
        __name__,
        os.path.join('resources/fonts', 'DejaVuSans.ttf'))
boldfont = resource_filename(
        __name__,
        os.path.join('resources/fonts', 'DejaVuSans-Bold.ttf'))
fontawesomefont = resource_filename(
        __name__,
        os.path.join('resources/fonts', 'FontAwesome.ttf'))
buttonnormal = resource_filename(
        __name__,
        os.path.join('resources/images', 'button-normal.png'))
buttondown = resource_filename(
        __name__,
        os.path.join('resources/images', 'button-down.png'))
clearimage = resource_filename(
        __name__,
        os.path.join('resources/images', 'clear.png'))
backdrop = resource_filename(
        __name__,
        os.path.join('resources/images', 'backdrop.png'))
listbackdrop = resource_filename(
        __name__,
        os.path.join('resources/images', 'list-backdrop.png'))
trackslidercursor = resource_filename(
        __name__,
        os.path.join('resources/images', 'track-slider-cursor.png'))
ratingstars = [
        u"\uf006\uf006\uf006\uf006\uf006",
        u"\uf123\uf006\uf006\uf006\uf006",
        u"\uf005\uf006\uf006\uf006\uf006",
        u"\uf005\uf123\uf006\uf006\uf006",
        u"\uf005\uf005\uf006\uf006\uf006",
        u"\uf005\uf005\uf123\uf006\uf006",
        u"\uf005\uf005\uf005\uf006\uf006",
        u"\uf005\uf005\uf005\uf123\uf006",
        u"\uf005\uf005\uf005\uf005\uf006",
        u"\uf005\uf005\uf005\uf005\uf123",
        u"\uf005\uf005\uf005\uf005\uf005",
        u"\uf29c"]


class BaseLabel(Label):
    """Base label class to ensure consistency."""
    pass


class OutlineLabel(BaseLabel):
    """Label with an outline."""

    def __init__(self, *args, **kwargs):
        a = App.get_running_app()
        otype = int(a.config.get('colors','outlinetype'))
        w = int(a.config.get('colors','outlinewidth'))
        if otype == 1:
            self.outline_width = sp(w)
            (c1,c2,c3,c4) = get_color_from_hex(
                    a.config.get('colors','textoutline'))
            self.outline_color = (c1,c2,c3)
        elif otype == 2:
            self.bind(texture_size=self.draw_outline)
        super(OutlineLabel, self).__init__(*args, **kwargs)

    def draw_outline(self, *args, **kwargs):
        a = App.get_running_app()
        (c1,c2,c3,c4) = get_color_from_hex(
                a.config.get('colors','textoutline'))
        w = int(a.config.get('colors','outlinewidth'))
        x = int(self.center_x - self.texture_size[0] / 2.0)
        y = int(self.center_y - self.texture_size[1] / 2.0)
        # texture = Texture.create(size=self.texture_size,colorfmt='rgba')
        # widget = Widget()
        with self.canvas.before:
            for lw in range(w,0,-1):
                nw = self.texture_size[0] + lw*2
                nh = self.texture_size[1] + lw*2
                sw = nw / self.texture_size[0]
                sh = nh / self.texture_size[1]
                alpha = (1.0 / w) * (w-lw+1)
                Color(c1,c2,c3,alpha)
                Rectangle(pos=[x,y],size=self.texture_size,
                        texture=self.texture)
                PushMatrix()
                Scale(origin=(self.center_x,self.center_y),
                        x=sw, y=sh)
                PopMatrix()
        # reset the color, otherwise the next widget will be tinted
        Color(1.,1.,1.)
        # self.unbind(texture_size=self.draw_outline)
        # self.texture=widget.texture
        # self.bind(texture_size=self.draw_outline)


class ShadowLabel(BaseLabel):
    """Label with a drop shadow."""

    def __init__(self, *args, **kwargs):
        super(ShadowLabel, self).__init__(*args, **kwargs)
        # this was the only way i could get it to draw the correct size (?)
        self.bind(texture_size=self.draw_shadow)

    def draw_shadow(self, *args, **kwargs):
        a = App.get_running_app()
        o = int(a.config.get('colors','textshadowsize'))
        (c1,c2,c3,c4) = get_color_from_hex(a.config.get('colors','textshadow'))
        x = int(self.center_x - self.texture_size[0] / 2.0)
        y = int(self.center_y - self.texture_size[1] / 2.0)
        with self.canvas.before:
            # check if the texture is actually on the screen (?)
            if x > 0 and y > 0:
                for i in range(o):
                    alpha = (1.0 / (o+1)) * (o-i)
                    # Logger.debug("ShadowLabel: text "+self.text+" color "+format((c1,c2,c3,alpha))+" pos "+format([x+sp(i+1),y-sp(i-1)])+" size "+format(self.texture_size)+" texture "+format(self.texture))
                    Color(c1,c2,c3,alpha)
                    Rectangle(pos=[x+sp(i+1),y-sp(i+1)],
                            size=self.texture_size, texture=self.texture)
            # reset the color, otherwise the next widget will be tinted
            Color(1.,1.,1.)


class ScaledWidthLabel(BaseLabel):
    """Helps avoid a divide by zero exception when texture_size[0] = 0 (?)"""
    _internalscale = NumericProperty(None)
    _scale = NumericProperty(1.0)

    def __init__(self, *args, **kwargs):
        super(ScaledWidthLabel, self).__init__(*args, **kwargs)
        if len(self.text) < 50:
            self.font_size = '40sp'
        else:
            self.font_size = '20sp'
        self.do_resize()

    def do_resize(self):
        if self.texture_size[0] > 0 and self.texture_size[0] < self.width:
            self._internalscale = float(self.width) / self.texture_size[0]
        else:
            self._internalscale = 1.0

    def on_texture_size(self, obj, value):
        self.do_resize()


class ExtraSlider(Slider):
    """Class that implements some extra stuff on top of a standard slider."""

    def __init__(self, **kwargs):
        """Do normal init routine, but also register on_release event."""
        super(self.__class__, self).__init__(**kwargs)
        self.register_event_type('on_release')

    def on_release(self):
        """Override this with something you want this slider to do."""
        pass

    def on_touch_up(self, touch):
        """Check if slider is released, dispatch the on_release event if so."""
        released = super(self.__class__, self).on_touch_up(touch)
        if released:
            self.dispatch('on_release')
        return released


class CoverButton(Button):
    """Album cover that is pressable."""

    img = ObjectProperty(None)
    layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.background_normal = clearimage
        self.background_down = clearimage
        self.font_name = boldfont
        with self.canvas.before:
            Rectangle(texture=self.img.texture,
                      pos=self.layout.pos,
                      size=self.layout.size)


class ArtistRecycleBoxLayout(
        FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class ArtistRow(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(ArtistRow, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(ArtistRow, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            App.get_running_app().root.selected_row = index


class RatingPopup(Popup):
    rating_set = ObjectProperty(None)
    song = StringProperty(None)
    index = NumericProperty(None)
    robject = ObjectProperty(None)


class ScreenSwitcher(BoxLayout):
    manager = ObjectProperty(None)
    currentscreen = StringProperty('nowplaying')

