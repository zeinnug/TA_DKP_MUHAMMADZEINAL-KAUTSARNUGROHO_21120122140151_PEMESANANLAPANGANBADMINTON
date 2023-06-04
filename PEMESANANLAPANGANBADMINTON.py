from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from queue import Queue
from datetime import date, datetime
from tkcalendar import Calendar


# Class untuk mengelola data lapangan
class Lapangan:
    def __init__(self, nama):
        self.nama = nama
        self.is_booked = False

    def book(self):
        self.is_booked = True

    def cancel_booking(self):
        self.is_booked = False


# Class untuk mengelola GUI
class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Program Pemesanan Lapangan")


        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 500
        window_height = 400
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.username = "zein"
        self.password = "admin"
        self.logged_in = False

        self.create_login_page()

        self.lapangan_list = [Lapangan("Lapangan Edoras"), Lapangan("Lapangan Bersama"), Lapangan("Lapangan Gladius"),
                              Lapangan("Lapangan Vention"), Lapangan("Lapangan Antimen")]
        self.lapangan_queue = Queue()
        self.daftar_pemesanan = []
        self.current_date = date.today()
        self.daftar_pemesanan_window = None
        self.listbox_pemesanan = None

    # Membuat halaman login
    def create_login_page(self):
        self.clear_window()

        self.label_username = Label(self.root, text="Username:")
        self.label_username.pack()
        self.entry_username = Entry(self.root)
        self.entry_username.pack()

        self.label_password = Label(self.root, text="Password:")
        self.label_password.pack()
        self.entry_password = Entry(self.root, show="*")
        self.entry_password.pack()

        self.button_login = Button(self.root, text="Login", command=self.login, bg = "orange")
        self.button_login.pack()

        self.button_exit = Button(self.root, text="Exit", command=self.exit_program, bg = "orange")
        self.button_exit.pack()

    # Membuat halaman utama pemesanan lapangan
    def create_main_page(self):
        self.clear_window()

        self.label_program_name = Label(self.root, text="ZEIN'S COURT")
        self.label_program_name.pack()

        self.label_lapangan = Label(self.root, text="Daftar Lapangan")
        self.label_lapangan.pack()

        self.combobox_lapangan = ttk.Combobox(self.root, values=self.get_lapangan_names())
        self.combobox_lapangan.pack()

        self.label_tanggal = Label(self.root, text="Tanggal:")
        self.label_tanggal.pack()

        self.entry_tanggal = Entry(self.root)
        self.entry_tanggal.pack()

        self.button_pilih_tanggal = Button(self.root, text="Pilih Tanggal", command=self.show_calendar, bg = "orange")
        self.button_pilih_tanggal.pack()

        self.label_waktu = Label(self.root, text="Waktu:")
        self.label_waktu.pack()

        self.combobox_waktu = ttk.Combobox(self.root, values=["7:00 - 9:00", "9:30 - 11:30", "13:00 - 16:00", "19:00 - 23:00"])
        self.combobox_waktu.pack()

        self.label_nama = Label(self.root, text="Nama Pemesan:")
        self.label_nama.pack()

        self.entry_nama = Entry(self.root)
        self.entry_nama.pack()

        self.label_telepon = Label(self.root, text="Nomor Telepon:")
        self.label_telepon.pack()

        self.entry_telepon = Entry(self.root)
        self.entry_telepon.pack()

        self.button_pesan = Button(self.root, text="Pesan", command=self.pesan_lapangan, bg = "orange")
        self.button_pesan.pack()

        self.button_lihat_daftar = Button(self.root, text="Lihat Daftar Pemesanan", command=self.lihat_daftar_pemesanan, bg = "orange")
        self.button_lihat_daftar.pack()


    # Membersihkan halaman
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Menampilkan pesan error
    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    # Menampilkan pesan sukses
    def show_success_message(self, message):
        messagebox.showinfo("Success", message)

    # Fungsi untuk login
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == self.username and password == self.password:
            self.logged_in = True
            self.create_main_page()
        else:
            self.show_error_message("Username atau password salah!")

    # Fungsi untuk keluar dari program
    def exit_program(self):
        self.root.quit()

    # Fungsi untuk mendapatkan nama-nama lapangan
    def get_lapangan_names(self):
        return [lapangan.nama for lapangan in self.lapangan_list]

    # Fungsi untuk memeriksa ketersediaan lapangan
    def is_lapangan_available(self, lapangan_name, tanggal, waktu):
        for pemesanan in self.daftar_pemesanan:
            if pemesanan["lapangan"] == lapangan_name and pemesanan["tanggal"] == tanggal and pemesanan["waktu"] == waktu:
                return False
        return True

    # Fungsi untuk memeriksa apakah tanggal melewati waktu real-time
    def is_valid_date(self, tanggal):
        now = datetime.now()
        selected_date = datetime.strptime(tanggal, "%Y-%m-%d")
        return selected_date.date() >= now.date()

    # Fungsi untuk memvalidasi nomor telepon
    def validate_telepon(self, nomor_telepon):
        if not nomor_telepon.isdigit():
            return False
        return len(nomor_telepon) == 12

    # Fungsi untuk memilih tanggal menggunakan kalender
    def show_calendar(self):
        top = Toplevel(self.root)
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack()

        def get_selected_date():
            selected_date = cal.get_date()
            if selected_date:
                self.entry_tanggal.delete(0, END)
                self.entry_tanggal.insert(END, selected_date)
            top.destroy()

        button_select = Button(top, text="Pilih", command=get_selected_date)
        button_select.pack()


    # Fungsi untuk memesan lapangan
    def pesan_lapangan(self):
        lapangan_name = self.combobox_lapangan.get()
        tanggal = self.entry_tanggal.get()
        waktu = self.combobox_waktu.get()
        nama_pemesan = self.entry_nama.get()
        nomor_telepon = self.entry_telepon.get()

        if not lapangan_name or not tanggal or not waktu or not nama_pemesan or not nomor_telepon:
            self.show_error_message("Harap isi semua field!")
            return

        if not self.is_valid_date(tanggal):
            self.show_error_message("Tanggal tidak valid!")
            return

        if not self.validate_telepon(nomor_telepon):
            self.show_error_message("Nomor telepon tidak valid!")
            return

        if not self.is_lapangan_available(lapangan_name, tanggal, waktu):
            self.show_error_message("Lapangan tidak tersedia pada tanggal dan waktu tersebut!")
            return

        self.daftar_pemesanan.append({
            "lapangan": lapangan_name,
            "tanggal": tanggal,
            "waktu": waktu,
            "nama_pemesan": nama_pemesan,
            "nomor_telepon": nomor_telepon
        })

        self.show_success_message("Pemesanan berhasil!")
        self.combobox_lapangan.set("")
        self.entry_tanggal.delete(0, END)
        self.combobox_waktu.set("")
        self.entry_nama.delete(0, END)
        self.entry_telepon.delete(0, END)

    # Fungsi untuk melihat daftar pemesanan
    # Fungsi untuk melihat daftar pemesanan
    def lihat_daftar_pemesanan(self):
        if self.daftar_pemesanan_window is not None and self.daftar_pemesanan_window.winfo_exists():
            return  # Jika window daftar pemesanan sudah ada, keluar dari fungsi

        self.daftar_pemesanan_window = Toplevel(self.root)
        self.daftar_pemesanan_window.title("Daftar Pemesanan")

        self.listbox_pemesanan = Listbox(self.daftar_pemesanan_window, width=50)
        self.listbox_pemesanan.pack()

        for i, pemesanan in enumerate(self.daftar_pemesanan, start=1):
            text = f"Nomor {i}\nLapangan: {pemesanan['lapangan']}\nTanggal: {pemesanan['tanggal']}\nWaktu: {pemesanan['waktu']}\nNama Pemesan: {pemesanan['nama_pemesan']}\nNomor Telepon: {pemesanan['nomor_telepon']}\n"
            self.listbox_pemesanan.insert(END, text)

        self.button_delete_pemesanan = Button(self.daftar_pemesanan_window, text="Hapus Pemesanan", command=self.delete_pemesanan)
        self.button_delete_pemesanan.pack()

    # Fungsi untuk menghapus pemesanan
    def delete_pemesanan(self):
        selected_item = self.listbox_pemesanan.curselection()[0]
        self.daftar_pemesanan.pop(selected_item)
        self.listbox_pemesanan.delete(selected_item)

        self.show_success_message("Pemesanan berhasil dihapus!")

    def run(self):
        self.root.mainloop()


root = Tk()
app = GUI(root)
app.run()
