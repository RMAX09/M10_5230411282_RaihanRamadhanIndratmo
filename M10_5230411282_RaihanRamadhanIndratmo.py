import mysql.connector
from datetime import datetime
from tabulate import tabulate


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='penjualan'
        )
        self.cur = self.conn.cursor()

    def execute_query(self, query, params=None):
        try:
            self.cur.execute(query, params)
            return self.cur.fetchall()
        except mysql.connector.Error as e:
            print(f"Kesalahan: {e}")
        finally:
            self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


class Pegawai:
    def __init__(self, db: Database):
        self.db = db

    def tampilkan(self):
        hasil = self.db.execute_query("SELECT * FROM pegawai")
        if hasil:
            print(tabulate(hasil, headers=[
                  "NIK", "Nama", "Alamat"], tablefmt="grid"))
        else:
            print("Tidak ada data pegawai.")

    def tambah(self, id, nama, alamat):
        if not id or not nama or not alamat:
            print("Data tidak boleh kosong!")
            return
        self.db.execute_query(
            "INSERT INTO pegawai (NIK, nama_pegawai, alamat_pegawai) VALUES (%s, %s, %s)", (id, nama, alamat))
        print("Pegawai berhasil ditambahkan!")


class Produk:
    def __init__(self, db: Database):
        self.db = db

    def tampilkan(self):
        hasil = self.db.execute_query("SELECT * FROM produk")
        if hasil:
            print(tabulate(hasil, headers=[
                  "ID Produk", "Nama", "Jenis", "Harga"], tablefmt="grid"))
        else:
            print("Tidak ada data produk.")

    def tambah(self, id, nama, jenis, harga):
        if not id or not nama or not jenis or not harga:
            print("Data tidak boleh kosong!")
            return
        self.db.execute_query("INSERT INTO produk (id_produk, nama_produk, jenis_produk, harga_produk) VALUES (%s, %s, %s, %s)",
                              (id, nama, jenis, harga))
        print("Produk berhasil ditambahkan!")


class Transaksi:
    def __init__(self, db: Database):
        self.db = db

    def tampilkan(self):
        hasil = self.db.execute_query("SELECT * FROM transaksi")
        if hasil:
            print(tabulate(hasil, headers=[
                  "ID Transaksi", "Jumlah", "ID PRODUK"], tablefmt="grid"))
        else:
            print("Tidak ada data transaksi.")

    def tambah(self, id, id_produk, jumlah_beli):
        if not id or not id_produk or not jumlah_beli:
            print("Data tidak boleh kosong!")
            return
        self.db.execute_query("INSERT INTO transaksi (id_transaksi, id_produk, jumlah_beli) VALUES (%s, %s, %s)",
                              (id, id_produk, jumlah_beli))
        print("Transaksi berhasil ditambahkan!")


class Struk:
    def __init__(self, db: Database):
        self.db = db

    def tampilkan(self, id_transaksi):
        query = """
        SELECT produk.nama_produk, transaksi.jumlah_beli, produk.harga_produk, 
               (produk.harga_produk * transaksi.jumlah_beli) AS total_per_barang
        FROM transaksi
        JOIN produk ON produk.id_produk = transaksi.id_produk
        WHERE transaksi.id_transaksi = %s
        """
        hasil = self.db.execute_query(query, (id_transaksi,))
        struk = self.db.execute_query(
            "SELECT total_harga FROM struk WHERE id_transaksi=%s", (id_transaksi,))
        if hasil and struk:
            print(tabulate(hasil, headers=[
                  "Nama Produk", "Jumlah", "Harga", "Total"], tablefmt="grid"))
            print(f"Total Harga: {struk[0][0]}")
        else:
            print("Struk tidak ditemukan.")

    def tambah(self, id, total_harga, NIK):
        if not id or not total_harga or not NIK:
            print("Data tidak boleh kosong!")
            return

        if not self.db.execute_query("SELECT 1 FROM pegawai WHERE NIK=%s", (NIK,)):
            print("NIK Pegawai tidak ditemukan!")
            return
        tanggal = datetime.now()
        self.db.execute_query("INSERT INTO struk (id_transaksi, tanggal, total_harga, NIK) VALUES (%s, %s, %s, %s)",
                              (id, tanggal, total_harga, NIK))
        print("Struk berhasil ditambahkan!")


def main_menu():
    db = Database()
    pegawai = Pegawai(db)
    produk = Produk(db)
    transaksi = Transaksi(db)
    struk = Struk(db)

    while True:
        print("\nMenu Utama")
        menu = ["Tampilkan Pegawai", "Tambah Pegawai",
                "Tampilkan Produk", "Tambah Produk",
                "Tampilkan Transaksi", "Tambah Transaksi",
                "Tampilkan Struk", "Tambah Struk", "Keluar"]
        for i, item in enumerate(menu, 1):
            print(f"{i}. {item}")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            pegawai.tampilkan()
        elif pilihan == '2':
            pegawai.tambah(input("NIK: "), input("Nama: "), input("Alamat: "))
        elif pilihan == '3':
            produk.tampilkan()
        elif pilihan == '4':
            produk.tambah(input("ID Produk: "), input("Nama: "),
                          input("Jenis: "), int(input("Harga: ")))
        elif pilihan == '5':
            transaksi.tampilkan()
        elif pilihan == '6':
            transaksi.tambah(input("ID Transaksi: "), input(
                "ID Produk: "), int(input("Jumlah: ")))
        elif pilihan == '7':
            struk.tampilkan(input("ID Transaksi: "))
        elif pilihan == '8':
            struk.tambah(input("ID Transaksi: "), int(
                input("Total Harga: ")), input("NIK Pegawai: "))
        elif pilihan == '9':
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

    db.close()


if __name__ == "__main__":
    main_menu()
