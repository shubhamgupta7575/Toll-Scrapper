import tkinter as tk
from routeScrapper import routeScrapper
from tollRouteCoordinatesDB import tollRouteCoordinatesDB
from tollListDB import tollListDB
from tollPriceDB import tollPriceDB
from tollFinder import tollFinder
from tollScrapper import tollScrapper
from tollVisit import tollVisit

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

root.geometry('450x300')
root.title('Toll Scrapper')

# result = tk.Label(text='STEP-1 : ', bg="green", fg="white")
# result.place(x=10,y=10)
routefinderbutton = tk.Button( text='Download Vehicle Location Data')
routefinderbutton["command"] = routeScrapper
routefinderbutton.place(x=10, y=0)

tollbutton = tk.Button(text='Insert Vehicle Location Data')
tollbutton["command"] = tollRouteCoordinatesDB
tollbutton.place(x=10, y=30)

tollListbutton = tk.Button(text='Insert Manually Data(Toll List)')
tollListbutton["command"] = tollListDB
tollListbutton.place(x=10, y=60)

tollPricebutton = tk.Button(text='Insert Manually Data(Toll Price)')
tollPricebutton["command"] = tollPriceDB
tollPricebutton.place(x=10, y=90)

tollfinderbutton = tk.Button(text='Toll Finder')
tollfinderbutton["command"] = tollFinder
tollfinderbutton.place(x=10, y=120)

tollscapperbutton = tk.Button(text='Load FastTag Data')
tollscapperbutton["command"] = tollScrapper
tollscapperbutton.place(x=10,y=150)

tollDiscrepanciesButton = tk.Button(text='Find Discrepancies')
tollDiscrepanciesButton["command"] = tollVisit
tollDiscrepanciesButton.place(x=10,y=180)


quit = tk.Button(text="QUIT", fg="red",command=root.destroy)
quit.place(x=10, y=230)

# result = tk.Label(text='RESULT : ', bg="green", fg="white")
# result.place(x=10,y=180)
# result = tk.Label(text='xxxx')
# result.place(x=80,y=180)

root.mainloop()


