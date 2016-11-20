import cv2
from deteccion_bosque import DeteccionBosque
from Tkinter import Tk, BOTH, IntVar, StringVar, Label, Checkbutton, Entry
from ttk import Frame, Button, Style
from PIL import Image, ImageTk

class WindowMain(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.deteccion = DeteccionBosque()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Proyecto Guardian del Bosque")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.check_var1 = IntVar()
        self.check_var2 = IntVar()
        self.check_var3 = IntVar()
        self.path_video = StringVar()
        self.path_video1 = StringVar()
        lbl_title = Label(self, text="Proyecto Guardian del bosque")
        lbl_title.place(x=280, y=10)
        image = Image.open("images/img.png")
        photo = ImageTk.PhotoImage(image)
        lbl_image = Label(image=photo)
        lbl_image.image = photo
        lbl_image.place(x= 550, y=50)

        image1 = Image.open("images/img1.png")
        photo1 = ImageTk.PhotoImage(image1)
        lbl_image1 = Label(image=photo1)
        lbl_image1.image = photo1
        lbl_image1.place(x=50, y=300)

        lbl_path1 = Label(self, text="Ingrese la direccion de la primera imagen(actual): ")
        lbl_path1.place(x=20, y=50)
        entry_path1 = Entry(self, textvariable=self.path_video, width=60)
        entry_path1.place(x=20, y=80)

        lbl_path2 = Label(self, text="Ingrese la direccion de la segunda imagen(anterior): ")
        lbl_path2.place(x=20, y=110)

        entry_path2 = Entry(self, textvariable=self.path_video1, width=60)
        entry_path2.place(x=20, y=140)

        button_detect = Button(self, text="Detectar", command=self.detect, width=20)
        button_detect.place(x=60, y=180)

        button_quit = Button(self, text="Salir", command=self.quit, width=20)
        button_quit.place(x=280, y=180)

    def detect(self):
        path_image1 = self.path_video.get()
        path_image2 = self.path_video1.get()
        img1 = cv2.imread(path_image1)
        img2 = cv2.imread(path_image2)
        porcentaje_ganancia, porcentaje_perdida = self.deteccion.obtener_variacion(img1, img2)

        lbl_path3 = Label(self, text=" Porcentaje de ganancia: "+ str(porcentaje_ganancia))
        lbl_path3.place(x=20, y=650)
        lbl_path4 = Label(self, text=" Porcentaje de perdida: " + str(porcentaje_perdida))
        lbl_path4.place(x=20, y=680)
        image1 = Image.open("images/imgresultado.PNG")
        photo1 = ImageTk.PhotoImage(image1)
        lbl_image1 = Label(image=photo1)
        lbl_image1.image = photo1
        lbl_image1.place(x=50, y=210)

def main():
    root = Tk()
    root.geometry("700x700+800+800")
    app = WindowMain(root)
    root.mainloop()

if __name__ == "__main__":
    main()