from bs4 import BeautifulSoup
import requests, re
import tkinter
import time


def load_page_source(link) :
    url = requests.get(link).text
    str_version = str(BeautifulSoup(url, 'lxml'))
    return str_version

def construct_search_url(search) :
    return ''.join(['https://www.marketbeat.com/pages/search.aspx?query=', search])

def scrape_search_results(page_source, tick) :
    search_results = [match.split('>')[-1][:-1] for match in re.findall('<div class=\"title-area\">[^<>]+<', page_source)]
    search_results_links = ['https://www.marketbeat.com'+match.split('"')[1]+'/' for match in re.findall('href=\"/stocks/[A-Z]+/'+tick, page_source)]
    final_results = list(zip(search_results, search_results_links))

    #I'm gonna change it so that the max results is 5
    #Never mind, do list

    return final_results

def locate_div(page_source) :
    results = re.findall('<div class=\'ticker-area\'>[A-Z]+', page_source)[0].split('>')[1]
    return results

def construct_page_url(ticker) :
    return ''.join(['https://www.marketbeat.com/stocks/',ticker, '/'])


def get_company_data(page_source) :
    start = time.time()
    to_retrieve = ['Stock Exchange', 'Industry', 'Sub-Industry', 'Sector', 'Current Symbol', 'Previous Symbol', 'CUSIP', 'CIK', 'Web', 'Phone', 'Employees', 'Year Founded',
                   'Debt-to-Equity Ratio', 'Current Ratio', 'Quick Ratio', 'Trailing P/E Ratio', 'Forward P/E Ratio', 'P/E Growth', 'Annual Sales', 'Price / Sales', 'Cash Flow',
                   'Price / Cash Flow', 'Book Value', 'Price / Book', 'EPS (Most Recent Fiscal Year)', 'Net Income', 'Net Margins', 'Return on Equity', 'Return on Assets',
                   'Outstanding Shares', 'Market Cap', 'Next Earnings Date', 'Optionable'
                   ]
    company_data = {}
    concerned = page_source.split('row price-data-section mb-5')[1]
    for f in re.findall('<a [a-z]+=\"[^"]+\" [a-z]+=\"[^"]+\">', concerned) :
        concerned = concerned.replace(f, '')
    for data_point in to_retrieve :
        
        data = data_point.replace('(', '\(').replace(')', '\)')
        
        finding = (re.findall('>'+data+'</a><strong>[^<>]*<', concerned)+re.findall('>'+data+'<strong>[^<>]*<', concerned))[0].split('>')[-1][:-1].lstrip()
        company_data[data_point] = finding
    return company_data

import tkinter as tk

from tkinter import Button, Label, Entry


LARGE_FONT = ("Verdana", 12)


def load_user_data() :
    pass

loading = False

user_data = []


def validatePassword(s) :
    if s == 'soccer' :
        return HomePage
    return WrongPassword

class StockTracker(tk.Tk) :
    
    def __init__(self, *args, **kwargs) :
        tk.Tk.__init__(self, *args, **kwargs)

        container=tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        loading=False
        
        for F in (StartPage, SignInPage, HomePage, WrongPassword, SearchStocks) :
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont) :
        frame=self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)
        label1 = Label(self, text="Welcome to the Stock Tracker", font=LARGE_FONT)
        label1.pack(pady=10, padx=10)

        button1 = Button(self, text="Sign In",
                         command=lambda: controller.show_frame(SignInPage))
        button1.pack()

class SignInPage(tk.Frame):

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)

        label2 = Label(self, text="Password", font=LARGE_FONT)
        label2.pack(pady=10, padx=10)


        self.password = Entry(self,text='Password')
        self.password.pack()

        button2 = Button(self, text="Submit",
                         command=lambda: controller.show_frame(validatePassword(self.password.get())))
        button2.pack()

class HomePage(tk.Frame) :
    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)

        label3 = Label(self, text="This is your list of Searched Stock Tickers.", font=LARGE_FONT)
        label3.pack(pady=10, padx=10)

        print(user_data)

        
        button3 = Button(self, text="Add Stock",
                         command=lambda: controller.show_frame(SearchStocks))
        button3.pack()

class WrongPassword(tk.Frame) :
    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)

        label4 = Label(self, text="Incorrect Password", font=LARGE_FONT)
        label4.pack(pady=10, padx=10)

        
        button4 = Button(self, text="Try Again",
                         command=lambda: controller.show_frame(SignInPage))
        button4.pack()

