from tkinter.scrolledtext import*
import matplotlib.pyplot as plt
from tkinter.messagebox import*
from tkinter import*
from sqlite3 import*
import pandas as pd
import requests
import bs4


#to get location
def loc():
    try:
        res = requests.get("https://ipinfo.io/")
        data=res.json()
        city_name=data['city']
    except Exception as e:
        print("issue: ",e)
    return city_name

#to get temperature
def temp():
    try:
         
        a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
        a2 = "&q=" + loc()        
        a3 = "&appid=c6e315d09197cec231495138183954bd"
        api_address =  a1 + a2  + a3
        res=requests.get(api_address)  
        data=res.json()
        loc_temp=data['main']['temp']
    except Exception as e:
        print("Temp issue ",e)
    return loc_temp


        
# to give input for qotd

def qotd():
    try:
        res=requests.get("https://www.brainyquote.com/quote_of_the_day")
        soup=bs4.BeautifulSoup(res.text,"lxml")
        data=soup.find('img',{'class':'p-qotd'})
        msg=data['alt']
    except Exception as e:
        print(" Quote Error ",e)
    
    return msg

#show adst window   
def adst_window(type):
    if type == 1:
        adst.title("Add Student Details")  
        adst.configure(background="Light Blue")
        lblrno.configure(bg="Light Blue")
        lblname.configure(bg="Light Blue")
        lblmarks.configure(bg="Light Blue")
        btnsave.configure(command=add_stu)
        
    else:
        adst.title("Update Student Details") 
        adst.configure(background="khaki1")
        lblname.configure(bg="khaki1")
        lblrno.configure(bg="khaki1")
        lblmarks.configure(bg="khaki1")
        btnsave.configure(command=up_stu)
        
    adst.deiconify()
    root.withdraw()
    
    
#to show delete window
def del_window():
    dlt.deiconify()
    root.withdraw()

#show root window when adst window is on
def root_window1():
    root.deiconify()
    adst.withdraw()
    
#show root window when view window is on
def root_window2():
    root.deiconify()
    view.withdraw()
    
#show root window when delete window is on
def root_window3():
    root.deiconify()
    dlt.withdraw()
    
    
#function to add student data

def add_stu():
    con=None
    try:
        con=connect("test.db")
        print("connected")
        rno= int(entrno.get())
        if rno<=0:
            showerror("Invalid Roll No.","Enter Valid Roll Number")
            entrno.delete(0,END)
            entname.delete(0,END)
            entmarks.delete(0,END)
            entrno.focus()    #to clear the entered data from widget
            return   #does not save the data if error occurs
        name=entname.get()
        if len(name)<2:
            showerror("Invalid Name", "Name should atleast have 2 letters")
            entrno.delete(0,END)
            entname.delete(0,END)
            entmarks.delete(0,END)
            entrno.focus()
            return
        if name.isdigit():
            showerror("Invalid Entry","Name should consists of letters")
            entrno.delete(0,END)
            entname.delete(0,END)
            entmarks.delete(0,END)
            entrno.focus()
            return
        marks=int(entmarks.get())
        if marks<=0 or marks>100:
            showerror("Invalid Marks", "Marks should be in range of 0-100")
            entmarks.delete(0,END)
            return
        args=(rno,name,marks)
        cursor=con.cursor()
        sql="insert into student values('%d','%s','%d')"
        cursor.execute(sql%args)
        con.commit()
        showinfo("Success","Details Saved")
        entrno.delete(0,END)
        entname.delete(0,END)
        entmarks.delete(0,END)
        entrno.focus()
    except ValueError:
        showerror("Invalid","Enter Valid Details")
        con.rollback()
    except Exception as e:
        if "UNIQUE" in str(e):
            showerror("Invalid","Roll No. already exists")
        else:
            showerror("failure", "insert issue "+str(e))
            con.rollback()
    
    finally:
        if con is not None:
            con.close()
            print("disconnected ")
            
