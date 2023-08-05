import string
import ctypes
import platform
import subprocess
from typing import Union
from pathlib import Path
from ctypes import wintypes, windll

"""
Platform-independent server-share path discovery.
"""

mpr = ctypes.WinDLL('mpr')

ERROR_SUCCESS = 0x0000
ERROR_MORE_DATA = 0x00EA

wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)
mpr.WNetGetConnectionW.restype = wintypes.DWORD
mpr.WNetGetConnectionW.argtypes = (wintypes.LPCWSTR,
                                   wintypes.LPWSTR,
                                   wintypes.LPDWORD)


def __get_drives() -> list:
    """
    Gets all available mapped drive letters.
    https://stackoverflow.com/questions/827371/is-there-a-way-to-list-all-the-available-drive-letters-in-python?answertab=oldest#tab-top
    :return: list of available drive letters
    """
    drives = list()
    bit_mask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bit_mask & 1:
            drives.append(letter)
        bit_mask >>= 1
    return drives


def __get_connection(drive_letter: str, debug: bool = False) -> Union[str, None]:
    """
    Get full connection name from mapped drive letter.
    https://stackoverflow.com/questions/34801315/get-full-computer-name-from-a-network-drive-letter-in-python
    :param drive_letter: mapped drive letter
    :return: string as "\\server\drive" or None if no connection
    """
    local_name = drive_letter + ":"
    length = (wintypes.DWORD * 1)()
    result = mpr.WNetGetConnectionW(local_name, None, length)
    if result != ERROR_MORE_DATA:
        if debug:
            raise ctypes.WinError(result)
        else:
            return
    remote_name = (wintypes.WCHAR * length[0])()
    result = mpr.WNetGetConnectionW(local_name, remote_name, length)
    if result != ERROR_SUCCESS:
        if debug:
            raise ctypes.WinError(result)
        else:
            return
    return remote_name.value


def __get_network_drive_with_share(server_name: str, share_name: str) -> Union[str, None]:
    """
    Get a network drive letter given a server and share name.
    ex. \\my-computer\share -> D if (D:\\ == \\my-computer\share)
    :param share_name: name of share to search for
    :return: single letter string of drive letter if found else None
    """
    net_match = r"\\{}\{}".format(server_name, share_name)

    # check whether this is a mapped network drive and the connection name is \\server\share
    drives = __get_drives()
    for drive in drives:
        connection = __get_connection(drive)
        if connection == net_match:
            return drive


def __get_local_drive_with_share(share_name: str) -> Union[str, None]:
    """
    Get a local drive letter given a share name.
    ex. \\my-computer\share -> D if (D:\\ == \\my-computer\share)
    :param share_name: name of share to search for
    :return: single letter string of drive letter if found else None
    """
    # check shared network drives to see if we have the drive locally (we're the ones sharing it)
    s = subprocess.check_output(['net', 'share']).decode()  # get shared drives
    for row in s.split("\n")[4:]:   # check each row after formatting
        split = row.split()
        if len(split) >= 2 and split[0] == share_name:  # if the share name matches
            return split[1][0]


def get_path(
        server_name: str,
        share_name: str = "",
        unix_path_prefix: str = "/mnt"
) -> Path:
    """
    Returns the server path for a given server name and shared drive name.

    # When discovering the server path from a Windows machine.
    #   Windows machines require a share name.
    #   We will always attempt to look for mapped drives that contain the share name.
    #   This is to prevent slowdown from accessing a drive using "\\server\share" vs. "D:\".

    # When discovering the server path from a Unix machine.
    #   Unix machines do not require a share name.
    #   A unix path prefix is usually specified to point to where shared drives are mounted.
    #   The default value for this prefix is "/mnt" assuming the drive was mounted with Samba.

    :param server_name: name of server
    :param share_name: name of shared drive on server
    :param unix_path_prefix: path prefix where shares are mounted if on unix machine (default assumes Samba shares)
    :return: Path object containing full path to share on server
    """
    if platform.system() == 'Windows':
        if not share_name == "":
            # if the host name is the same as the server name, that means that this is a shared network drive, so figure
            # out which lettered drive it is
            if platform.node().lower() == server_name.lower():
                local = __get_local_drive_with_share(share_name=share_name)
                if local:
                    return Path(r"{}:\\".format(local))
            else:
                # attempt to get find mapped network drive
                net = __get_network_drive_with_share(server_name=server_name, share_name=share_name)
                if net:
                    return Path(r"{}:\\".format(net))     # use the drive letter
            # if mapped network drive or local drive for this server and share is not found,
            # just return full Windows server path
            return Path(r'\\{}\{}'.format(server_name, share_name))
        else:
            raise ValueError("Must specify share name if on Windows machine and accessing external server.")
    else:
        if platform.node() == server_name:
            return Path('/{}'.format(share_name))
        if share_name == "":
            return Path('{}/{}'.format(unix_path_prefix, server_name))
        else:
            return Path('{}/{}/{}'.format(unix_path_prefix, server_name, share_name))
