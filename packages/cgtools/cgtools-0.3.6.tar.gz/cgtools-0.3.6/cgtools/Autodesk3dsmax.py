import os
import glob


class Autodesk3dsmax(object):

    def __init__(self):
        super(Autodesk3dsmax, self).__init__()
        self.exe_filename = None
        self.max_root = None
        self.version = None
        self.version_str = None
        self.icon = None
        self.bit = None

        self.startup_script_path = None
        self.local_startup_script_path = None

    def __lt__(self, s):
        return self.version_int() < s.version_int()

    def __gt__(self, s):
        return self.version_int() > s.version_int()

    def __eq__(self, s):
        return self.version_int() == s.version_int()

    def __ge__(self, s):
        return self.version_int() >= s.version_int()

    def __le_(self, s):
        return self.version_int() <= s.version_int()

    def version_int(self):
        v = int(self.version_str.split(' ')[-1])
        return v

    def __repr__(self):
        return '{}_{}'.format(self.version_str, self.bit)

    def get_default_exe(self):
        """
        获取ftype 关联
        :return:
        """
        data = os.popen('ftype 3dsmax').read()
        if '=' in data:
            exe = data.split('=')[1].split('" ')[0][1:]
            exe = os.path.abspath(exe)
            if os.path.exists(exe):
                return exe

    def get_hwnds(self):
        import win32gui
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

    def mxs_base64(self, code):
        import base64
        base_64_data = base64.b64encode(code.encode('gbk')).decode('utf-8')
        data = '''
base64data = "{}"
dotnet_encoding = dotnetclass "System.Text.Encoding"
ascii_object = dotnet_encoding.ASCII
dotnet_convert = dotnetclass "Convert"
bytes_data = dotnet_convert.FromBase64String(base64data)
real_data = ascii_object.Default.GetString(bytes_data);
execute(real_data);
        '''.format(base_64_data)
        data = data
        return data

    def filein_script_code(self, script_filename):
        """
        生成filein脚本的mxs代码
        :param script_filename:
        """
        code = 'try(filein @"{}";)catch(print ("error_filein:"+@"{}"))'.format(script_filename, script_filename)
        code = 'try(if (maxversion())[1] >= 21000 then(filein @"{}";)else({});)catch(print "error_kjk")'.format(
            script_filename,
            self.mxs_base64(code))
        return code

    def ready_data_from_finder(self, data):
        self.exe_filename = data['path']
        self.version = data['version']
        self.version_str = data['version_string']
        self.icon = data['icon']
        self.bit = data['bit']

        self.max_root = os.path.dirname(self.exe_filename)

        self.startup_script_path = os.path.join(self.max_root, 'scripts\Startup')
        self.local_startup_script_path = data['local_path']

    def install_startup_script(self, filename, data, menu_name=None):
        """
        安装启动脚本
        :param data:
        """

        lang_lst = glob.glob(self.local_startup_script_path + "\\*\\scripts\\startup")

        is_sucess = False

        for lang_folder in lang_lst:
            full_script_filename = os.path.join(lang_folder, filename)

            try:
                with open(full_script_filename, 'wb') as f:
                    f.write(data.encode())
                    is_sucess = True
            except:
                pass

            self.build_clear_menu_script(lang_folder, menu_name, by_install=True)

        if not is_sucess:
            # 尝试安装到主目录
            full_script_filename = os.path.join(self.startup_script_path, filename)

            try:
                with open(full_script_filename, 'wb') as f:
                    f.write(data.encode())
                    return True
            except:
                pass

        self.build_clear_menu_script(self.startup_script_path, menu_name, by_install=True)

        return True

    def build_clear_menu_script(self, folder, menu_name=None, by_install=False):
        mxs_code = u'''
        -- 自动清理空间酷残留菜单 本脚本会自动删除
        try(
        temp_source_filename = filenamefrompath(getsourcefilename())
        temp_filter_str = filterstring temp_source_filename "."
        menu_name = temp_filter_str[1]
        manMenu = menuMan.getMainMenuBar()
        for i in 1 to manMenu.numItems() do
        (
        try(menu = manMenu.getItem(i))catch()
        if menu.getTitle() == menu_name do(
        manMenu.removeItem menu;
        menuMan.updateMenuBar()
        )
        )
        )catch()
        try(deletefile (getsourcefilename()))catch()
        '''

        temp_filename = os.path.join(folder, '{}.ms'.format(menu_name))

        if by_install:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
            return True

        if not menu_name:
            return False

        try:
            with open(temp_filename, 'wb') as f:
                f.write(mxs_code.encode('gbk'))
        except:
            return False

    def uninstall_startup_script(self, filename, menu_name=None):
        """
        卸载启动脚本
        """
        # 用户路径
        lang_lst = glob.glob(self.local_startup_script_path + "\\*\\scripts\\startup")

        for lang_folder in lang_lst:
            full_script_filename = os.path.join(lang_folder, filename)
            if os.path.exists(full_script_filename):
                os.remove(full_script_filename)

            # 生成顶级菜单清理脚本
            self.build_clear_menu_script(lang_folder, menu_name)

        # max 安装路径
        full_script_filename = os.path.join(self.startup_script_path, filename)
        if os.path.exists(full_script_filename):
            os.remove(full_script_filename)

        # 生成顶级菜单清理脚本
        self.build_clear_menu_script(self.startup_script_path, menu_name)

    def is_install_startup_script(self, filename, code=None):
        """
        是否安装过启动脚本
        data = 脚本内容
        :rtype: object
        """

        lang_lst = glob.glob(self.local_startup_script_path + "\\*\\scripts\\startup")

        is_installed = False

        for lang_folder in lang_lst:
            full_script_filename = os.path.join(lang_folder, filename)

            if os.path.exists(full_script_filename):
                with open(full_script_filename, 'rb') as f:
                    old_code = f.read()
                    if old_code == code.encode():
                        is_installed = True

        if is_installed == False:
            full_script_filename = os.path.join(self.startup_script_path, filename)

            if os.path.exists(full_script_filename):
                with open(full_script_filename, 'rb') as f:
                    old_code = f.read()
                    if old_code == code.encode():
                        is_installed = True

        return is_installed


if __name__ == '__main__':
    data = {'bit': '64',
            'local_path': r'C:\Users\Administrator\AppData\Local\Autodesk\3dsMax\2012 - 64bit',
            'icon': {'large': 'C:\\Program Files\\Autodesk\\3ds Max '
                              '2014\\UI_ln/Icons/ATS/ATSScene.ico',
                     'small': 'C:\\Program Files\\Autodesk\\3ds Max '
                              '2014\\UI_ln/Icons/ATS/ATSScene.ico'},
            'path': 'C:\\Program Files\\Autodesk\\3ds Max 2014\\3dsmax.exe',
            'version': 1604200000,
            'version_string': '3dsmax 2014'}

    a = Autodesk3dsmax()
    print(a.get_default_exe())

    # a.ready_data_from_finder(data)
    #
    # file_in_code = a.filein_script_code(r"E:\XDL_MANAGER3\plug-ins\3dsmax\xdl_init.ms")
    # file_in_name = 'kjj_init_test.ms'
    #
    # print(file_in_code)
    #
    # # print(a.is_install_startup_script(file_in_name, file_in_code))
    # print(a.install_startup_script(file_in_name, file_in_code))
