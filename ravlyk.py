import sys

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    print("GTK Not Availible")


class Ravlyk:
    wTree = None

    def __init__( self ):
        filename = "main_window.glade"
        builder = gtk.Builder()
        builder.add_from_file(filename)
        builder.connect_signals(self)

        window = builder.get_object('window_main')
        window.set_title('Ravlyk')
        window.set_size_request(1000, 500)
        window.show_all()

        gtk.main()

    def quit(self, widget):
        sys.exit(0)


if __name__ == "__main__":
    Ravlyk()
