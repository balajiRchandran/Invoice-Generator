from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ListProperty,StringProperty
from kivy.graphics import Color
from kivy.metrics import dp
from kivymd.font_definitions import theme_font_styles


KV='''
<Table>
    orientation:'vertical'  
    size_hint_y:0.95
    GridLayout:
        id:header
        spacing:2
        padding:[10,10,10,10]
        size_hint_y:None
        height:dp(28)
    ScrollView:
        size_hint_y:1       
        GridLayout:
            id:body
            spacing:2
            padding:[10,10,10,10]
            size_hint_y:None
            #spacing:dp(2)
            height:self.minimum_height
    BoxLayout:
        padding: 20
        orientation:'vertical'
        MDTextField:
            id: name
            hint_text: "Item Name"
            on_text: root.process1(self.text,'name')
        MDTextField:
            id: unit
            hint_text: "Unit Price"
            on_text: root.process1(self.text,'price')
        MDTextField:
            id:quan
            hint_text: "Quantity"
            on_text: root.process1(self.text,'quantity')
        MDTextField:
            id:tax
            hint_text: "Tax"
            on_text: root.process1(self.text,'tax')
        MDRaisedButton:
            pos_hint: {"center_x": .5}
            text: "Add Item"
            elevation_normal: 5
            md_bg_color: 1, 0, 1, 1
            on_press: root.addSingle()
        AnchorLayout:
            anchor_x:"right"
            anchor_y:"bottom"
            MDFloatingActionButton:
                icon:'arrow-right-bold'
                width: 40
                height: 40
                pos_hint: { "center_y": .9}
                text: "Generate Invoice"
                md_bg_color: app.theme_cls.primary_color
                on_press: app.print()
                        


<Header>
    padding:[10,10,10,10]
    canvas.before:
        Color:
            rgba: app.theme_cls.primary_light
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint_y:None
    size_hint_x:header.size_hint_x
    height:dp(28)
    MDLabel:
        halign:"center"
        id:header
        text:root.text
        font_style:"Body1"
<Cell>
    padding:[10,10,10,10]
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint_y:None
    size_hint_x:cell.size_hint_x
    height:dp(28)
    MDLabel:
        halign:"center"
        font_style:"Body2"
        id:cell
        text:root.text               
'''
Builder.load_string(KV)
class Header(BoxLayout):
    text = StringProperty()



class Cell(BoxLayout):
    text = StringProperty()




class Table(BoxLayout):
    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        self.check=False
        self.cols = NumericProperty(1)
        self.table_content = []
        self.thead = ListProperty()
        self.tbody = ListProperty()
        self.color = [128, 0, 2, 0.8]
        self.tempItem=dict()
        self.thead=["Item","Quan","Price","Tax"]
        self.ids['header'].cols = len(self.thead)
        self.ids['body'].cols = len(self.thead)
        for i in self.thead:
            head = Header(text=i)
            self.ids['header'].add_widget(head)

    def process1(self,val,cat):
        if cat=="name":
            self.tempItem["name"]=val
        elif cat=="price":
            self.tempItem["price"]=val
        elif cat=="tax":
            self.tempItem["tax"]=val
        elif cat=="quantity":
            self.tempItem["quantity"]=val

    def addSingle(self):
        self.ids['header'].clear_widgets()
        self.ids['body'].clear_widgets()
        self.table_content.append({"Item":self.tempItem["name"],"Quan":self.tempItem["quantity"],"Price":self.tempItem["price"],"Tax":self.tempItem["tax"]})
        for i in self.table_content:
            self.thead =[]
            for j in i.keys():
                self.thead.append(j)
        #self.thead=["ITEM","QUANTITY","UNIT PRICE","TAX"]
        self.ids['header'].cols = len(self.thead)
        self.ids['body'].cols = len(self.thead)
        for i in self.thead:
            head = Header(text=i)
            self.ids['header'].add_widget(head)
        for i in self.table_content:
            for j in i.keys():
                body = Cell(text=i[j])
                self.ids['body'].add_widget(body)
        self.ids['name'].text=""
        self.ids['quan'].text=""
        self.ids['unit'].text=""
        self.ids['tax'].text=""