#function to view student data

def view_stu():
    stdata.delete(1.0,END)
    view.deiconify()
    root.withdraw()
    con=None
    try:
        con=connect("test.db")
        print("connected")
        cursor=con.cursor()
        sql="select * from student"
        cursor.execute(sql)
        data=cursor.fetchall()
        info=""
        for d in data:
            info=info+"rno: "+str(d[0])+"  name: "+str(d[1])+"  marks :"+str(d[2])+"\n"
        stdata.insert(INSERT,info)
    except Exception as e:
        showerror("Failure","Selection Issue "+str(e))
        print("selection issue ",e)
    finally:
        if con is not None:
            con.close()
            print("disconnected")

def up_stu():
    con=None
    try:
        con=connect("test.db")
        print(entrno.get())
        rno=int(entrno.get())
        if rno<=0:
            showerror("Invalid Roll No.","Enter Valid Roll Number")
            entrno.delete(0,END)    
            return   
        print(entname.get())  
        name=entname.get()
        if len(name)<2:
            showerror("Invalid Name", "Name should atleast have 2 letters")
            entname.delete(0,END)
            return
        print(entmarks.get())
        marks=int(entmarks.get())
        if marks<=0 or marks>100:
            showerror("Invalid Marks", "Marks should be in range of 0-100")
            entmarks.delete(0,END)
            return      
        cursor=con.cursor()
        sql="update student set name='%s' ,  marks='%d' where rno='%d' "
        args=(name,marks,rno)
        cursor.execute(sql%args)
        if cursor.rowcount>=1:
            con.commit()
            showinfo("Success","Details Updated")
            entrno.delete(0,END)
            entname.delete(0,END)
            entmarks.delete(0,END)
            entrno.focus()
        else:
            showerror("Invalid","Enter Valid Data")
    except ValueError as e:
        print(e)
        showerror("Invalid","Enter Valid Details")
        con.rollback()
    except Exception as e:
        showerror("failure", "insert issue "+str(e))
        con.rollback()
    finally:
        if con is not None:
            con.close()
            print("disconnected")
            
#function to delete the student record

def del_stu():
    con=None
    try:
        con=connect("test.db")
        print("connected")
        rno=int(entdrno.get())
        if rno<=0:
            showerror("Invalid","Enter a valid Roll No.")
            entdrno.delete(0,END)
            entdrno.focus()
            return
        args=(rno)
        cursor=con.cursor()
        sql="delete from student where rno='%d'"
        cursor.execute(sql%args)
        if cursor.rowcount>=1:
            con.commit()
            showinfo("Success","Record Deleted")
            entdrno.delete(0,END)
            entdrno.focus()
        else:
            showerror("Invalid","Roll No. does not exists")
            entdrno.delete(0,END)
            entdrno.focus()
    except Exception as e:
        showerror("Failure", "Deletion issue " + str(e))
        con.rollback()
    finally:
        if con is not None:
            con.close()
            print("disconnected")
            
#Display the top five marks of student in charts format
def charts():
    con=connect("test.db")
    print("connected")
    cursor=con.cursor()
    
    sql="select name, marks from student "
    cursor.execute(sql)
    dbdata=cursor.fetchall()
    data=pd.DataFrame(dbdata,columns=['Name','Marks'])
    a1=data.sort_values(by="Marks",ascending=False)
    a2=a1.head()
    
    marks=a2['Marks'].tolist()
    name=a2["Name"].tolist()
    
    barlist=plt.bar(name,marks)
    barlist[0].set_color('r')
    barlist[1].set_color('g')
    barlist[2].set_color('b')
    barlist[3].set_color('r')
    barlist[4].set_color('g')
    plt.title("Batch Information")
    plt.ylabel("Marks")
    plt.show()


#design of root window--> Student Management System
'''
bg-->background color
anchor-->to adjust text at left, by default the text is adjusted in center
wraplength-->to have multiple lines
'''
root=Tk()
root.title("Student Management System")
root.geometry("500x600+400+300")
root.configure(background="Yellow Green")
root.resizable(width=0,height=0)

