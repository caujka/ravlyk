import os
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
    window_main=None

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
        self.window_main.show_all()

        self.left_image = builder.get_object('left_image')
        self.right_image = builder.get_object('right_image')

        self.image_list = builder.get_object('treeview_images')
        self.image_list.set_size_request(1, 0)

        column = gtk.TreeViewColumn('Files')
        self.image_list.append_column(column)

        self.file_list_model = gtk.ListStore(str)
        self.image_list.set_model(self.file_list_model)
        cell = gtk.CellRendererText()
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', 0)

        self.window_main.show_all()

    def load_images(self, data):
        img_load_dialog = gtk.FileChooserDialog (title="Load images",
            parent=self.window_main,
            action=gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        img_load_dialog.set_select_multiple(True)

        response = img_load_dialog.run()

        if response == gtk.RESPONSE_OK:
            files = img_load_dialog.get_filenames()

            def select_image(selection, model, items, is_selected):
                if is_selected:
                    self.display_image(self.images[items[0]])
                return True

            for filepath in sorted(files):
                image = RavlykImage(filepath)
                self.images.append(image)
                self.file_list_model.append([image.filename])

                self.image_list.get_selection().set_select_function(select_image, full=True)

            for file in files:
                print ('%s selected' % (file,))
        elif response == gtk.RESPONSE_CANCEL:
            print ('Closed, no files selected')

        img_load_dialog.destroy()

    def display_image(self, image):
        pixbuf = gtk.gdk.pixbuf_new_from_file(image.path)
        self.left_image.window.draw_pixbuf(self.left_image.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0, 0)


if __name__ == "__main__":
    Ravlyk()
    gtk.main()

