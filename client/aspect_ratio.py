import win32api
import win32con
import aspect_ratio_config

def ratio(par: bool):
    if par == True:
        width = aspect_ratio_config.ASPECT_W
        height = aspect_ratio_config.ASPECT_H
    else:
        width = aspect_ratio_config.DEFAULT_W
        height = aspect_ratio_config.DEFAULT_H
    refresh_rate = aspect_ratio_config.HZ

    device = win32api.EnumDisplayDevices(None, 0)

    dm = win32api.EnumDisplaySettings(
        device.DeviceName,
        win32con.ENUM_CURRENT_SETTINGS
    )

    dm.PelsWidth = width
    dm.PelsHeight = height
    dm.DisplayFrequency = refresh_rate
    dm.Fields = (
        win32con.DM_PELSWIDTH |
        win32con.DM_PELSHEIGHT |
        win32con.DM_DISPLAYFREQUENCY
    )

    result = win32api.ChangeDisplaySettings(
        dm,
        win32con.CDS_UPDATEREGISTRY | win32con.CDS_GLOBAL
    )