btnAdd=Button(root,text="ADD", font=("arial",15,"bold"),width=10, command=lambda:adst_window(1))
btnView=Button(root,text="VIEW",font=("arial",15,"bold"),width=10,command=view_stu)
btnUpdate=Button(root,text="UPDATE",font=("arial",15,"bold"),width=10,command=lambda:adst_window(3))
btnDelete=Button(root,text="DELETE",font=("arial",15,"bold"),width=10,command=del_window)
btnCharts=Button(root,text="CHARTS",font=("arial",15,"bold"),width=10,command=charts)
lblLocation=Label(root,text="Location: "+str(loc()),font=("arial",15),width=20,bg="Yellow Green",anchor="w")
lbltemp=Label(root,text="Temp: "+ str(temp()),font=("arial",15),width=10,bg="Yellow Green")
lblqotd=Label(root,text="QOTD: "+ str(qotd()),font=("arial",15),width=100,bg="Yellow Green",anchor="w",wraplength=450)
btnAdd.pack(pady=20)
btnView.pack(pady=20)
btnUpdate.pack(pady=20)
btnDelete.pack(pady=20)
btnCharts.pack(pady=20)
lblLocation.place(x=50,y=450)
lbltemp.place(x=300,y=450)
lblqotd.place(x=50,y=500)

#design of add student window

adst=Toplevel(root)
#adst.title("Add Student Details") 
adst.geometry("500x500")
adst.configure(background="Light Blue")
adst.resizable(width=0,height=0)
adst.withdraw()

lblrno=Label(adst,text="Enter Roll Number",font=("arial",15,"bold"))
entrno=Entry(adst,bd=5,font=("arial",15,"bold"))
entrno.focus()

lblname=Label(adst,text="Enter Name",font=("arial",15,"bold"))
entname=Entry(adst,bd=5,font=("arial",15,"bold"))

lblmarks=Label(adst,text="Enter Marks",font=("arial",15,"bold"))
entmarks=Entry(adst,bd=5,font=("arial",15,"bold"))

btnsave=Button(adst,text="Save",font=("arial",15,"bold"),width=10)
btnback=Button(adst,text="Back",font=("arial",15,"bold"),width=10, command=root_window1)

lblrno.pack(pady=10)
entrno.pack(pady=10)
lblname.pack(pady=10)
entname.pack(pady=10)
lblmarks.pack(pady=10)
entmarks.pack(pady=10)
btnsave.pack(pady=15)
btnback.pack(pady=10)

#design of view data window

view=Toplevel(root)
view.title("View Student Data")
view.geometry("500x500")
view.configure(background="bisque")
view.resizable(width=0,height=0)
view.withdraw()

stdata=ScrolledText(view,width=40,height=25)
btnback=Button(view,text="Back",font=("arial",15,"bold"),width=10,command=root_window2)

stdata.pack(pady=10)
btnback.pack(pady=10)

#design of delete window

dlt=Toplevel(root)
dlt.title("Delete Student Details")
dlt.geometry("500x500")
dlt.configure(background="light cyan")
dlt.resizable(width=0,height=0)
dlt.withdraw()

lbldrno=Label(dlt,text="Enter Roll Number",font=("arial",15,"bold"),bg="Light Cyan")
lbldrno.configure(bg="Light cyan")
entdrno=Entry(dlt,bd=5,font=("arial",15,"bold"))
entdrno.focus()
btndsave=Button(dlt,text="Save",font=("arial",15,"bold"),width=10,command=del_stu)
btndback=Button(dlt,text="Back",font=("arial",15,"bold"),width=10, command=root_window3)

lbldrno.pack(pady=20)
entdrno.pack(pady=10)
btndsave.pack(pady=20)
btndback.pack(pady=20)


root.mainloop()


