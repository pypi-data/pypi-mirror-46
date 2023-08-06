"""
This module is specifically intended for use when in environments where
you're actively trying to share/develop tools across multiple applications
which support PyQt, PySide or PySide2. 

The premise is that you can request the main application window using 
a common function regardless of the actual application - making it trivial
to implement a tool which works in multiple host applications without any
bespoke code.

The current list of supported applications are:

    * Native Python
    * Maya
    * 3dsmax
    * Motion Builder

"""
import sys
from .vendor import Qt


# ------------------------------------------------------------------------------
def get_host():

    global HOST

    if HOST:
        return HOST

    if 'maya.exe' in sys.executable or 'mayapy.exe' in sys.executable:
        HOST = 'Maya'
        return HOST

    if 'motionbuilder.exe' in sys.executable:
        HOST = 'Mobu'
        return HOST

    if '3dsmax.exe' in sys.executable:
        HOST = 'Max'
        return HOST

    return 'Pure'


# ------------------------------------------------------------------------------
def mainWindow():
    """
    Returns the main window regardless of what the host is
    
    :return: 
    """
    return HOST_MAPPING[get_host()]()


# ------------------------------------------------------------------------------
def returnNativeWindow():
    for candidate in Qt.QtWidgets.QApplication.topLevelWidgets():
        if isinstance(candidate, Qt.QtWidgets.QMainWindow):
            return candidate


# ------------------------------------------------------------------------------
def _findWindowByTitle(title):
    # -- Find the main application window
    for candidate in Qt.QtWidgets.QApplication.topLevelWidgets():
        try:
            if title in candidate.windowTitle():
                return candidate
        except: pass

# ------------------------------------------------------------------------------
def returnModoMainWindow():
    pass


# ------------------------------------------------------------------------------
def returnMaxMainWindow():
    return _findWindowByTitle('Autodesk 3ds Max')


# ------------------------------------------------------------------------------
def returnMayaMainWindow():
    from maya import OpenMayaUI as omui
    from shiboken2 import wrapInstance

    return wrapInstance(long(omui.MQtUtil.mainWindow()), Qt.QtWidgets.QWidget)


# ------------------------------------------------------------------------------
def returnMobuMainWindow():
    return _findWindowByTitle('MotionBuilder 20')


# ------------------------------------------------------------------------------
HOST = None
HOST_MAPPING = dict(
    Maya=returnMayaMainWindow,
    Max=returnMaxMainWindow,
    Modo=returnModoMainWindow,
    Mobu=returnMobuMainWindow,
    Pure=returnNativeWindow,
)
