import tkinter as tk
import sqlite3
import datetime
import csv

kcal = 0
fats = 0
carbs = 0
proteins = 0

def create_sql_table():
   conn = sqlite3.connect('my_daily_macros.db')
   c = conn.cursor()
   c.execute("""CREATE TABLE IF NOT EXISTS products (
         name text PRIMARY KEY,
         kcal REAL,
         fats REAL,
         carbs REAL,
         proteins REAL  
         )""")
   conn.commit()
   conn.close()

create_sql_table()

def query_list():
   user_entry = entry_1.get()

   conn = sqlite3.connect('my_daily_macros.db')
   c = conn.cursor()
   c.execute("SELECT name FROM products WHERE name LIKE '%" + str(user_entry) + "%'")

   results_list = [i[0] for i in c.fetchall()]
   count_results = len(results_list)

   listbox = tk.Listbox(frame_left_2)
   listbox.config(relief='flat')
   listbox.option_add("*font", "arial 11")
   for x in range (1,count_results + 1):
      listbox.insert(x,results_list[x - 1]) #list elements index begins with 0 not 1
   listbox.place(relx=0.0, rely =0.0, relheight=1 ,relwidth=1)

   def curselect(event):

      listbox.bind('<<ListboxSelect>>')

      global picked
      try:
         picked = listbox.get(listbox.curselection())
      except:
         pass

   listbox.bind('<<ListboxSelect>>', curselect)
   #listbox.bind('<Double-Button>', curselect)

   conn.close()

def get_data_from_list():
   #check if product already is added to MyDay
   x = listbox2.size() + 1
   check3 = ''

   try:
      picked1 = picked
      for j in range(0, x):
         if str(picked).strip("'{}[](),") == str(listbox2.get(j)).strip("'{}[](),"):
            check3 = True
   except:
      pass

   check1 = 0
   check2 = 0

   #print(str(picked).strip("'{}[](),"))
   global current_product
   current_product = tk.StringVar()
   try:
      current_product = str(picked1).strip("'{}[](),")
   except:
      pass

   grams = 0

   try:
      grams = float(entry_2.get())
      check1 = 1
   except:
      check1 = 0

   try:
      if len(str(picked1)) > 0:
         check2 = 1
   except:
      check2 = 0

   if check1 != 0 and check2 != 0 and str(picked1).startswith('PY_VAR') != True and check3 != True:

      a = listbox2.size()
      b = listbox3.size()

      for x in range(a,a+1):
         listbox2.insert(x, picked1)  # list elements index begins with 0 not 1
         listbox2.place(relx=0.0, rely=0.0, relheight=1, relwidth=0.7)

      for x in range(b, b+1):
         listbox3.insert(x, grams)  # list elements index begins with 0 not 1
         listbox3.place(relx=0.7, rely=0.0, relheight=1, relwidth=0.3)

      entry_2.delete(0, tk.END)
      frame_left_err.place(relx=1) #beyond the main window screen, probably should be better way to do this.

   elif check3 == True:
      message_text = str(picked).strip("'{}[](),") + " has been already added to My Day"
      font_color = '#D74A4A'
      main_window_message(message_text, font_color)

   else:
      message_text = "please select product and provide it's weight"
      font_color = '#D74A4A'
      main_window_message(message_text, font_color)

def main_window_message(message_txt, font_color):
   frame_left_err.place(relx=0.1, rely=0.775, relheight=0.05, relwidth=0.375)
   label_mw_message.place(relx=0.0, rely=0.0, relheight=1, relwidth=1)
   label_mw_message.config(font=("Arial", 9), text=message_txt, fg=font_color)

def refresh():
   listbox2.delete(0,tk.END)
   listbox3.delete(0,tk.END)

def delete():
   listbox2.bind('<<ListboxSelect>>')

   if listbox2.size() > 0:
      n = listbox2.curselection()
      try:
         listbox2.delete(n)
         listbox3.delete(n)
         n = None
      except:
         pass

