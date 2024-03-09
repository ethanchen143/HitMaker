from cx_Freeze import setup, Executable

# Include additional data files
includefiles = ['/Users/ethanchen/PycharmProjects/Hitmaker/cleaned_data.csv','/Users/ethanchen/PycharmProjects/Hitmaker/background.png']  # Add other files if needed

packages = ["music21", "pygame", "requests", "spotipy", "wx"]

options = {
    'build_exe': {
        'include_files': includefiles,
        'packages': packages
    }
}

setup(
    name="HitMaker",
    version="1.0",
    description="HitMaker App",
    options=options,
    executables=[Executable("Hitmaker.py")]
)


