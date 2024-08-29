from ctypes import *
from ctypes.wintypes import (HWND, LPSTR, DWORD, UINT, INT, WORD
, LPVOID, DWORD, CHAR, BYTE, WCHAR, BOOL)

# since i couldn't find dwordlong this is another alternative for
DWORDLONG = c_ulonglong


# all of this was gotten of the Windows api docs
class SYSTEMINFO(Structure):
    _fields_ = [("wProcessorArchitecture", WORD),
                ("wReserved", WORD),
                ("dwPageSize", DWORD),
                ("lpMinimumApplicationAddress", LPVOID),
                ("lpMaximumApplicationAddress", LPVOID),
                ("dwActiveProcessorMask", DWORD),
                ("dwNumberOfProcessors", DWORD),
                ("dwProcessorType", DWORD),
                ("dwAllocationGranularity", DWORD),
                ("wProcessorLevel", WORD),
                ("wProcessorRevision", WORD),
                ]


class MEMORYSTATUSEX(Structure):
    _fields_ = [("dwLength", DWORD),
                (" dwMemoryLoad", DWORD),
                ("ullTotalPhys", DWORDLONG),
                ("ullAvailPhys", DWORDLONG),
                (" ullTotalPageFile", DWORDLONG),
                ("ullAvailPageFile", DWORDLONG),
                ("ullTotalVirtual", DWORDLONG),
                ("ullAvailVirtual", DWORDLONG),
                ("ullAvailExtendedVirtual", DWORDLONG)]


class OSVERSIONINFOEXA(Structure):
    _fields_ = [("dwOSVersionInfoSize", DWORD),
                ("dwMajorVersion", DWORD),
                ("dwMinorVersion", DWORD),
                ("dwBuildNumber", DWORD),
                ("dwPlatformId", DWORD),
                ("szCSDVersion", WCHAR * 128),
                ("wServicePackMajor", WORD),
                (" wServicePackMinor", WORD),
                ("wSuiteMask", WORD),
                ("wProductType", BYTE),
                ("wReserved", BYTE)]


class IP_ADDRESS_STRING(Structure):
    _fields_ = [("string", CHAR * 16)]


class IP_ADDR_STRING(Structure):
    _fields_ = [("Next", POINTER(IP_ADDRESS_STRING)),
                ("IpAddress", CHAR * 16),
                ("IpMask", CHAR * 16),
                ("Context", DWORD)]


class IP_ADAPTER_INFO(Structure):
    _fields_ = [
        ('ComboIndex', DWORD),
        ("AdapterName", CHAR * 256),
        ("Description", CHAR * 128),
        ("AddressLength", UINT),
        ("Address", BYTE * 8),
        ("Index", DWORD),
        ("Type", UINT),
        ("DhcpEnabled", UINT),
        ("CurrentIpAddress", IP_ADDRESS_STRING),
        ("IpAddressList", IP_ADDR_STRING),
        ("GatewayList", IP_ADDR_STRING),
        ("DhcpServer", IP_ADDR_STRING),
        ("HaveWins", BOOL),
        ("PrimaryWinsServer", IP_ADDR_STRING),
        ("SecondaryWinsServer", IP_ADDR_STRING),
        ("LeaseObtained", DWORD),
        ("LeaseExpires", DWORD),
    ]

# const buffer overflow value
ERROR_BUFFER_OVERFLOW = 111

# getting the dll and setting the argtype and return value
GetAdapterInfo = windll.iphlpapi.GetAdaptersInfo
GetAdapterInfo.argtypes = [POINTER(IP_ADAPTER_INFO), POINTER(c_ulong)]
GetAdapterInfo.restype = DWORD

# setting the buffer size and casting it to the IP_ADAPTER_INFO
buffer_size = DWORD(1500)
buffer = create_string_buffer(buffer_size.value)
info = POINTER(IP_ADAPTER_INFO)(cast(buffer, POINTER(IP_ADAPTER_INFO)))
res = GetAdapterInfo(info, byref(buffer_size))

# error handling in case of buffer overflow
if res == ERROR_BUFFER_OVERFLOW:
    # ERROR_BUFFER_OVERFLOW
    print("error buffer flow occured")
    buffer = create_string_buffer(buffer_size.value)
    res = GetAdapterInfo(cast(buffer, POINTER(IP_ADAPTER_INFO)), byref(buffer_size))

if pointer(info) == 0:
    print("error allocating memory to call adapter info")


OS_Version = OSVERSIONINFOEXA()
GlobalMemstat = MEMORYSTATUSEX()
system_info = SYSTEMINFO()
GlobalMemstat.dwLength = sizeof(MEMORYSTATUSEX)
OS_Version.dwOSVersionInfoSize = sizeof(OSVERSIONINFOEXA)

# getting the dll and setting the argtype and return value
GlobalMemoryStatusEx = windll.kernel32.GlobalMemoryStatusEx
GlobalMemoryStatusEx.argptype = (POINTER(MEMORYSTATUSEX))
GlobalMemoryStatusEx.restype = INT

# getting the dll and setting the argtype and return value
GetNativeSystemInfo = windll.kernel32.GetNativeSystemInfo
GetNativeSystemInfo.argtype = (POINTER(SYSTEMINFO))
GetNativeSystemInfo.restype = None

# getting the dll and setting the argtype and return value
GetVersionEXA = windll.kernel32.GetVersionExW
GetVersionEXA.argtype = (POINTER(OSVERSIONINFOEXA))
GetVersionEXA.restype = INT

# fetch info
GetNativeSystemInfo(byref(system_info))
GlobalMemoryStatusEx(byref(GlobalMemstat))
GetVersionEXA(byref(OS_Version))

# print info
print(f"Processor Architecture: {system_info.wProcessorArchitecture}")
print(f"Number of Processors: {system_info.dwNumberOfProcessors}")
print(f"Page Size: {system_info.dwPageSize} bytes")
print(f"Processor Type: {system_info.dwProcessorType}")
print(f"Allocation Granularity: {system_info.dwAllocationGranularity} bytes")
print(f"Minimum Application Address: {system_info.lpMinimumApplicationAddress}")
print(f"Maximum Application Address: {system_info.lpMaximumApplicationAddress}")

print(f"Total Physical Memory: {GlobalMemstat.ullTotalPhys}")
print(f"Available Physical Memory: {GlobalMemstat.ullAvailPhys}")
print(f"Total Virtual Memory: {GlobalMemstat.ullTotalVirtual}")
print(f"Available Virtual Memory: {GlobalMemstat.ullAvailVirtual}")

print(f"OS Version: {OS_Version.dwMajorVersion}.{OS_Version.dwMinorVersion}")
print(f"Build Number: {OS_Version.dwBuildNumber}")

# have some issues with this don't know why will figure it out later
print(f"Adapter Name: {info.contents.AdapterName.decode()}")
print(f"Description: {info.contents.Description.decode()}")
print( f"MAC Address: {':'.join(f'{info.contents.Address[i]:02X}' for i in range(info.contents.AddressLength))}")
print(f"Index: {info.contents.Index}")
print(f"Type: {info.contents.Type}")
