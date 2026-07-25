paths = {
    "steam": r'subprocess.Popen("C:\Program Files (x86)\Steam\steam.exe")',
    "riot": r'subprocess.Popen("C:\Riot Games\Riot Client\RiotClientServices.exe")',
    "discord": 'subprocess.Popen([os.path.join(os.environ["LocalAppData"], "Discord", "Update.exe"), "--processStart", "Discord.exe"])',
    "edge": r'subprocess.Popen("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")'
}