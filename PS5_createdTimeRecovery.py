from ctypes import GetLastError
from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
import time
import os


def modifyFileTime(filepath, createTime, modifyTime, accessTime, offset):
    """
    用来修改PS5导出照片的创建时间
    """
    try:
        format = "%Y%m%d%H%M%S"  # 时间格式
        cTime_t = timeOffsetAndStruct(createTime, format, offset[0])
        mTime_t = timeOffsetAndStruct(modifyTime, format, offset[1])
        aTime_t = timeOffsetAndStruct(accessTime, format, offset[2])

        fh = CreateFile(filepath, GENERIC_READ | GENERIC_WRITE,
                        0, None, OPEN_EXISTING, 0, 0)
        createTimes, accessTimes, modifyTimes = GetFileTime(fh)

        createTimes = Time(time.mktime(cTime_t))
        accessTimes = Time(time.mktime(aTime_t))
        modifyTimes = Time(time.mktime(mTime_t))
        SetFileTime(fh, createTimes, accessTimes, modifyTimes)
        CloseHandle(fh)
        return 0
    except:
        return 1

#结构化时间
def timeOffsetAndStruct(times, format, offset):
    return time.localtime(time.mktime(time.strptime(times, format)) + offset)


# 获取文件名中的时间用于修改
def get_time(basename):
    if "_" in basename:
        temp_time = basename.split('_')[-1].split('.')[0]
        return temp_time


def get_filelist(dir):
    FileMap = {}
    for home, dirs, files in os.walk(os.getcwd()):
        for filename in files:
            FileMap[filename] = os.path.join(home, filename)
    return FileMap


if __name__ == '__main__':

    offset = (0, 1, 2)

    FileMap = get_filelist(dir)
    for key in FileMap:
        if key.split('.')[-1] == 'jpg' or key.split('.')[-1] == 'mp4':
            filepath = FileMap[key]
            temp_time = get_time(key)
            cTime = mTime = aTime = temp_time
            r = modifyFileTime(filepath, cTime, mTime, aTime, offset)
            if r == 0:
                print(key+'>>>>'+'修改完成')
            elif r == 1:
                print(key+'>>>>'+'修改失败')