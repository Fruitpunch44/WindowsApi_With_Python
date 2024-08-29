from ctypes import *
import sys
import os

# I just import most of the common types because I don't know how the structure looks like
from ctypes.wintypes import (HWND, LPSTR, DWORD, UINT, INT, WORD
, LPVOID, DWORD, CHAR, BYTE, WCHAR, BOOL, LPCSTR, HANDLE)


class FILETIME(Structure):
    _fields_ = [("dwLowDateTime", DWORD),
                ("dwHighDateTime", DWORD)]


class WIN32_FIND_DATAA(Structure):
    _fields_ = [("dwFileAttributes", DWORD),
                ("ftCreationTime", FILETIME),
                ("ftLastAccessTime", FILETIME),
                ("ftLastWriteTime", FILETIME),
                ("nFileSizeHigh", DWORD),
                ("nFileSizeLow", DWORD),
                ("dwReserved0", DWORD),
                ("dwReserved1", DWORD),
                ("cFileName", CHAR * 500),
                ("cAlternateFileName", CHAR * 32)]


class SYSTEMTIME(Structure):
    _fields_ = [("wYear", WORD),
                ("wMonth", WORD),
                ("wDayOfWeek", WORD),
                ("wDay", WORD),
                ("wHour", WORD),
                ("wMinute", WORD),
                ("wSecond", WORD),
                ("wMilliseconds", WORD)]


# instance of the WIN32_FIND_DATAT class
LPWIN32_FIND_DATAA = WIN32_FIND_DATAA()


# converting from file time to systemtime
def filetime_sytemtime(filetime):
    system_time = SYSTEMTIME()
    FileTimeToSystemTime = windll.kernel32.FileTimeToSystemTime
    FileTimeToSystemTime.argtypes = (POINTER(FILETIME), POINTER(SYSTEMTIME))
    FileTimeToSystemTime.restype = BOOL
    res = FileTimeToSystemTime(byref(filetime), byref(system_time))
    if not res:
        print('error')
    return system_time


'''
def getsystemtime():
    Gt_time = SYSTEMTIME()
    GetSystemTime = windll.kernel32.GetSystemTime
    GetSystemTime.argtype= (POINTER(SYSTEMTIME))
    GetSystemTime.restype = None
    info = GetSystemTime(byref(Gt_time))
    return info
'''

# initilizing the FindFirstFileA
FindFirstFileA = windll.Kernel32.FindFirstFileA
FindFirstFileA.argtypes = (LPCSTR, POINTER(WIN32_FIND_DATAA))
FindFirstFileA.restype = HANDLE

INVALID_HANDLE_VALUE = DWORD(-1).value

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [target file]")
    sys.exit(1)

hfind = FindFirstFileA(sys.argv[1].encode('utf-8'), byref(LPWIN32_FIND_DATAA))
if hfind == INVALID_HANDLE_VALUE:
    print("file not found")

else:
    creation_time = filetime_sytemtime(LPWIN32_FIND_DATAA.ftCreationTime)
    output = f"The file was found with handle {hfind}\n" \
             f"File name: {LPWIN32_FIND_DATAA.cFileName.decode('utf-8')}\n" \
             f"Creation time: {creation_time.wYear}-{creation_time.wMonth}-{creation_time.wDay}\n" \
             f"Current working directory of file: {os.getcwd()}\n"
    print(output)
    with open("FILE_search.txt", "a") as file:
        file.write(output)
        print("saved")
