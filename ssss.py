from stegano import lsb
qp = lsb.hide('Abstract1.png', "Hello World")
qp.save('Abstract11.png')
clear_message = lsb.reveal( r"Abstract11.png")
print(clear_message)