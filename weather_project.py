import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import*
import time
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
import mysql.connector

master = tk.Tk()
master.title("Weather App")
master.geometry("950x550+350+250")
master.resizable(False, False)

# Function to store weather in the database
def store_weather_in_db(city, wind, pressure, humidity, description):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jee1130@",
            database="weather_data"
        )
        cursor = conn.cursor()
        sql = "INSERT INTO weather (city, wind, pressure, humidity, description) VALUES (%s, %s, %s, %s, %s)"
        val = (city, wind, pressure, humidity, description)
        cursor.execute(sql, val)
        conn.commit()
        print("Weather data inserted successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Function to fetch weather data
def getweather():
    #try:
        city = textfield.get()
        if not city:
            raise ValueError("City cannot be empty")

        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)

        #if location is None:
         #   raise ValueError(f"City '{city}' not found.")

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        #if result is None:
         #   raise ValueError("Could not find timezone for the location.")

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")


        #api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=YOUR_API_KEY"

        api_key = "5f122db340bb4a0617eccd816cce8ca8"
        api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        #api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=5f122db340bb4a0617eccd816cce8ca8"
        json_data = requests.get(api).json()

       # if json_data.get("cod") != 200:
        #    raise ValueError(f"Error fetching weather data: {json_data.get('message', 'Unknown error')}")

        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        t.config(text=(temp, "°"))
        c.config(text=(condition, "|", "FEELS", "LIKE", temp, "°"))
        w.config(text=wind)
        h.config(text=humidity)
        d.config(text=description)
        p.config(text=pressure)

        store_weather_in_db(city, wind, pressure, humidity, description)

   # except ValueError as ve:
    #    messagebox.showerror("Weather App", str(ve))

    #except Exception as e:
     #   messagebox.showerror("Weather App", f"An error occurred: {str(e)}")

# Function to retrieve and display weather data from the database
def show_weather_table():
    weather_frame.pack_forget()  # Hide the weather frame
    table_frame.pack(fill="both", expand=1)  # Show the table frame

    # Clear existing data in the table
    for row in tree.get_children():
        tree.delete(row)

    # Fetch data from the database
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jee1130@",
            database="weather_data"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT city, wind, pressure, humidity, description FROM weather")  # Fetch all records
        records = cursor.fetchall()

        for i, (city, wind, pressure, humidity, description) in enumerate(records):
            tree.insert("", "end", values=(city, wind, pressure, humidity, description))
    
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Function to return to the weather app frame
def return_to_weather_app():
    table_frame.pack_forget()  # Hide the table frame
    weather_frame.pack(fill="both", expand=1)  # Show the weather frame

# Function to verify login
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "jeeva" and password == "123":
        messagebox.showinfo("Login", "Login Successful!")
        show_weather_app()  
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# Function to display the weather app
def show_weather_app():
    login_frame.pack_forget()  # Hide login frame
    weather_frame.pack(fill="both", expand=1)  # Show the weather app

# Function to display the login page
def show_login_page():
    weather_frame.pack_forget()  # Hide weather frame
    login_frame.pack(fill="both", expand=1)  # Show the login frame

# Login Frame
login_frame = tk.Frame(master, bg="lemon chiffon")

username_label = tk.Label(login_frame, text="Username", font=("Arial", 14), bg="lemon chiffon")
username_label.pack(pady=10)
username_entry = tk.Entry(login_frame, font=("Arial", 14))
username_entry.pack(pady=10)

password_label = tk.Label(login_frame, text="Password", font=("Arial", 14), bg="lemon chiffon")
password_label.pack(pady=10)
password_entry = tk.Entry(login_frame, show="*", font=("Arial", 14))
password_entry.pack(pady=10)

login_button = tk.Button(login_frame, text="Login", command=login, font=("Arial", 14), bg="spring green2")
login_button.pack(pady=20)

# Weather Frame
weather_frame = tk.Frame(master, bg="linen")

# Menu Bar in Weather Frame
menu_bar = tk.Menu(master)
master.config(menu=menu_bar)

weather_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Menu", menu=weather_menu)
weather_menu.add_command(label="Show Weather Table", command=show_weather_table)
weather_menu.add_command(label="Return to Weather App", command=return_to_weather_app)


# Search box
search_image = tk.PhotoImage(file="Copy of search.png")
myimage = tk.Label(weather_frame, image=search_image,bg="linen")
myimage.place(x=25, y=20)

textfield = tk.Entry(weather_frame, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

search_icon = tk.PhotoImage(file="Copy of search_icon.png")
myimage_icon = tk.Button(weather_frame, image=search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getweather)
myimage_icon.place(x=400, y=34)

# Logo
logo_image = tk.PhotoImage(file="Copy of logo.png")
logo = tk.Label(weather_frame, image=logo_image,bg="linen")
logo.place(x=150, y=110)

# Bottom box
frame_image = tk.PhotoImage(file="Copy of box.png")
frame_myimage = tk.Label(weather_frame, image=frame_image,bg="linen")
frame_myimage.pack(padx=5, pady=5, side=tk.BOTTOM)

# Time display
name = tk.Label(weather_frame, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = tk.Label(weather_frame, font=("Helvetica", 20))
clock.place(x=30, y=130)

# Labels for weather parameters
label1 = tk.Label(weather_frame, text="WIND", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label1.place(x=120, y=450)

label2 = tk.Label(weather_frame, text="HUMIDITY", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label2.place(x=250, y=450)

label3 = tk.Label(weather_frame, text="DESCRIPTION", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label3.place(x=430, y=450)

label4 = tk.Label(weather_frame, text="PRESSURE", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
label4.place(x=650, y=450)

# Weather display
t = tk.Label(weather_frame, font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = tk.Label(weather_frame, font=("arial", 15, "bold"))
c.place(x=400, y=250)

w = tk.Label(weather_frame, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=480)
h = tk.Label(weather_frame, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=480)
d = tk.Label(weather_frame, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=430, y=480)
p = tk.Label(weather_frame, text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=480)



# Weather Table Frame
table_frame = tk.Frame(master)


# Treeview to display the weather data
tree = ttk.Treeview(table_frame, columns=("City", "Wind", "Pressure", "Humidity", "Description"), show="headings")
tree.heading("City", text="City")
tree.heading("Wind", text="Wind")
tree.heading("Pressure", text="Pressure")
tree.heading("Humidity", text="Humidity")
tree.heading("Description", text="Description")
scrol=Scrollbar(table_frame,command=tree.yview)
scrol.pack(side=RIGHT,fill=Y)

tree.pack(fill="both", expand=True)

# Initially show login page
show_login_page()

master.mainloop()