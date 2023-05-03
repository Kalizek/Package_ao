import win32print
import win32ui
from PIL import Image, ImageWin

PHYSICALWIDTH = 110
PHYSICALHEIGHT = 111

printer_name = win32print.GetDefaultPrinter ()
file_name = "new.jpg"

hDC = win32ui.CreateDC ()
hDC.CreatePrinterDC (printer_name)
printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)

bmp = Image.open (file_name)

hDC.StartDoc (file_name)
hDC.StartPage ()

dib = ImageWin.Dib (bmp)
dib.draw (hDC.GetHandleOutput (), (0,0,printer_size[0],printer_size[1]))

hDC.EndPage ()
hDC.EndDoc ()
hDC.DeleteDC ()