import tkinter as tk
from tkinter import ttk
from subprocess import Popen, PIPE

def get_results():
    keyword = keyword_entry.get()

    # Execute main.py with keyword as input
    process = Popen(['python', 'main.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    output, _ = process.communicate(keyword + '\n')
    
    # Split the output to get highest and lowest patents
    output_lines = output.split('\n')
    highest_patents = '\n'.join(output_lines[output_lines.index('Most Trending Patents with given keywords')+1 : output_lines.index('Emerging Patents with given keywords')-1])
    lowest_patents = '\n'.join(output_lines[output_lines.index('Emerging Patents with given keywords')+1 :])

    # Display the results in the GUI
    # display_as_table(highest_patents, lowest_patents)
    highest_patents_label.config(text=highest_patents)
    lowest_patents_label.config(text=lowest_patents)

def display_as_table(highest_patents, lowest_patents):
    result_window = tk.Toplevel()
    result_window.title("Patent Search Results")
    
    columns = ('Patent Name', 'Application Date', 'Applicant')

    highest_treeview = ttk.Treeview(result_window, columns=columns, show='headings')
    lowest_treeview = ttk.Treeview(result_window, columns=columns, show='headings')

    # 각 열에 대한 제목 설정
    for col in columns:
        highest_treeview.heading(col, text=col)
        lowest_treeview.heading(col, text=col)

    # 각 열의 너비 설정
    highest_treeview.column("Patent Name", width=400)
    highest_treeview.column("Application Date", width=100)
    highest_treeview.column("Applicant", width=200)

    lowest_treeview.column("Patent Name", width=400)
    lowest_treeview.column("Application Date", width=100)
    lowest_treeview.column("Applicant", width=200)

    # 데이터 입력
    for patent in highest_patents:
        highest_treeview.insert('', 'end', values=patent)

    for patent in lowest_patents:
        lowest_treeview.insert('', 'end', values=patent)

    highest_treeview.pack(padx=10, pady=5)
    lowest_treeview.pack(padx=10, pady=5)

# Create the main window
root = tk.Tk()
root.title('Patent Search')

# Create and place GUI elements
keyword_label = tk.Label(root, text="Enter keyword:")
keyword_label.pack()

keyword_entry = tk.Entry(root)
keyword_entry.pack()

search_button = tk.Button(root, text="Search", command=get_results)
search_button.pack()

highest_patents_label = tk.Label(root, text="Most Trending Patents with given keywords")
highest_patents_label.pack()

lowest_patents_label = tk.Label(root, text="Emerging Patents with given keywords")
lowest_patents_label.pack()

root.mainloop()
