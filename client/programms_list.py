paths = {
    "steam": r'subprocess.Popen("C:\Program Files (x86)\Steam\steam.exe")',
    "riot": r'subprocess.Popen("C:\Riot Games\Riot Client\RiotClientServices.exe")',
    "discord": r"""os.system(r'start "" "%LocalAppData%\Discord\Update.exe" --processStart Discord.exe')"""
}