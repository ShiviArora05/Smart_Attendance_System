import qrcode

name = input("Enter name: ")
qr = qrcode.make(name)
qr.save(f"{name}.png")
print("QR Code Generated")
