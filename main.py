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
    """bagian pewarnaan"""

    print(colored("[{icon}] {msg}".format(
        icon=icon, msg=msg), "{color}".format(color=color)))


def buat_folder(name):
    """bagian membuat folder,
    setelah user melilih artis langsung membuat folder
    dan pindah kedalam folder artis"""

    current_dir = os.getcwd()

    warna(START, "Lokasi sekarang: {path}".format(path=current_dir), GREEN)

    # replace spasi dengan underscore
    folder_name = "_".join(name.split())

    # membuat folder
    try:
        os.makedirs(current_dir+"/"+folder_name)
    except Exception as e:
        warna(CHECK, "Folder telah dibuat: {name} ".format(
            name=folder_name), RED)

    # setelah membuat folder pindah kedalam folder
    os.chdir(folder_name)
    warna(START, "Pindah folder: {path}".format(path=os.getcwd()), GREEN)
    print()


def ambil_nama_link():
    """bagian mendapatkan nama artis dan link """

    people_link = {}
    container = []

    response = session.get(URL)

    # ambil div articel dengan id
    page = response.html.find("#post-125697")
    get_articel = page

    # ambil tag ol
    for get_ols in get_articel:
        for get_ol in get_ols.find("ol"):

            # ambl tag li
            for get_lis in get_ol.find("li"):

                # setelah dapat tag li
                # ekplore link
                for link in get_lis.links:
                    # dapatkan nama artis
                    name = get_lis.text
                    # dapatkan link
                    link = link

                    # simpan hasil ke dict
                    # dan bungkus ke list agar tidak
                    # kena overwrite
                    people_link = {name: link}
                    container.append(people_link)

    return container


def pilih_narasumber(container):
    """bagian tampilan nama artis,link dan action pilih nama artis"""

    warna(START, "===== pilih artis dengan input nomer =====".upper(), RED)
    print()

    # akses list untuk mengambil nomer urut
    # sebagai menu pilih user
    for i, name in enumerate(container):

        # akes didct untuk menampilan nama artis
        for key, value in name.items():
            # print("""{i} {name} {link}""".format(i = i ,name = key, link = value))
            print("""[{i}] {name}""".format(i=i, name=key))

        if i == 42:
            break

    # user memilih nomer untuk menentukan artis yg di pilih
    pilih = int(input(colored("[*] Masukan Nomer: ".upper(), RED)))

    # menentukan index ke i untuk mementukan pilihan user
    for i, name in enumerate(container):
        for key, value in name.items():
            if pilih == i:
                # print(value)
                buat_folder(key)
                warna(CHECK, key, GREEN)
                sleep(3)
                ambil_content(value)


def ambil_content(url):
    """bagian mengambil konten mp3,
    setelah berhasil memilih artis,request ke halaman berikutnya
    dan cari link,untuk di download
    """

    links = []
    response = session.get(url)
    page = response.html.find("#content")

    # ambil div dengan id content
    for contents in page:

        # karenan link di bungkus dengan tabel
        # ambil tag tabel untuk di explor
        for get_tabels in contents.find("table"):

            # ambil link
            for link in get_tabels.links:
                # print(link)
                links.append(link)

    # bagian untuk meng ekplore hasil pengambilan link halaman
    # berikut nya
    ekplore_content(links)


def ekplore_content(link):
    """setelah berhasil mengambil link di dalam tabel,
    ekplore link dan buat menu tampilan"""

    for i, name in enumerate(link):
        # sorting tampilan hanya,tampilan nama surah saja

        name = re.findall(r"https://islamdownload.net/.*/.*/(.*)", name)[0]
        print("[{i}] {name}".format(i=i, name=name))

    # bagian user input
    # kondisi selalu true sampai user keluar sendiri
    ulang = True
    while(ulang):
        warna(
            START, "download satuan[nomer] / download semua[-0] / keluar[-1]".upper(), RED)
        pilih = int(input(colored("[*] Masukan Nomer: ", RED)))

        for i, name in enumerate(link):
            if pilih == i:
                name_re = re.findall(
                    r"https://islamdownload.net/.*/.*/(.*)", name)[0]
                warna(START, "{name}".format(name=name_re), GREEN)
                download(name)
                print()

            if pilih == -0:
                for download_all in link:
                    name = re.findall(
                        r"https://islamdownload.net/.*/.*/(.*)", name)[0]
                    warna(START, "{name}".format(name=name_re), GREEN)
                    download(download_all)

            if pilih == -1:
                ulang = False


def download(url):
    """bagian download konten"""

    wget.download(url)


def main():
    data = ambil_nama_link()
    pilih_narasumber(data)


if __name__ == "__main__":
    main()