def calculate_macros():
   o = listbox2.size()

   global sum_kcal
   global sum_fats
   global sum_carbs
   global sum_proteins

   kcal_list=[]
   fats_list=[]
   carbs_list=[]
   proteins_list = []

   for x in range (0,o):

      # calculate kcal
      product_to_calc = str(listbox2.get(x)).strip("'{}[](),")

      conn = sqlite3.connect('my_daily_macros.db')
      c = conn.cursor()
      c.execute("SELECT kcal FROM products WHERE name='" + product_to_calc + "'")
      kcal = str(c.fetchall()).strip("'{}[](),")

      g = str(listbox3.get(x)).strip("'{}[](),")
      kcal_per_grams = float(kcal) * float(g) / 100
      kcal_list.append(kcal_per_grams)
      kcal_list = [float(i) for i in kcal_list]

      # calculate fats
      c.execute("SELECT fats FROM products WHERE name='" + product_to_calc + "'")
      fats = str(c.fetchall()).strip("'{}[](),")

      fats_per_grams = float(fats) * float(g) / 100
      fats_list.append(fats_per_grams)
      fats_list = [float(i) for i in fats_list]

      # calculate carbs
      c.execute("SELECT carbs FROM products WHERE name='" + product_to_calc + "'")
      carbs = str(c.fetchall()).strip("'{}[](),")

      carbs_per_grams = float(carbs) * float(g) / 100
      carbs_list.append(carbs_per_grams)
      carbs_list = [float(i) for i in carbs_list]

      # calculate proteins
      c.execute("SELECT proteins FROM products WHERE name='" + product_to_calc + "'")
      proteins = str(c.fetchall()).strip("'{}[](),")

      proteins_per_grams = float(proteins) * float(g) / 100
      proteins_list.append(proteins_per_grams)
      proteins_list = [float(i) for i in proteins_list]

   sum_kcal = int(round(sum(kcal_list),0))
   sum_fats = int(round(sum(fats_list),0))
   sum_carbs = int(round(sum(carbs_list),0))
   sum_proteins = int(round(sum(proteins_list),0))

   label_sum = tk.Label(frame_right_1,text="kcal: " + str(sum_kcal) + ";  fats: " + str(sum_fats)
                        + ";  carbs: " + str(sum_carbs) + ";  proteins:" + str(sum_proteins) ,anchor='w', background='#E9E9E9')
   label_sum.place(rely=0, relx=0, relheight=1, relwidth=0.8)

   button_save.place(relx=0.8, relheight=1, relwidth=0.1)

   button_csv.place(relx=0.9, relheight=1, relwidth=0.1)

def save():
   now = datetime.datetime.now()
   date = now.strftime("%Y %B %d")

   conn = sqlite3.connect('my_daily_macros.db')
   c = conn.cursor()
   c.execute("""CREATE TABLE IF NOT EXISTS archive (
          date text,
          kcal text,
          fats text,
          carbs text,
          proteins text  
          )""")
   conn.commit()

   c.execute("INSERT INTO archive (date, kcal, fats, carbs, proteins) VALUES (?, ?, ?, ?, ?)",
             (date, sum_kcal, sum_fats, sum_carbs, sum_proteins))
   conn.commit()
   conn.close()

