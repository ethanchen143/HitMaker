import wx
from app import generate
from app import play
from app import stop
import threading
import sys
import os
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

background_path = os.path.join(application_path, 'background.png')
class Hitmaker(wx.Frame):
    def __init__(self, *args, **kw):
        super(Hitmaker, self).__init__(*args, **kw)
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.WHITE)

        background_image = wx.Image(background_path, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        bmp = wx.StaticBitmap(self.panel, -1, background_image, (0, 0))

        font = wx.Font(32, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)
        font2 = wx.Font(20, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_MAX, wx.FONTWEIGHT_BOLD)
        # Create the header title and apply font
        self.header_title = wx.StaticText(self.panel, label="HitMaker", style=wx.ALIGN_CENTER)
        self.header_title.SetFont(font)

        # Create sliders for energy and mood
        self.energy_label = wx.StaticText(self.panel, label="Energy", style=wx.ALIGN_CENTER)
        self.energy_label.SetFont(font2)
        self.energy_slider = wx.Slider(self.panel, value=50, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL)
        self.mood_label = wx.StaticText(self.panel, label="Mood", style=wx.ALIGN_CENTER)
        self.mood_label.SetFont(font2)
        self.mood_slider = wx.Slider(self.panel, value=50, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL)

        font3 = wx.Font(16, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_MAX, wx.FONTWEIGHT_NORMAL)
        # Create buttons
        self.help_button = wx.Button(self.panel, label="Help")
        self.location_button = wx.Button(self.panel, label="Location")
        self.generate_button = wx.Button(self.panel, label="Generate")
        self.play_button = wx.Button(self.panel, label="Play")
        self.stop_button = wx.Button(self.panel, label="Stop")
        self.help_button.SetFont(font3)
        self.location_button.SetFont(font3)
        self.generate_button.SetFont(font3)
        self.play_button.SetFont(font3)
        self.stop_button.SetFont(font3)

        # Create a TextCtrl to display the chord progression
        self.chord_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.song_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Bind event handlers for buttons
        self.help_button.Bind(wx.EVT_BUTTON,self.on_help_button)
        self.location_button.Bind(wx.EVT_BUTTON, self.on_location_button)
        self.generate_button.Bind(wx.EVT_BUTTON, self.on_generate_button)
        self.play_button.Bind(wx.EVT_BUTTON,self.on_play_button)
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop_button)

        # Use a BoxSizer to divide the window into two halves
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Left half containing the energy label and slider
        left_half_sizer = wx.BoxSizer(wx.VERTICAL)
        left_half_sizer.Add(self.energy_label, 0, wx.ALL | wx.CENTER, 10)
        left_half_sizer.Add(self.energy_slider, 0, wx.ALL | wx.EXPAND, 10)
        # Right half containing the mood label and slider
        right_half_sizer = wx.BoxSizer(wx.VERTICAL)
        right_half_sizer.Add(self.mood_label, 0, wx.ALL | wx.CENTER, 10)
        right_half_sizer.Add(self.mood_slider, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(left_half_sizer, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(right_half_sizer, 1, wx.EXPAND | wx.ALL, 10)

        helper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        helper_sizer.Add(self.help_button, 0, wx.ALL, 10)

        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        header_sizer.AddStretchSpacer(1)
        header_sizer.Add(self.header_title, 0, wx.ALL | wx.CENTER, 10)
        header_sizer.AddStretchSpacer(1)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.AddStretchSpacer(1)
        button_sizer.Add(self.location_button, 0, wx.ALL, 10)
        button_sizer.Add(self.generate_button, 0, wx.ALL, 10)
        button_sizer.Add(self.play_button, 0, wx.ALL, 10)
        button_sizer.Add(self.stop_button, 0, wx.ALL, 10)
        button_sizer.AddStretchSpacer(1)

        info_sizer = wx.BoxSizer(wx.VERTICAL)
        info_sizer.Add(self.chord_text, 0, wx.EXPAND | wx.ALL, 10)
        info_sizer.Add(self.song_text, 0, wx.EXPAND | wx.ALL, 10)

        # Vertical BoxSizer for the entire layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(helper_sizer, 0, wx.EXPAND)
        main_sizer.Add(header_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(sizer, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(info_sizer, 1, wx.EXPAND | wx.ALL, 10)

        self.panel.SetSizer(main_sizer)
        self.midi_location = "./sample_midis"
        self.song_info = None

    def on_location_button(self, event):
        # Trigger file dialog to select folder location
        dlg = wx.DirDialog(self, "Select Folder Location", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.midi_location = dlg.GetPath()
            print("Selected MIDI Location:", self.midi_location)
        dlg.Destroy()

    def on_generate_button(self, event):
        if not self.midi_location:
            wx.MessageBox("Please select MIDI location first.", "Error", wx.OK | wx.ICON_ERROR)
            return
        energy_value = self.energy_slider.GetValue()
        mood_value = self.mood_slider.GetValue()
        self.song_info = generate(energy_value/100, mood_value/100,self.midi_location)
        # Display the song information
        # Create a font for chord progressions
        font4 = wx.Font(16, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_MAX, wx.FONTWEIGHT_MEDIUM)
        self.chord_text.SetValue(self.song_info["chord_progression"].__str__()
                                 .replace('[','').replace(',','').replace(']','')
                                 .replace("'","").replace('"','').replace(' &pause ', ' ')
                                 .replace(' ', '---'))
        self.chord_text.SetFont(font4)
        self.song_text.SetValue(self.song_info["name"] + " (" + self.song_info["release year"] + ")"
                                             "\nArtist: " + self.song_info["artist"] +
                                             "\nSection: " + self.song_info["section"] +
                                             "\nBpm: " + str(round(float(self.song_info['tempo']))))

    def on_help_button(self,event):
        help_text = "Welcome to Hitmaker!\n\nGet inspired by generating and playing " \
                    "with hits progressions!!!\n\n#1 Choose a folder for the midi outputs by clicking on location\n\n " \
                    "#2 Generate and play away;)"
        wx.MessageBox(help_text, "Help", wx.OK | wx.ICON_INFORMATION)
    def on_play_button(self,event):
        if not self.song_info:
            wx.MessageBox("Please generate a chord progression first.", "Error", wx.OK | wx.ICON_ERROR)
            return
        midi_name = f"{self.midi_location}/{self.song_info['name']}__{self.song_info['artist']}__{self.song_info['section']}.mid"
        play_thread = threading.Thread(target=play, args=(midi_name,))
        play_thread.start()

    def on_stop_button(self,event):
        stop()


if __name__ == '__main__':
    app = wx.App()
    frame = Hitmaker(None, title="HitMaker", size=(600, 600))
    frame.Show()
    app.MainLoop()