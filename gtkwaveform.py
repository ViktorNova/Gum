import gtk
import cairo
import gobject

class CairoWidget(gtk.DrawingArea):

    __gsignals__ = {"expose-event": "override"}

    def __init__(self):
        super(CairoWidget, self).__init__()
    
    def do_expose_event(self, event):
        context = self.window.cairo_create()
        context.rectangle(event.area.x, event.area.y,
                          event.area.width, event.area.height)
        context.clip()
        width, height = self.window.get_size()
        self.draw(context, width, height)

    def draw(self, context, width, height):
        """Must be overriden to draw to the cairo context."""
        pass

class Waveform(CairoWidget):

    def __init__(self, graphdata):
        super(Waveform, self).__init__()
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK|gtk.gdk.SCROLL_MASK)
        self.connect("button_press_event", self.button_press)
        self.connect("scroll_event", self.scroll_event)
        self._graphdata = graphdata
        self._graphdata.changed.connect(self.redraw)
        
    def draw(self, context, width, height):
        # black background
        context.set_source_rgb(0, 0, 0)
        context.paint()

        # line at zero
        context.set_line_width(1)
        context.set_source_rgb(0.2, 0.2, 0.2)
        context.move_to(0, round(height / 2) + 0.5)
        context.line_to(width, round(height / 2) + 0.5)
        context.stroke()

        # waveform
        context.set_source_rgb(0, 0.9, 0)
        overview = self._graphdata.get_info(width)
        for i, value in enumerate(overview):
            x = i
            y = round((-value * 0.5 + 0.5) * height)
            #context.rectangle(x, y, 1, 1)
            #context.fill()
            context.move_to(x + 0.5, 0.5 * height + 0.5)
            context.line_to(x + 0.5, y + 0.5)
            context.stroke()

    def redraw(self):
        # queue_draw() emits an expose event. Double buffering is used
        # automatically in the expose event handler.
        self.queue_draw()

    def button_press(self, widget, event):
        print event.button

    def scroll_event(self, widget, event):
        if event.direction == gtk.gdk.SCROLL_UP:
            pass
        elif event.direction == gtk.gdk.SCROLL_DOWN:
            pass

if __name__ == '__main__':
    from mock import Mock, Fake
    

    def test_window():
        window = gtk.Window()
        window.resize(500, 200)
        window.connect("delete-event", gtk.main_quit)
        ctrl = Mock({"get_info": [v / 500. for v in xrange(500)]})
        ctrl.changed = Fake()
        waveform = Waveform(ctrl)
        window.add(waveform)
        window.show_all()
        gtk.main()

    def test_rand():
        window = gtk.Window()
        window.resize(500, 200)
        window.connect("delete-event", gtk.main_quit)

        from random import random
        values = [(random() - 0.5) * 2 for i in xrange(500)]        
        ctrl = Mock({"get_info": values})
        ctrl.changed = Fake()
        waveform = Waveform(ctrl)
        window.add(waveform)
        window.show_all()
        gtk.main()

    def test_sine():
        window = gtk.Window()
        window.resize(500, 200)
        window.connect("delete-event", gtk.main_quit)

        from math import sin
        sine = [sin(2 * 3.14 * 0.01 * x) for x in xrange(500)]
        ctrl = Mock({"get_info": sine})
        ctrl.changed = Fake()
        waveform = Waveform(ctrl)
        window.add(waveform)
        window.show_all()
        gtk.main()

    

    test_window()
    test_rand()
    test_sine()
