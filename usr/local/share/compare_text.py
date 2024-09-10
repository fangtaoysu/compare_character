import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import subprocess

class TextCompareApp(Gtk.Window):

    def __init__(self):
        super().__init__(title="Text Comparison Tool")
        self.set_default_size(1000, 600)

        # Main layout with horizontal box for inputs and control area in the center
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.add(hbox)

        # Left Input Section
        self.left_input_area = self.create_input_area("Left Input")
        hbox.pack_start(self.left_input_area, True, True, 0)

        # Center Controls
        self.controls = self.create_control_area()
        hbox.pack_start(self.controls, False, False, 0)

        # Right Input Section
        self.right_input_area = self.create_input_area("Right Input")
        hbox.pack_start(self.right_input_area, True, True, 0)

        self.mode = 'text'  # Start in text mode

    def create_input_area(self, label_text):
        """Create an input area with a text view, scrollbar, and clear button."""
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        label = Gtk.Label(label=label_text)
        vbox.pack_start(label, False, False, 0)

        # Scrolled window containing the text view
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        text_view = Gtk.TextView()
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        text_view.set_editable(True)  # Initially editable in text mode
        scrolled_window.add(text_view)
        vbox.pack_start(scrolled_window, True, True, 0)

        # Set drag-and-drop support for files
        text_view.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        text_view.connect("drag-data-received", self.on_drag_data_received)

        # Clear Button
        clear_button = Gtk.Button(label="Clear")
        clear_button.connect("clicked", lambda btn: text_view.get_buffer().set_text(""))
        vbox.pack_start(clear_button, False, False, 0)

        # File Select Button (visible only in file mode)
        select_file_button = Gtk.Button(label="Select File")
        select_file_button.connect("clicked", lambda btn: self.select_file_for_text_view(text_view))
        select_file_button.set_no_show_all(True)  # Hide by default in text mode
        vbox.pack_start(select_file_button, False, False, 0)

        # Add drag-drop support details
        self.set_accept_text_drops(text_view)

        return vbox

    def create_control_area(self):
        """Create the control area with compare and mode buttons."""
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Mode Label to show current mode
        self.mode_label = Gtk.Label(label="Current Mode: Text Mode")
        vbox.pack_start(self.mode_label, False, False, 0)

        # Compare Button
        compare_button = Gtk.Button(label="Compare")
        compare_button.connect("clicked", self.compare_texts)
        vbox.pack_start(compare_button, False, False, 0)

        # Mode Toggle Button
        self.mode_button = Gtk.Button(label="Switch to File Mode")
        self.mode_button.connect("clicked", self.toggle_mode)
        vbox.pack_start(self.mode_button, False, False, 0)

        return vbox

    def toggle_mode(self, button):
        """Toggle between text input mode and file mode."""
        if self.mode == 'text':
            self.mode = 'file'
            self.mode_button.set_label("Switch to Text Mode")
            self.mode_label.set_text("Current Mode: File Mode")
            self.set_file_mode(True)
        else:
            self.mode = 'text'
            self.mode_button.set_label("Switch to File Mode")
            self.mode_label.set_text("Current Mode: Text Mode")
            self.set_file_mode(False)

    def set_file_mode(self, is_file_mode): 
        """Enable or disable file mode for input areas."""
        for area in [self.left_input_area, self.right_input_area]:
            scrolled_window = area.get_children()[1]  # ScrolledWindow
            text_view = scrolled_window.get_child()  # TextView
            select_file_button = area.get_children()[3]  # File Select Button

            text_view.set_editable(not is_file_mode)
            select_file_button.set_visible(is_file_mode)

            if is_file_mode:
                text_view.get_buffer().set_text("Click to select a file...")  # Placeholder text
                text_view.connect("button-press-event", lambda w, e: self.select_file_for_text_view(text_view))

    def compare_texts(self, button):
        """Compare texts based on the current mode."""
        left_buffer = self.get_buffer_text(self.left_input_area)
        right_buffer = self.get_buffer_text(self.right_input_area)

        if self.mode == 'text' and left_buffer and right_buffer:
            self.run_compare(['/home/fangtao/compare-character/usr/local/bin/compare'], input_data=f"{left_buffer}\n{right_buffer}")
        elif self.mode == 'file':
            left_file = self.get_buffer_text(self.left_input_area)
            right_file = self.get_buffer_text(self.right_input_area)
            if left_file and right_file and left_file != "Click to select a file..." and right_file != "Click to select a file...":
                self.run_compare(['/home/fangtao/compare-character/usr/local/bin/compare', left_file, right_file])

    def run_compare(self, command, input_data=None):
        """Run the compare executable with given command and input."""
        try:
            if input_data:
                result = subprocess.run(
                    command,
                    input=input_data,
                    capture_output=True,
                    text=True,
                    check=True
                )
            else:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=True
                )

            # Display results and apply highlighting
            self.display_results(result.stdout)
        except subprocess.CalledProcessError as e:
            self.show_error(f"Subprocess error: {e}\n{e.stderr}")
        except Exception as e:
            self.show_error(f"Failed to run compare: {e}")

    def get_buffer_text(self, input_area):
        """Retrieve text from the input area's text view."""
        text_view = input_area.get_children()[1].get_child()  # Get the TextView inside ScrolledWindow
        buffer = text_view.get_buffer()
        start, end = buffer.get_bounds()
        return buffer.get_text(start, end, True).strip()

    def display_results(self, results):
        """Display comparison results with highlighting."""
        lines = results.split('\n')

        # Highlight logic based on the lines returned from the compare tool
        self.apply_highlighting(self.left_input_area, lines, "left")
        self.apply_highlighting(self.right_input_area, lines, "right")

    def apply_highlighting(self, input_area, lines, side):
        """Apply text highlighting based on comparison results."""
        text_view = input_area.get_children()[1].get_child()
        buffer = text_view.get_buffer()
        buffer.set_text("\n".join(lines))
        missing_line_tag = buffer.create_tag("missing_line", background="lightcoral")
        added_line_tag = buffer.create_tag("added_line", background="lightgreen")
        missing_word_tag = buffer.create_tag("missing_word", background="red")
        added_word_tag = buffer.create_tag("added_word", background="green")

        start_iter = buffer.get_start_iter()
        for line in lines:
            # Custom logic for highlighting missing/added lines and words
            if "missing line" in line:
                buffer.apply_tag(missing_line_tag, start_iter, start_iter.copy().forward_line())
            elif "added line" in line:
                buffer.apply_tag(added_line_tag, start_iter, start_iter.copy().forward_line())
            elif "missing word" in line:
                buffer.apply_tag(missing_word_tag, start_iter, start_iter.copy().forward_word_end())
            elif "added word" in line:
                buffer.apply_tag(added_word_tag, start_iter, start_iter.copy().forward_word_end())
            start_iter.forward_line()

    def select_file_dialog(self, title):
        """Open file dialog to select a file."""
        dialog = Gtk.FileChooserDialog(
            title, self, Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )
        response = dialog.run()
        file_path = dialog.get_filename() if response == Gtk.ResponseType.OK else None
        dialog.destroy()
        return file_path

    def select_file_for_text_view(self, text_view):
        """Select a file and set its path in the TextView."""
        file_path = self.select_file_dialog("Select File")
        if file_path:
            text_view.get_buffer().set_text(file_path)

    def on_drag_data_received(self, widget, context, x, y, data, info, time):
        """Handle drag-and-drop data received event."""
        if data.get_length() > 0:
            file_path = data.get_uris()[0].replace('file://', '')
            self.update_text_view_with_file(widget, file_path)

    def update_text_view_with_file(self, text_view, file_path):
        """Update TextView with contents of the dragged file."""
        try:
            with open(file_path, 'r') as file:
                text = file.read()
                text_view.get_buffer().set_text(text)
        except Exception as e:
            self.show_error(f"Failed to read file: {e}")

    def show_error(self, message):
        """Show an error message dialog."""
        dialog = Gtk.MessageDialog(
            self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Error"
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def set_accept_text_drops(self, text_view):
        """Enable drag-and-drop text functionality for TextView."""
        text_view.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        text_view.connect("drag-data-received", self.on_drag_data_received)

if __name__ == "__main__":
    win = TextCompareApp()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()