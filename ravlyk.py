from math import trunc
from image import RavlykImage

try:
    import pygtk

    pygtk.require("2.0")
except:
    pass
try:
    import gtk
except:
    print("GTK Not Availible")


class Ravlyk:
    wTree = None
    window_main = None
    selected_left = None
    selected_right = None

    def __init__( self ):
        self.images = []
        self.show_window()

    def show_window(self):
        builder = gtk.Builder()
        builder.add_from_file("main_window.glade")
        builder.connect_signals(self)

        self.window_main = builder.get_object('window_main')
        self.window_main.set_title('Ravlyk')
        self.window_main.set_size_request(1000, 500)
        self.window_main.connect("destroy", lambda w: gtk.main_quit())
        self.window_main.show_all()

        self.left_image = builder.get_object('left_image')
        self.right_image = builder.get_object('right_image')
        self.left_image.connect("expose-event", self.refresh_image)
        self.right_image.connect("expose-event", self.refresh_image)

        def select_poi(widget, event):
            self.selected_left.add_poi(int(event.x), int(event.y))
            self.draw_poi(self.left_image, int(event.x), int(event.y))

        self.left_scrollwindow = builder.get_object('scrolledwindow1')
        self.left_scrollwindow.connect('button-press-event', select_poi)

        self.right_image = builder.get_object('right_image')

        self.image_list = builder.get_object('treeview_images')
        self.image_list.set_size_request(1, 0)

        column = gtk.TreeViewColumn('Files')
        self.image_list.append_column(column)

        def select_image(selection, model, items, is_selected):
            if not is_selected:
                self.selected_left = self.images[items[0]]
                self.display_image(self.selected_left)
            return True

        self.image_list.get_selection().set_select_function(select_image, full=True)

        self.file_list_model = gtk.ListStore(str)
        self.image_list.set_model(self.file_list_model)
        cell = gtk.CellRendererText()
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', 0)

        self.window_main.show_all()

    def draw_poi(self, drawable, x, y):
        gc = drawable.window.new_gc(foreground=gtk.gdk.Color('#ff0000'), background=None, font=None,
            function=-1, fill=-1, tile=None,
            stipple=None, clip_mask=None, subwindow_mode=-1,
            ts_x_origin=-1, ts_y_origin=-1, clip_x_origin=-1,
            clip_y_origin=-1, graphics_exposures=-1,
            line_width=2, line_style=-1, cap_style=-1, join_style=-1)

        offset_x, offset_y = trunc(self.left_scrollwindow.get_hadjustment().value), \
                             trunc(self.left_scrollwindow.get_vadjustment().value)
        drawable.window.draw_rectangle(gc, False, x + offset_x - 5, y + offset_y - 5, 10, 10)
        #        self.pangolayout.set_text("Rectangle")
        #        drawable.window.draw_layout(gc, x+5, y+80, self.pangolayout)
        return

    def load_images(self, data):
        img_load_dialog = gtk.FileChooserDialog(title="Load images",
            parent=self.window_main,
            action=gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        img_load_dialog.set_select_multiple(True)

        response = img_load_dialog.run()

        if response == gtk.RESPONSE_OK:
            files = img_load_dialog.get_filenames()

            for filepath in sorted(files):
                image = RavlykImage(filepath)
                self.images.append(image)
                self.file_list_model.append([image.filename])

        elif response == gtk.RESPONSE_CANCEL:
            print ('Closed, no files selected')

        img_load_dialog.destroy()

    def display_image(self, image):
        pixbuf = gtk.gdk.pixbuf_new_from_file(image.path)
        self.left_image.window.draw_pixbuf(self.left_image.style.bg_gc[gtk.STATE_NORMAL],
            pixbuf, 0, 0, 0, 0, width=image.size[0], height=image.size[1])
        self.left_image.set_size_request(*image.size)

    def refresh_image(self, widget, event):
        i=self.selected_left
        if i:
            pixbuf = gtk.gdk.pixbuf_new_from_file(i.path)
            widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0, 0)

            for p in i.poi:
                if p:
                    self.draw_poi(self.left_image, p[0], p[1])


if __name__ == "__main__":
    Ravlyk()
    gtk.main()

