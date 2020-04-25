from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from MyTable import Table
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDSeparator
from sqlite3 import *
import requests
import json as jso
import datetime
import threading 
from kivytoast import toast
import sys
from kivy.core.window import Window

c=connect("invoice.db")
cur=c.cursor()
cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='records' ''')
if cur.fetchone()[0]==0 : {
	cur.execute('''create table records(id char(20),name char(50),due date,amount char(10))''')
}
Builder.load_string('''
<First>:
    BoxLayout:
        orientation:'vertical'

        MDToolbar:
            title: 'Invoice Generator'
            left_action_items: [["arrow-left", lambda x: app.callback()]]

        MDBottomNavigation:
            panel_color: .9, .9, .9, 1
            MDBottomNavigationItem:
                name: 'Customer'
                text: 'Add'
                icon: 'sticker-plus-outline'
                BoxLayout:
                    pos_hint: {"center_x": .5, "center_y": .5}
                    padding: 20
                    size_hint_y: None
                    height: self.minimum_height
                    orientation:'vertical'
                    MDTextField:
                        hint_text: "Name"
                        on_text: app.process(self.text,'name')
                    MDTextField:
                        hint_text: "Address"
                        on_text: app.process(self.text,'address')
                    MDTextField:
                        hint_text: "City"
                        on_text: app.process(self.text,'city')
                    MDTextField:
                        hint_text: "PIN Code"
                        on_text: app.process(self.text,'pin')
                    MDTextField:
                        hint_text: "Mail Id"
                        on_text: app.process(self.text,'mail')
                    MDTextField:
                        hint_text: "Phone"
                        on_text: app.process(self.text,'phone')
                    MDRaisedButton:
                        md_bg_color: 1, 0, 1, 1
                        elevation_normal: 5
                        text: "Next"
                        pos_hint: {"center_x": .5, "center_y": .5}
                        on_press: app.firstToSecond()
                        
                    

            MDBottomNavigationItem:
                name: 'screen 2'
                text: 'View'
                icon: 'database-search'
                on_tab_press: app.fetchData(self)

<Second>:
    BoxLayout:
        orientation:'vertical'
''')
class First(Screen):
    pass
class Second(Screen):
    pass
class Test(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "700"
        return self.sm
    
    def __init__(self, **kwargs):
        self.exit=False
        super().__init__(**kwargs)
        self.item=[]
        self.cust=dict()
        self.sm = ScreenManager()
        self.temp_first=First(name='first')
        self.sm.add_widget(self.temp_first)
        self.temp_sec=Second(name='second')
        self.bello=Table()
        self.temp_sec.add_widget(self.bello)
        self.sm.add_widget(self.temp_sec)
        self.person=dict()

    def fetchData(self,tab):
        tab.clear_widgets()
        cur.execute("SELECT id,name,due,amount FROM RECORDS")
        rows = cur.fetchall()
        rows.insert(0,["Inv No","Name","Due Date","Amount"])
        temp=ScrollView()
        root1=StackLayout(size_hint_y=None,spacing=0,orientation="lr-tb")
        root1.bind(minimum_height=root1.setter('height'))
        i=0
        for row in rows:
            for col in row:
                    if i==0:
                        root1.add_widget(MDLabel(text=str(col),height=30,size_hint_x=1/4,size_hint_y=None,halign="center",font_style="Body1"))
                    else:
                        root1.add_widget(MDLabel(text=str(col),height=30,size_hint_x=1/4,size_hint_y=None,halign="center",font_style="Body2"))
            if i==0:
                root1.add_widget(MDSeparator())
            i=i+1
        temp.add_widget(root1)
        tab.add_widget(temp)
        
    def changeExit(self):
        self.exit=False

    def firstToSecond(self):
        self.person["shipping"]=dict()
        self.person["shipping"]["name"]=self.cust["name"]
        self.person["shipping"]["address"]=self.cust["address"]
        self.person["shipping"]["city"]=self.cust["city"]
        self.person["shipping"]["pin"]=self.cust["pincode"]
        self.sm.current="second"
        self.sm.remove_widget(self.temp_first)
        self.temp_first=First(name="first")
        self.sm.add_widget(self.temp_first)
    
    def callback(self):
        if self.exit==False:
            toast("Press back again to exit")
            self.exit=True
            timer = threading.Timer(2.0, self.changeExit) 
            timer.start() 
        else:
            Window.close()
            sys.exit()

    def process(self,val,cat):
        if cat=="name":
            self.cust['name']=val
        elif cat=="address":
            self.cust['address']=val
        elif cat=="city":
            self.cust['city']=val
        elif cat=="pin":
            self.cust['pincode']=val
        elif cat=="phone":
            self.cust['phone']=val
        elif cat=="mail":
            self.cust['emid']=val

    def gotohome(self):
        self.sm.current="first"
        self.sm.remove_widget(self.temp_sec)
        self.temp_sec=Second(name="second")
        self.temp_sec.clear_widgets()
        self.temp_sec.add_widget(Table())
        self.sm.add_widget(self.temp_sec)

    def print(self):
        self.person["items"]=self.bello.table_content
        t=str(datetime.datetime.now())
        t=(((t[2:].replace('-','')).replace(' ','')).replace(':','')).split('.')[0]
        self.person["invoice_nr"]=t
        self.person["cmail"]=self.cust["emid"]
        tot=0
        i=0
        for sin in self.person["items"]:
            sin_cost=float(sin["Price"])*float(sin["Quan"])
            sin_tax=sin_cost*float(float(sin["Tax"])/100)
            tot=tot+sin_cost+sin_tax
            self.person["items"][i]["taxamnt"]=str(sin_tax)
            self.person["items"][i]["line"]=str(sin_tax+sin_cost)
            i=i+1
        self.person["due"]=str(tot)
        js=jso.dumps(self.person)
        r=requests.get('https://invoice-3po.herokuapp.com/postdata', json={"data":js},allow_redirects=True)
        print(r)
        toast('Invoice Generated and Mail sent!')
        open('invoice.pdf', 'wb').write(r.content)
        query='insert into records values("'+t+'","'+self.person["shipping"]["name"]+'","'+str(datetime.datetime.now()+datetime.timedelta(days=10))[0:10]+'","'+str(tot)+'")'
        print(query)
        cur.execute(query)
        c.commit()
        timer = threading.Timer(2.0, self.gotohome) 
        timer.start() 
        

        
Test().run()
