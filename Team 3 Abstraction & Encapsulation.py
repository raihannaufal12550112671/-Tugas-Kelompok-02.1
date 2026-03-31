# Nama Anggota Team 3   : 1. Raihan Naufal (12550112671)
#                         2. Muhammad Fatur Firdaus (12550112783)
#                         3. Mutiara Putri Salim (12550122824)
# Kelas                 : H
# Dosen                 : Muhammad Affandes, S.T., M.T.

from abc import ABC, abstractmethod
from datetime import datetime

# MIXIN
class LogMixin:
    def log(self, pesan):
        print(f"[LOG]: {pesan}")

# ABSTRACT CLASS
class Item(ABC):
    @abstractmethod
    def tampilkan_info(self):
        pass

# CLASS BUKU
class Buku(Item, LogMixin):
    def __init__(self, judul, penulis):
        self.__judul = judul
        self.__penulis = penulis
        self.__status = "Tersedia"

    def get_judul(self):
        return self.__judul

    def get_penulis(self):
        return self.__penulis

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def tampilkan_info(self):
        print(f"Judul: {self.__judul} | Penulis: {self.__penulis} | Status: {self.__status}")

# CLASS USER
class User:
    def __init__(self, nama, peran):
        self.nama = nama
        self.peran = peran

    def get_peran(self):
        return self.peran

# CLASS PERPUSTAKAAN
class Perpustakaan(LogMixin):
    def __init__(self):
        self.__daftar_buku = []
        self.__riwayat_peminjaman = []

    # ADMIN & PEGAWAI
    def tambah_buku(self, user, buku):
        if user.get_peran() in ["Administrator", "Pegawai"]:
            self.__daftar_buku.append(buku)
            self.log("Buku ditambahkan")
        else:
            print("Akses ditolak!")

    def hapus_buku(self, user, judul):
        if user.get_peran() in ["Administrator", "Pegawai"]:
            for buku in self.__daftar_buku:
                if buku.get_judul().lower() == judul.lower():
                    self.__daftar_buku.remove(buku)
                    self.log("Buku dihapus")
                    return
            print("Buku tidak ditemukan!")
        else:
            print("Akses ditolak!")

    def tandai_rusak(self, user, judul):
        if user.get_peran() in ["Administrator", "Pegawai"]:
            buku = self.cari_buku(judul)
            if buku:
                buku.set_status("Rusak")
                self.log(f"Buku '{judul}' ditandai rusak")
            else:
                print("Buku tidak ditemukan!")
        else:
            print("Akses ditolak!")

    def update_buku(self, user, judul_lama, judul_baru):
        if user.get_peran() in ["Administrator", "Pegawai"]:
            buku = self.cari_buku(judul_lama)
            if buku:
                buku._Buku__judul = judul_baru
                self.log("Buku diperbarui")
        else:
            print("Akses ditolak!")

    # SEMUA PERAN
    def tampilkan_buku(self):
        print("\n=== DAFTAR BUKU ===")
        if not self.__daftar_buku:
            print("Belum ada buku.")
        for buku in self.__daftar_buku:
            buku.tampilkan_info()

    def cari_buku(self, judul):
        for buku in self.__daftar_buku:
            if judul.lower() in buku.get_judul().lower():
                return buku
        return None

    # MAHASISWA
    def pinjam_buku(self, user, judul):
        if user.get_peran() == "Mahasiswa":
            buku = self.cari_buku(judul)
            if buku and buku.get_status() == "Tersedia":
                buku.set_status("Dipinjam")
                self.__riwayat_peminjaman.append(datetime.now())
                self.log(f"{user.nama} meminjam Buku'{judul}'")
            else:
                print("Buku tidak tersedia!")
        else:
            print("Hanya mahasiswa yang bisa meminjam!")

    def kembalikan_buku(self, user, judul):
        if user.get_peran() == "Mahasiswa":
            buku = self.cari_buku(judul)
            if buku:
                buku.set_status("Tersedia")
                self.log(f"{user.nama} mengembalikan '{judul}'")
        else:
            print("Hanya mahasiswa yang bisa mengembalikan!")

    # STATISTIK
    def statistik_peminjaman(self):
        per_hari = {}
        per_bulan = {}

        for tgl in self.__riwayat_peminjaman:
            hari = tgl.strftime("%Y-%m-%d")
            bulan = tgl.strftime("%Y-%m")

            per_hari[hari] = per_hari.get(hari, 0) + 1
            per_bulan[bulan] = per_bulan.get(bulan, 0) + 1

        print("\nStatistik Peminjaman per Hari:")
        for k, v in per_hari.items():
            print(k, ":", v)

        print("\nStatistik Peminjaman per Bulan:")
        for k, v in per_bulan.items():
            print(k, ":", v)

    def statistik_kondisi_buku(self):
        kondisi = {"Tersedia": 0, "Dipinjam": 0, "Rusak": 0}

        for buku in self.__daftar_buku:
            kondisi[buku.get_status()] += 1

        print("\nStatistik Kondisi Buku:")
        for k, v in kondisi.items():
            print(k, ":", v)

