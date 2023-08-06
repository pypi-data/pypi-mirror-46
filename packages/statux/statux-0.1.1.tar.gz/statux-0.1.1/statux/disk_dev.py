import errno
from os import listdir, readlink, statvfs
from os.path import basename, exists
from statux._conversions import set_bytes
from statux._errors import ValueNotFoundError, PartitionNotMountError, ex_handler
from collections import namedtuple

_PROC = "/proc/"
_DEV = "/dev/"
_DISK = "%sdisk/" % _DEV
_BLOCK_DEV = "/sys/block/"
_PARTITIONS = "%spartitions" % _PROC


@ex_handler(_PARTITIONS)
def partitions(remove_disks=True) -> list:
    """Returns a list with partitions

    :Params:
        :remove_disk (bool): If it's True removes block devices from the list

    """
    with open(_PARTITIONS, "r") as f:
        stat = f.readlines()
        res = []
        dsk = remove_disks and block_devices()
        for i in range(2, len(stat)):
            ptt = stat[i].split()[3]
            if not remove_disks or ptt not in dsk:
                res.append(ptt)
    return res

def _fix_escapes(string: str) -> str:
    # Sometimes Linux internally escapes path names. E.g. '/dev/disk/by-label/Data\x20Partition'. When
    # statux captures these strings, Python adds a new backslash. E.g. "Data\x20Partition" becomes
    # "Data\\x20Partition". To get this string as "Data Partition" is necessary to delete one backslash or
    # to encode and decode the string several times. This is the only way I've found. Explanation in:
    # https://es.stackoverflow.com/questions/261873/eliminar-una-barra-invertida-dentro-de-una-cadena-en-python
    return string if "\\" not in string else string.encode().decode("unicode-escape").encode("latin1").decode()

diccionario = {"loop0":
                   {"id": "a id",
                    "path": "a path",
                    "uuid": "a uuid",
                    },
                "nvme0n1":
                   {"id": "a id",
                    "path": "a path",
                    "uuid": "a uuid",
                    },
                "sda1":
                   {"id": "a id",
                    "path": "a path",
                    "uuid": "a uuid",
                    }
               }


def _get_disks_naming():
    def fix_name(string):
        return string.lstrip("by-")
    fields = [d for d in listdir(_DISK)]
    result = {ptt: {fix_name(d): "" for d in fields} for ptt in partitions(False)}
    for d in fields:
        pth = "%s%s/" % (_DISK, d)
        for field in listdir(pth):
            fn = "%s%s" % (pth, field)
            field_name = fix_name(fn.split("/")[-2])
            disk = basename(readlink(fn))
            result[disk][field_name] = _fix_escapes(field)
    return result


def disk_naming(disk_or_partition: str):
    dic = _get_disks_naming()[disk_or_partition]
    data = namedtuple(disk_or_partition, dic.keys())
    return data(*dic.values())


print(disk_naming("sda2"))