def export_csv():
   conn = sqlite3.connect("my_daily_macros.db")
   c = conn.cursor()

   data = c.execute("SELECT * FROM archive")
   with open('file.csv', 'w', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(['date', 'kcal', 'fats', 'carbs', 'proteins'])
      writer.writerows(data)

   conn.close()

def handle_focus_in_entry_1(_):
   entry_1.delete(0, tk.END)
   entry_1.config(fg='black')

def handle_focus_in_entry_2(_):
   entry_2.delete(0, tk.END)
   entry_2.config(fg='black')

def new_window():
   global message_text
   global font_color

   def update_database():
      check_list = []

      conn = sqlite3.connect('my_daily_macros.db')
      c = conn.cursor()

      # Check if product exists in database
      c.execute("SELECT name FROM products WHERE name LIKE '%" + str(user_entry) + "%'")
      check_list = c.fetchall()
      items = len(check_list)

      check_before_update = False

      for i in range(0, items):
            if new_product_name.get() == str(check_list[i]).strip("'{}[](),"):
               check_before_update = True

      if check_before_update != True:
         message_text = 'Product not found, please add'
         font_color = '#D74A4A'
         new_window_message(message_text, font_color)
         return

      try:

         if new_product_name.get() != '' and new_kcal.get() != '' and new_fats.get() != '' and new_carbs.get() != '' and new_proteins.get() != '':

            conn = sqlite3.connect('my_daily_macros.db')
            c = conn.cursor()

            # Executing update
            c.execute("UPDATE products SET name = ?, kcal = ?, fats = ?, carbs = ?, proteins = ?  WHERE name = ? ",
                     (new_product_name.get(), new_kcal.get(), new_fats.get(), new_carbs.get(), new_proteins.get(),new_product_name.get()))
            conn.commit()

            message_text = new_product_name.get() + " has been updated"
            font_color = '#3A9349'
            new_window_message(message_text, font_color)

            refresh_new_window_entry()

         else:
            message_text = "please fill in all fields"
            font_color = '#D74A4A'
            new_window_message(message_text, font_color)
      except:
         message_text = "kcal, fats, carbs and proteints - should be numeric"
         font_color = '#D74A4A'
         new_window_message(message_text, font_color)

      conn.close()

   def refresh_new_window_entry():
      entry_nw_product_name.delete(0, tk.END)
      entry_nw_kcal.delete(0, tk.END)
      entry_nw_fats.delete(0, tk.END)
      entry_nw_carbs.delete(0, tk.END)
      entry_nw_proteins.delete(0, tk.END)

   def new_window_message(message_txt, font_color):
      frame_nw_3.place(relx=0.1, rely=0.6, relheight=0.125, relwidth=0.6)
      label_nw_message = tk.Label(frame_nw_3, text=message_txt,
                                  background='#E9E9E9',
                                  fg=font_color, anchor='w')
      label_nw_message.place(relx=0.0, rely=0.0, relheight=1, relwidth=1)

   def insert_data_in_sql_table():

      try:
         if new_product_name.get() != '' and new_kcal.get() != '' and new_fats.get() != '' and new_carbs.get() != '' and new_proteins.get() != '':

            conn = sqlite3.connect('my_daily_macros.db')
            c = conn.cursor()
            c.execute("INSERT INTO products (name, kcal, fats, carbs, proteins) VALUES (?, ?, ?, ?, ?)",
                    (new_product_name.get(), new_kcal.get(), new_fats.get(), new_carbs.get(), new_proteins.get()))
            conn.commit()

            message_text = new_product_name.get() + " has been added"
            font_color = "#3A9349"
            new_window_message(message_text, font_color)

            refresh_new_window_entry()

            conn.close()

         else:
            message_text = "please fill in all fields"
            font_color = '#D74A4A'
            new_window_message(message_text, font_color)

      except tk.TclError:
         message_text = "kcal, fats, carbs and proteints - should be numeric"
         font_color = '#D74A4A'
         new_window_message(message_text, font_color)

      except sqlite3.IntegrityError:
         message_text = new_product_name.get() + ' is already in database'
         font_color = '#D74A4A'
         new_window_message(message_text, font_color)

   global new_product_name
   global new_kcal
   global new_fats
   global new_carbs
   global new_proteins
   new_product_name = tk.StringVar()
   new_kcal = tk.DoubleVar()
   new_fats = tk.DoubleVar()
   new_carbs = tk.DoubleVar()
   new_proteins = tk.DoubleVar()

   new_window = tk.Toplevel(master=None)
   new_window.title("Add Product To Database")
   new_window.geometry("600x200")
   new_window.option_add( "*font", "arial 10" )

   canvas_nw = tk.Canvas(new_window, height=200, width=600)
   filename_nw = tk.PhotoImage(file='AppBackground_600x200.PNG')
   image = canvas_nw.create_image(600, 0, anchor='ne', image=filename_nw)
   canvas_nw.pack()

   frame_nw_1 = tk.Frame(new_window, bg='white')
   frame_nw_1.place(relx=0.1, rely =0.35, relheight=0.25 ,relwidth=0.8)

   label_nw_1 = tk.Label(frame_nw_1, text="Product name                                (per 100g):", background='#E9E9E9')
   label_nw_1.place(relx=0.0, rely =0.0, relheight=0.5 ,relwidth=0.6)
   entry_nw_product_name = tk.Entry(frame_nw_1, textvariable=new_product_name)
   entry_nw_product_name.config(relief='sunken', selectforeground='white', background='#F8F8F8')
   entry_nw_product_name.place(relx=0.0, rely=0.5, relheight=0.5 ,relwidth=0.6)

   label_nw_2 = tk.Label(frame_nw_1, text="kcal", background='#E9E9E9')
   label_nw_2.place(relx=0.6, rely=0.0, relheight=0.5, relwidth=0.1)
   entry_nw_kcal = tk.Entry(frame_nw_1, textvariable=new_kcal)
   entry_nw_kcal.config(relief='sunken', selectforeground='white', background='#F8F8F8')
   entry_nw_kcal.place(relx=0.6, rely=0.5, relheight=0.5, relwidth=0.1)

   label_nw_3 = tk.Label(frame_nw_1, text="fats", background='#E9E9E9')
   label_nw_3.place(relx=0.7, rely=0.0, relheight=0.5, relwidth=0.1)
   entry_nw_fats = tk.Entry(frame_nw_1, textvariable=new_fats)
   entry_nw_fats.config(relief='sunken', selectforeground='white', background='#F8F8F8')
   entry_nw_fats.place(relx=0.7, rely=0.5, relheight=0.5, relwidth=0.1)

   label_nw_4 = tk.Label(frame_nw_1, text="carbs", background='#E9E9E9')
   label_nw_4.place(relx=0.8, rely=0.0, relheight=0.5, relwidth=0.1)
   entry_nw_carbs = tk.Entry(frame_nw_1, textvariable=new_carbs)
   entry_nw_carbs.config(relief='sunken', selectforeground='white', background='#F8F8F8')
   entry_nw_carbs.place(relx=0.8, rely=0.5, relheight=0.5, relwidth=0.1)

   label_nw_5 = tk.Label(frame_nw_1, text="proteins", background='#E9E9E9')
   label_nw_5.place(relx=0.9, rely=0.0, relheight=0.5, relwidth=0.1)
   entry_nw_proteins = tk.Entry(frame_nw_1, textvariable=new_proteins)
   entry_nw_proteins.config(relief='sunken', selectforeground='white', background='#F8F8F8')
   entry_nw_proteins.place(relx=0.9, rely=0.5, relheight=0.5, relwidth=0.1)

   frame_nw_2 = tk.Frame(new_window, bg='#BDF2E7')
   frame_nw_2.place(relx=0.775, rely=0.60, relheight=0.125, relwidth=0.125)

   button_upd = tk.Button(frame_nw_2, anchor='w')
   button_upd.place(relx=0.0, relheight=1, relwidth=0.5)
   button_upd.config(command=update_database, image=photo_upd, bg='#E8E8E8', relief='flat')

   button_add_2 = tk.Button(frame_nw_2, anchor='w')
   button_add_2.place(relx=0.5, relheight=1, relwidth=0.5)
   button_add_2.config(command=insert_data_in_sql_table, image=photo_add_2, bg='#E8E8E8', relief='flat')

   frame_nw_3 = tk.Frame(new_window, bg='#E9E9E9')

   new_window.mainloop()

WIDTH = 1000
HEIGHT = 600

main_window = tk.Tk()
main_window.title("My Daily Macros")

main_window.option_add( "*font", "arial 11" )

canvas = tk.Canvas(main_window, height=HEIGHT, width=WIDTH)
filename = tk.PhotoImage(file='AppBackground_1000x600.PNG')
image = canvas.create_image(1000, 0, anchor='ne', image=filename)

canvas.pack()

frame_left_1 = tk.Frame(main_window, bg='#9FF9F9')
frame_left_1.place(relx=0.1, rely =0.35, relheight=0.05 ,relwidth=0.375)

user_entry = '' #tk.StringVar()
entry_1 = tk.Entry(frame_left_1, textvariable=user_entry)
entry_1.place(relx=0.0, relheight=1, relwidth=0.8)
entry_1.config(relief='sunken', fg='grey', selectforeground='white')
entry_1.insert(0, 'type product here and click search')
entry_1.bind("<FocusIn>", handle_focus_in_entry_1)

button_search = tk.Button(frame_left_1, text="Q", bg='white')
button_search.place(relx=0.8, relheight=1, relwidth=0.1)
photo_search = tk.PhotoImage(file="icons8-search-24.PNG")
button_search.config(command=query_list, image=photo_search, relief='flat')

button_add = tk.Button(frame_left_1, text="+", bg='white')
button_add.place(relx=0.9, relheight=1, relwidth=0.1)
photo_add = tk.PhotoImage(file="icons8-plus-24.PNG")
button_add.config(command=new_window, image=photo_add, relief='flat')

frame_left_2 = tk.Frame(main_window, bg='white')
frame_left_2.place(relx=0.1, rely =0.425, relheight=0.4 ,relwidth=0.375)

frame_left_3 = tk.Frame(main_window, bg='white')
frame_left_3.place(relx=0.1, rely =0.85, relheight=0.05 ,relwidth=0.375)

button_add_to_my_day = tk.Button(frame_left_3, text='>>>')
button_add_to_my_day.place(relx=0.9, relheight=1, relwidth=0.1)
photo_add_to_my_day=tk.PhotoImage(file="icons8-share-3-24.PNG")
button_add_to_my_day.config(command=get_data_from_list, image=photo_add_to_my_day, bg='white', relief='flat')

frame_left_err = tk.Frame(main_window, bg='grey')

label_mw_message = tk.Label(frame_left_err, background='#E9E9E9', anchor='center')

label_1 = tk.Label(frame_left_3, text="selected product weight [g]:")
label_1.place(relx=0.0, relheight=1, relwidth=0.5)

grams = ''
entry_2 = tk.Entry(frame_left_3, textvariable=grams)
entry_2.place(relx=0.5, relheight=1, relwidth=0.4)
entry_2.config(relief='sunken', fg='grey')
entry_2.insert(0, '100')

entry_2.bind("<FocusIn>", handle_focus_in_entry_2)

frame_right_1 = tk.Frame(main_window, bg='white')
frame_right_1.place(relx=0.5, rely =0.35, relheight=0.05 ,relwidth=0.375)

button_save = tk.Button(frame_right_1)
photo_save = tk.PhotoImage(file="icons8-save-close-24.PNG")
button_save.config(command=save, image=photo_save, bg='#E9E9E9', relief='flat')

button_csv = tk.Button(frame_right_1)
photo_csv = tk.PhotoImage(file="icons8-export-csv-24.PNG")
button_csv.config(command=export_csv, image=photo_csv, bg='#E9E9E9', relief='flat')

frame_right_2 = tk.Frame(main_window, bg='white')
frame_right_2.place(relx=0.5, rely =0.425, relheight=0.4 ,relwidth=0.375)

listbox2 = tk.Listbox(frame_right_2) #just definition
listbox2.config(relief='flat')
listbox2.option_add( "*font", "arial 11" )
listbox3 = tk.Listbox(frame_right_2) #just definition
listbox3.config(relief='flat')
listbox3.option_add( "*font", "arial 11" )

frame_right_3 = tk.Frame(main_window, bg='white')
frame_right_3.place(relx=0.5, rely =0.85, relheight=0.05 ,relwidth=0.375)

button_refresh = tk.Button(frame_right_3)
button_refresh.place(relx=0.0, relheight=1, relwidth=0.1)
photo_refresh=tk.PhotoImage(file="icons8-refresh-24b.PNG")
button_refresh.config(command=refresh, image=photo_refresh, bg='white', relief='flat')

button_delete = tk.Button(frame_right_3)
button_delete.place(relx=0.1, relheight=1, relwidth=0.1)
photo_delete=tk.PhotoImage(file="icons8-trash-24.PNG")
button_delete.config(command=delete, image=photo_delete, bg='white', relief='flat')

button_calc = tk.Button(frame_right_3, text='CALC', anchor ='w')
button_calc.place(relx=0.9, relheight=1, relwidth=0.2)
photo_calc=tk.PhotoImage(file="icons8-accounting-24.PNG")
button_calc.config(command=calculate_macros, image=photo_calc, bg='white', relief='flat')

photo_upd = tk.PhotoImage(file="icons8-refresh-24.PNG")
photo_add_2 = tk.PhotoImage(file="icons8-add-24a.PNG")

main_window.mainloop()