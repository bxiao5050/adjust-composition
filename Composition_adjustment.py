import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


def main():
    root = tk.Tk()
    root.title('composition adjustment')
    # app = Myslide(root)
    app = Composition_adjust(root)
    app.pack()

    root.mainloop()



#contain a scale, a spinbox and a entry
class Myslide(ttk.Frame):
    def __init__(self, master, ele_name = '', per = 10, power = 34):
        super().__init__(master)
        self.ini_per = per
        self.ini_power = power

        self.per_var = tk.DoubleVar(value=0.) # for scale and percentage
        self.power_var = tk.DoubleVar(value=0.)

        self.per_var.set(self.ini_per)
        self.power_var.set(self.ini_power)

        #scale
        f_slide = tk.LabelFrame(self, text = ele_name, fg = 'blue')
        self.slide = tk.Scale(f_slide, variable=self.per_var, orient='vertical', length=700, command = self.callback_slide, resolution  = 0.1, showvalue = 0, from_ = 90, to = 0.1)
        self.slide.pack()

        #power
        f_power = ttk.LabelFrame(self, text = 'power')

        self.power_spin = tk.Label(f_power, text = round(self.power_var.get(),1), width = 8)
        self.power_spin.pack()

        #percentage
        f_perl = ttk.LabelFrame(self, text = 'per')
        self.per_spin = tk.Spinbox(f_perl, textvariable = self.per_var, wrap=True, width=6, command = self.callback_slide, increment  = 0.1, from_=0.1, to=90,state='readonly', fg = 'red')
        self.per_spin.pack()

        # ttk.Entry(self, width = 3).grid(row = 0, column = 0, sticky = 'news')
        f_slide.grid(row = 1, column = 0, sticky = 'news')
        f_power.grid(row = 2, column = 0, sticky = 'news')
        f_perl.grid(row = 3, column = 0, sticky = 'news')


    def callback_slide(self, e=''):
        self.power_var.set(self.per_var.get()*self.ini_power/self.ini_per)
        self.power_spin.config(text = round(self.power_var.get(),1), width = 8)

    def set_value(self, value):
        self.input_var.set(value)


class Composition_adjust(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.f_ele = tk.Frame(self) # for element panel
        self.elements = [One_ele(self.f_ele, text = f'Nr. {i+1}', fg = 'blue') for i in range (2)]# all elments

        for e in self.elements:
            e.pack(side = 'left', padx = (10,10), pady = (10,10))

        self.f_ele.grid(row = 0, column = 0)
        tk.Button(self, text = '>>', command = self.on_more_ele).grid(row = 0, column =1, padx = (10,10))
        tk.Button(self, text = 'next', fg = 'red', command = self.on_next).grid(row = 1, column = 0, padx = (5,5), pady = (5,5))
    #override
    def callback_slide(self, e, slide, slides):
        #refresh the current power
        slide.power_var.set(slide.per_var.get()*slide.ini_power/slide.ini_per)
        slide.ini_power = slide.power_var.get()
        slide.ini_per = slide.per_var.get()
        #re-calculate the per for others
        summ = sum([s.per_var.get() for s in slides if s is not slide])

        for s in slides:
            if s is not slide:
                s.ini_power = s.power_var.get()
                s.ini_per = s.per_var.get()
            s.power_spin.config(text = round(s.power_var.get(),1), width = 8)

        #update the summation results
        self.per_total.config(text = round(sum([s.per_var.get() for s in slides]),1))
    # new window
    def on_next(self):
        try:
            w = tk.Toplevel(self)
            w.title(f'Composition and power')
            ele_f = tk.Frame(w) # frame for scales
            inf_f = tk.LabelFrame(w, text = 'summation of all percentages:') # for information panel
            ele_f.pack()
            inf_f.pack()
            slides = []
            for ele in self.elements:
                ele_name = ele.ele_name.get()
                per = float(ele.ele_per.get())
                power = float(ele.ele_power.get())
                slides.append(Myslide(ele_f, ele_name, per, power))
                slides[-1].pack(side = 'left', padx = (10,10), pady = (10, 10))

            self.per_total = tk.Label(inf_f, fg = 'blue', text = sum([slide.per_var.get() for slide in slides]))
            self.per_total.pack()

            for slide in slides:
                slide.per_spin.config(command = lambda e='', slide=slide, slides=slides:self.callback_slide(e, slide, slides))
                slide.slide.config(command = lambda e='', slide=slide, slides=slides:self.callback_slide(e, slide, slides))
                slide.slide.bind("<ButtonRelease-1>", lambda e = '',slides = slides: self.on_release(e, slides))
                slide.per_spin.bind("<ButtonRelease-1>", lambda e = '',slides = slides: self.on_release(e, slides))
        except:
            messagebox.showerror("showerror", "Give right values")


    
    #release the mouse
    def on_release(self, e, slides):
        summ = sum([s.per_var.get() for s in slides])
        for s in slides:
            s.per_var.set(s.per_var.get()/summ*100)
            s.ini_power = s.power_var.get()
            s.ini_per = s.per_var.get()
            # s.per_spin.config(text = round(s.power_var.get(),1), width = 8)
        #update the summation results
        self.per_total.config(text = round(sum([s.per_var.get() for s in slides]),1)) 
            
    def on_more_ele(self):
        self.elements.append(One_ele(self.f_ele, text = f'Nr. {len(self.elements)+1}', fg = 'blue'))
        self.elements[-1].pack(side = 'left', padx = (10,10))



    def callback_slide(self, e, slide, slides):
        #refresh the current power
        slide.power_var.set(slide.per_var.get()*slide.ini_power/slide.ini_per)
        slide.ini_power = slide.power_var.get()
        slide.ini_per = slide.per_var.get()
        #re-calculate the per for others
        summ = sum([s.per_var.get() for s in slides if s is not slide])

        for s in slides:
            if s is not slide:
                s.ini_power = s.power_var.get()
                s.ini_per = s.per_var.get()
            s.power_spin.config(text = round(s.power_var.get(),1), width = 8)

        #update the summation results
        self.per_total.config(text = round(sum([s.per_var.get() for s in slides]),1))







class One_ele(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        lf1 = ttk.LabelFrame(self, text = 'element:')
        lf2 = ttk.LabelFrame(self, text = 'power:')
        lf3 = ttk.LabelFrame(self, text = 'percentage:')

        self.ele_name = ttk.Entry(lf1, width = 9)
        self.ele_power = ttk.Entry(lf2, width = 9)
        self.ele_per = ttk.Entry(lf3, width = 9)

        self.ele_name.pack(pady = (5,5))
        self.ele_power.pack(pady = (5,5))
        self.ele_per.pack(pady = (5,5))

        lf1.pack()
        lf2.pack()
        lf3.pack()







if __name__ == '__main__':
    main()