# MAIN PROGRAM
def main():
    perpus = Perpustakaan()

    print("=== LOGIN ===")
    nama = input("Nama: ")
    print("1. Administrator")
    print("2. Pegawai")
    print("3. Mahasiswa")
    pilih = input("Pilih peran: ")

    if pilih == "1":
        peran = "Administrator"
    elif pilih == "2":
        peran = "Pegawai"
    else:
        peran = "Mahasiswa"

    user = User(nama, peran)

    while True:
        print(f"\nLogin sebagai: {user.peran}")
        print("1. Tambah Buku")
        print("2. Tampilkan Informasi Data Buku")
        print("3. Update Buku")
        print("4. Hapus Buku")
        print("5. Pinjam Buku")
        print("6. Kembalikan Buku")
        print("7. Statistik Peminjaman Buku")
        print("8. Statistik Kondisi Buku")
        print("9. Tandai Buku Rusak")
        print("10. Ganti User")
        print("0. Keluar")
        print()

        pilih = input("Pilih menu: ")
        print()

        if pilih == "1":
            judul = input("Judul buku: ")
            penulis = input("Penulis: ")
            perpus.tambah_buku(user, Buku(judul, penulis))

        elif pilih == "2":
            perpus.tampilkan_buku()

        elif pilih == "3":
            lama = input("Judul lama: ")
            baru = input("Judul baru: ")
            perpus.update_buku(user, lama, baru)

        elif pilih == "4":
            judul = input("Judul buku: ")
            perpus.hapus_buku(user, judul)

        elif pilih == "5":
            judul = input("Judul buku: ")
            perpus.pinjam_buku(user, judul)

        elif pilih == "6":
            judul = input("Judul buku: ")
            perpus.kembalikan_buku(user, judul)

        elif pilih == "7":
            perpus.statistik_peminjaman()

        elif pilih == "8":
            perpus.statistik_kondisi_buku()

        elif pilih == "9":
            judul = input("Judul buku: ")
            perpus.tandai_rusak(user, judul)

        elif pilih == "10":
            print("\n=== GANTI USER ===")
            nama = input("Nama: ")
            print("1. Administrator")
            print("2. Pegawai")
            print("3. Mahasiswa")
            pilih_peran = input("Pilih peran: ")

            if pilih_peran == "1":
                peran = "Administrator"
            elif pilih_peran == "2":
                peran = "Pegawai"
            else:
                peran = "Mahasiswa"

            user = User(nama, peran)

        elif pilih == "0":
            print("Terima kasih telah menggunakan program pustaka digital!")
            break

        else:
            print("Pilihan salah/tidak sesuai!")


if __name__ == "__main__":
    main()