import win32gui


def get_hwnds():
    hwnds = []

    def hwnd_s(a, h):
        try:
            if win32gui.IsWindow(a) and win32gui.IsWindowVisible(a) and \
                    win32gui.IsWindowEnabled(a):
                h.append((win32gui.GetClassName(a), win32gui.GetWindowText(a), a))
        except:
            pass

    win32gui.EnumWindows(hwnd_s, hwnds)

    hwnd_infos = []
    set_list = []
    for c_name, w_title, hwnd in hwnds:

        if c_name == "3DSMAX" and hwnd not in set_list:
            set_list.append(hwnd)
            hwnd_infos.append([w_title, hwnd])
            continue

        if c_name == 'Qt5QWindowIcon' and '3ds Max 2' in w_title:
            if hwnd not in set_list:
                set_list.append(hwnd)
                hwnd_infos.append([w_title, hwnd])

    return hwnd_infos


print(get_hwnds())