class SearchStocks(tk.Frame):

    def __init__(self, parent, controller) :
        tk.Frame.__init__(self, parent)

        label5 = Label(self, text="Search for a Stock (Ticker)", font=LARGE_FONT)
        label5.pack(pady=10, padx=10)

        label_loading = Label(self, text="This may take a second after button click, please be patient.", font=LARGE_FONT)
        label_loading.pack(pady=10, padx=10)


        self.search = Entry(self,text='Stock')
        self.search.pack()


        self.selected_stock = ()
        self.search_results = []
        self.company_data = []
        
        button5 = Button(self, text="Submit",
                         command=lambda: self.redefine_labels())
        button5.pack()

        self.label6 = Label(self, text="Results:", font=LARGE_FONT)
        self.label6.pack(pady=10, padx=10)

        self.option1 = Label(self, text="", font=LARGE_FONT)

        self.opt_button1 = Button(self, text="Select",
                         command=lambda: self.selected_widgets(0))

        self.option2 = Label(self, text="", font=LARGE_FONT)

        self.opt_button2 = Button(self, text="Select",
                         command=lambda: self.selected_widgets(1))

        self.option3 = Label(self, text="", font=LARGE_FONT)

        self.opt_button3 = Button(self, text="Select",
                         command=lambda: self.selected_widgets(2))

        self.option4 = Label(self, text="", font=LARGE_FONT)

        self.opt_button4 = Button(self, text="Select",
                         command=lambda: self.selected_widgets(3))

        self.option5 = Label(self, text="", font=LARGE_FONT)

        self.opt_button5 = Button(self, text="Select",
                         command=lambda: self.selected_widgets(4))

        self.info_on_screen = []
    def redefine_labels(self) :
        for t in self.info_on_screen :
            t.pack_forget()
        url = construct_search_url(self.search.get())
        self.search_results = scrape_search_results(load_page_source(url), self.search.get())
        option_list = [self.option1, self.option2, self.option3, self.option4, self.option5]
        button_list = [self.opt_button1, self.opt_button2, self.opt_button3, self.opt_button4, self.opt_button5]
        if self.search_results == [] :
            self.label6["text"] = "Your request failed. Please try again."
            for i, option in enumerate(option_list) :
                option["text"] = ""
                option.pack_forget()
                button_list[i].pack_forget()
        else :
            self.label6["text"] = "Success!"
            for i, option in enumerate(option_list) :
                try :
                    option["text"] = "Option "+str(i+1)+": "+self.search_results[i][0]
                    option.pack(pady=10, padx=10)
                    button_list[i].pack()
                except :
                    break

    def selected_widgets(self, ind) :
        self.selected_stock = self.search_results[ind]
        self.company_data = get_company_data(load_page_source(self.selected_stock[1]))
        option_list = [self.option1, self.option2, self.option3, self.option4, self.option5]
        button_list = [self.opt_button1, self.opt_button2, self.opt_button3, self.opt_button4, self.opt_button5]
        for i, option in enumerate(option_list) :
            option["text"] = ""
            option.pack_forget()
            button_list[i].pack_forget()
        self.label6["text"] = "Here's the Company Data. Confirm?"

        self.list_of_keys = list(self.company_data.keys())
        index_of_splitter = self.list_of_keys.index('Price / Sales')
        self.list_of_keys1, self.list_of_keys2 = self.list_of_keys[:index_of_splitter], self.list_of_keys[-(len(self.list_of_keys)-index_of_splitter):]

        self.info_on_screen = []
        
        for key in self.list_of_keys1 :
            t = Label(self, text=key+": "+self.company_data[key], font=LARGE_FONT)
            t.pack()
            self.info_on_screen.append(t)
            
        self.next_page_button = Button(self, text=">>>",
                         command=lambda: self.new_page())
        self.next_page_button.pack()

        self.info_on_screen.append(self.next_page_button)
            
    def new_page(self) :
        for t in self.info_on_screen :
            t.pack_forget()
            
        self.info_on_screen = []
        for key in self.list_of_keys2 :
            t = Label(self, text=key+": "+self.company_data[key], font=LARGE_FONT)
            t.pack()
            self.info_on_screen.append(t)
            
        self.confirm_button = Button(self, text="Confirm",
                         command=lambda: controller.show_frame(HomePage))
        self.confirm_button.pack()
        self.info_on_screen.append(self.confirm_button)

    def confirm_information(self) :
        user_data.append(self.company_data)
        controller.show_frame(HomePage)
        #print(user_data)
                         
app = StockTracker()

app.mainloop()


