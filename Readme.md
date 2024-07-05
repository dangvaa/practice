1) Создать виртуальное окружение: conda create --name env python=3.8
2) Активировать виртуальное окружение: conda activate env
3) Установить необходимые библиотеки: pip install -r requirements.txt
4) Запустить приложение: python main.py
   
если при запуске в линукс появляется предупреждение:
> Warning: Ignoring XDG_SESSION_TYPE=wayland on Gnome. Use QT_QPA_PLATFORM=wayland to run on Wayland anyway.
> QObject::moveToThread: Current thread (0x2b9ce40) is not the object's thread (0x2d9da10).
> Cannot move to target thread (0x2b9ce40)
> 
> qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "/home/vboxuser/anaconda3/envs/env/lib/python3.8/site-packages/cv2/qt/plugins" even though it was found.
> This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
> 
> Available platform plugins are: xcb, eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl.
> 
> Aborted

Нужно прописать: export QT_QPA_PLATFORM=wayland

Затем запустить: python main.py