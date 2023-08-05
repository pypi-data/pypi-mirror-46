# coding: utf-8
#
"""
python -m apkutils COMMAND

Commands:
    install     Install apk to device
"""

from __future__ import absolute_import

import argparse
import os
import re
import sys
import time
import hashlib

import requests

from adbutils import adb as adbclient
from adbutils import AdbError, AdbInstallError

MB = 1024 * 1024


def humanize(n: int) -> str:
    return '%.1f MB' % (float(n) / MB)


class ReadProgress():
    def __init__(self, r, total_size: int):
        self.r = r
        self.total = total_size
        self.copied = 0
        self.start_time = time.time()
        self.update_time = time.time()
        self.m = hashlib.md5()
        self._chunk_size = 0
        self._hash = ''

    def update(self, chunk: bytes):
        chunk_size = len(chunk)
        self.m.update(chunk)
        if chunk_size == 0:
            self._hash = self.m.hexdigest()
        self.copied += chunk_size
        self._chunk_size += chunk_size

        if self.total:
            percent = float(self.copied) / self.total * 100
        else:
            percent = 0.0 if chunk_size else 100.0

        p = int(percent)
        duration = time.time() - self.update_time
        if p == 100.0 or duration > 1.0:
            if duration:
                speed = humanize(self._chunk_size / duration) + "/s"
            else:
                copytime = time.time() - self.start_time
                speed = humanize(self.copied / copytime) + "/s"

            self.update_time = time.time()
            self._chunk_size = 0

            copysize = humanize(self.copied)
            totalsize = humanize(self.total)
            print("{:.1f}%\t{} [{}/{}]".format(percent, speed, copysize,
                                               totalsize))

    def read(self, n: int) -> bytes:
        chunk = self.r.read(n)
        self.update(chunk)
        return chunk


def main():
    parser = argparse.ArgumentParser()
    # formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-s", "--serial", help="device serial number")
    parser.add_argument(
        "-V",
        "--server-version",
        action="store_true",
        help="show adb server version")
    parser.add_argument(
        "-l", "--list", action="store_true", help="list devices")
    parser.add_argument(
        "-i", "--install", help="install from local apk or url")
    parser.add_argument("-u", "--uninstall", help="uninstall apk")
    parser.add_argument(
        "--clear", action="store_true", help="clear all data when uninstall")
    parser.add_argument(
        "--list-packages", action="store_true", help="list packages installed")
    parser.add_argument("--grep", help="filter matched package names")
    parser.add_argument("--connect", type=str, help="connect remote device")
    parser.add_argument(
        "--shell", action="store_true", help="run shell command")
    parser.add_argument("args", nargs="*", help="arguments")

    args = parser.parse_args()

    if args.connect:
        adbclient.connect(args.connect)
        return

    if args.server_version:
        print("ADB Server version: {}".format(adbclient.server_version()))
        return

    if args.list:
        rows = []
        for d in adbclient.devices():
            rows.append([d.serial, d.shell("getprop ro.product.model")])
        lens = []
        for col in zip(*rows):
            lens.append(max([len(v) for v in col]))
        format = "  ".join(["{:<" + str(l) + "}" for l in lens])
        for row in rows:
            print(format.format(*row))
        return

    d = adbclient.device_with_serial(args.serial)

    if args.shell:
        output = d.shell(args.args)
        print(output)
        return

    if args.install:
        dst = "/data/local/tmp/tmp-%d.apk" % (int(time.time() * 1000))
        print("push to %s" % dst)
        if re.match(r"^https?://", args.install):
            resp = requests.get(args.install, stream=True)
            resp.raise_for_status()
            length = int(resp.headers.get("Content-Length", 0))
            r = ReadProgress(resp.raw, length)
        else:
            length = os.stat(args.install).st_size
            fd = open(args.install, "rb")
            r = ReadProgress(fd, length)

        start = time.time()
        d.sync.push(r, dst)
        print("Success pushed, time used %d seconds" % (time.time() - start))

        new_dst = "/data/local/tmp/tmp-%s.apk" % r._hash[:8]
        d.shell_output("mv", dst, new_dst)
        dst = new_dst
        info = d.sync.stat(dst)
        print("verify pushed apk, md5: %s, size: %s" % (r._hash,
                                                        humanize(info.size)))
        assert info.size == r.copied

        print("install to android system ...")
        try:
            start = time.time()
            d.install_remote(dst, clean=True)
            print("Success installed, time used %d seconds" %
                  (time.time() - start))
        except AdbInstallError as e:
            sys.exit("Failure " + e.reason + "\n" +
                     "Remote apk is not removed. Manually install command:\n\t"
                     + "adb shell pm install -r -t " + dst)

    elif args.uninstall:
        d.shell_output("pm", "uninstall", args.uninstall)

    elif args.list_packages:
        patten = re.compile(args.grep or ".*")
        for p in d.list_packages():
            if patten.search(p):
                print(p)


if __name__ == "__main__":
    main()
