import tkinter as tk

def setScale(w, h, s=1.5):
	st_width = w
	st_height = h
	st_scale = s

	root = tk.Tk()


	label1 = tk.Label(root, text="Please set scale")
	label1.pack()


	options = []

	i = 0.5
	while i <= 5:

		options.append(str(i) + ": \t" + str(int(i*st_width)) + "x" + str(int(i*st_height)))

		if i < 1.5:
			i += 0.25
		elif i < 3:
			i += 0.5
		else:
			i += 1

	ausgewaehlt = tk.StringVar()
	st = (str(st_scale) + ": \t" + str(int(st_scale*st_width)) + "x" + str(int(st_scale*st_height)))
	ausgewaehlt.set(st)

	for einzelwert in options:
		radiob = tk.Radiobutton(root, text=einzelwert, value=einzelwert, variable=ausgewaehlt)
		radiob.pack()

	schaltf1 = tk.Button(root, text="Apply", command=root.destroy)
	schaltf1.pack()

	root.mainloop()

	sp = ausgewaehlt.get()
	li = sp.split(':')

	return float(li[0])

"""
e = setScale(700,400,1.5)
print(e)
"""