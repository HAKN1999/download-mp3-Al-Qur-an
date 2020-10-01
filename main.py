#!/usr/bin/python3
# coding: utf-8


from requests_html import HTMLSession
from termcolor import colored
from time import sleep
import wget
import os
import re


session = HTMLSession()


CHECK = "\u2713"
START = "*"
RED = "red"
GREEN = "green"
BLUE = "blue"
YELLOW = "yellow"


URL = "https://islamdownload.net/125697-download-mp3-al-quran-gratis-30-juz.html"


def warna(icon, msg, color):
    print(colored("[{icon}] {msg}".format(
        icon=icon, msg=msg), "{color}".format(color=color)))


def buat_folder(name):

    current_dir = os.getcwd()
    warna(START, "Lokasi sekarang: {path}".format(path=current_dir), GREEN)
    # replace spasi dengan underscore
    name = "_".join(name.split())

    # cek folder ada?
    try:
        os.makedirs(current_dir+"/"+name)
    except Exception as e:
        warna(CHECK, "Folder telah dibuat: {name} ".format(name=name), RED)

    # setelah membuat folder pindah kedalam folder
    # kemudian download
    os.chdir(name)
    warna(START, "Pindah folder: {path}".format(path=os.getcwd()), GREEN)
    print()


def ambil_nama_link():
    # bagian mendapatkan nama dan link

    people_link = {}
    container = []

    # get
    response = session.get(URL)

    # get bagian div articel
    page = response.html.find("#post-125697")

    get_articel = page
    for get_ols in get_articel:
        # daptakan tag ol
        for get_ol in get_ols.find("ol"):

            # dapatkan li
            for get_lis in get_ol.find("li"):

                # dapatkan link
                for link in get_lis.links:
                    # dapatkan nama orang
                    name = get_lis.text

                    # dapatkan link
                    link = link

                    # simpan hasil ke dict
                    # dan bungkus ke list
                    people_link = {name: link}
                    container.append(people_link)
    return container


def pilih_narasumber(container):
    # bagian tampilan nama link dan action pilih narasumber
    warna(START, "===== pilih narasumber dengan input nomer =====".upper(), RED)
    print()

    for i, name in enumerate(container):
        for key, value in name.items():
            # print("""{i} {name} {link}""".format(i = i ,name = key, link = value))
            print("""[{i}] {name}""".format(i=i, name=key))

        if i == 42:
            break

    print()
    pilih = int(input(colored("[*] Masukan Nomer: ", RED)))
    for i, name in enumerate(container):
        for key, value in name.items():
            if pilih == i:
                buat_folder(key)
                warna(CHECK, key, GREEN)
                sleep(3)
                # print(value)
                ambil_content(value)


def ambil_content(url):
    # bagian mengambil konten mp3

    links = []
    response = session.get(url)
    page = response.html.find("#content")

    # dapatkan content
    for contents in page:

        # dapatkan html
        for get_tabels in contents.find("table"):
            for link in get_tabels.links:
                # print(link)
                links.append(link)
                # download(link)

    ekplore_content(links)


def ekplore_content(link):

    # tampilkan konten
    for i, name in enumerate(link):
        name = re.findall(r"https://islamdownload.net/.*/.*/(.*)", name)[0]
        print("[{i}] {name}".format(i=i, name=name))

    # user pilih
    ulang = True
    while(ulang):
        warna(
            START, "download satuan[nomer] / download semua[-0] / keluar[-1]", RED)
        pilih = int(input(colored("[*] Masukan Nomer: ", RED)))

        for i, name in enumerate(link):
            if pilih == i:
                name_re = re.findall(
                    r"https://islamdownload.net/.*/.*/(.*)", name)[0]
                warna(START, "{}".format(name_re), GREEN)
                download(name)
                print()
            if pilih == -0:
                for download_all in link:
                    name = re.findall(
                        r"https://islamdownload.net/.*/.*/(.*)", name)[0]
                    warna(START, "{}".format(name_re), GREEN)
                    download(download_all)
            if pilih == -1:
                ulang = False


def download(url):
    # bagian download konten
    wget.download(url)


def main():
    data = ambil_nama_link()
    pilih_narasumber(data)


if __name__ == "__main__":
    main()
