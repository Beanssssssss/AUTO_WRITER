from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as msgbox
from get_access import get_login_eta
root = Tk()
root.title('Auto Writer')
root.resizable(False, False)
# ===== 🔽 전체 스크롤 가능한 캔버스 프레임 만들기 =====
main_canvas = Canvas(root, width=600, height=700)
scrollbar = Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = Frame(main_canvas)
def resize_frame(event):
    main_canvas.itemconfig("window_frame", width=event.width)
def on_frame_configure(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))
main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="window_frame")
main_canvas.bind("<Configure>", resize_frame)
main_canvas.configure(yscrollcommand=scrollbar.set)
scrollable_frame.bind("<Configure>", on_frame_configure)
main_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
def choose_file():
    file = filedialog.askopenfilename(
        title='텍스트 파일을 선택하세요',
        filetypes=(('txt 파일', "*.txt"), ("모든 파일", "*.*")),
        initialdir=r"/Users/kjb/Desktop/"
    )

    if not file:
        return  # 선택 안 했을 때 종료

    list_file.delete(0, END)
    list_file.insert(END, file)

    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        txt.delete("1.0", END)
        txt.insert(END, content)
        txt.config(state="disabled")

def del_file():
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

def extra_add_file():
    files = filedialog.askopenfilenames(title='이미지 파일을 선택하세요',
        filetypes=(
            ('이미지 파일', ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif")),
            ('모든 파일', "*.*")
        ),
        initialdir=r"/Users/kjb/Desktop/")
    # 사용자가 선택한 파일 목록
    for file in files:
        file_list_file.insert(END, file)

def extra_del_file():
    for index in reversed(file_list_file.curselection()):
        file_list_file.delete(index)

# 파일 프레임
file_frame = LabelFrame(scrollable_frame, text="텍스트 파일")
file_frame.pack(fill='x', padx=5, pady=5)

# 버튼 묶는 프레임 따로 생성해서 위쪽에 배치
button_frame = Frame(file_frame)
button_frame.pack(fill='x')

btn_add_file = Button(button_frame, text="파일 선택", command=choose_file)
btn_add_file.pack(side='left')

btn_del_file = Button(button_frame, text='선택 삭제', command=del_file)
btn_del_file.pack(side='right')

#  리스트 박스를 버튼 아래로 배치
list_frame = Frame(file_frame)
list_frame.pack(fill='both', padx=5, pady=5)

list_file = Listbox(list_frame, selectmode='extended', height=3)
list_file.pack(side='left', fill='both', expand=True)

#첨부 파일 프레임
extra_file_frame = LabelFrame(scrollable_frame, text = "첨부 파일")
extra_file_frame.pack(fill='x', padx=5, pady=5)
file_button_frame = Frame(extra_file_frame)
file_button_frame.pack(fill='x')

file_btn_add_file = Button(file_button_frame, text="파일 선택", command=extra_add_file)
file_btn_add_file.pack(side='left')

file_btn_del_file = Button(file_button_frame, text='선택 삭제', command=extra_del_file)
file_btn_del_file.pack(side='right')

# ✅ 리스트 박스를 버튼 아래로 배치
file_list_frame = Frame(extra_file_frame)
file_list_frame.pack(fill='both', padx=5, pady=5)

file_list_file = Listbox(file_list_frame, selectmode='extended', height=3)
file_list_file.pack(side='left', fill='both', expand=True)
#제목 프레임
title_frame = LabelFrame(scrollable_frame, text = "제목")
title_frame.pack(fill='both', padx=5, pady=5)
e = Entry(title_frame, width=50)
e.pack()
#내용 프레임
content_frame = LabelFrame(scrollable_frame, text = '내용')
content_frame.pack(fill='both', padx=5, pady=5)
scrbar = Scrollbar(content_frame)
scrbar.pack(side='right', fill = 'y')
txt = Text(content_frame, width=60, height=20,padx=5, pady=5,yscrollcommand=scrbar.set)
txt.pack()
scrbar.config(command=txt.yview)
# 해시태그 프레임
hash_frame = LabelFrame(scrollable_frame, text='해시태그')
hash_frame.pack(fill='both', padx=5, pady=5)
hash_code = Entry(hash_frame, width=50)
hash_code.insert(0, "#헤이트슬롭")
hash_code.pack()
#옵션 프레임
frame_option = LabelFrame(scrollable_frame, text='옵션')
frame_option.pack(fill='x', padx=5, pady=5)

# 최상위 선택 여부
is_eta = BooleanVar()
is_sedam = BooleanVar()

# 하위 체크박스 변수들
eta_club = BooleanVar()
eta_free = BooleanVar()
eta_fresh = BooleanVar()
eta_info = BooleanVar()
eta_promo = BooleanVar()
sedam_club = BooleanVar()
sedam_normal = BooleanVar()

# ==== 에타 토글 ====
def toggle_eta():
    if is_eta.get():
        eta_frame.pack(pady=5)
    else:
        eta_frame.pack_forget()

def get_selected_eta_boards():
    selected = []
    if eta_club.get(): selected.append("동아리·학회")
    if eta_free.get(): selected.append("자유게시판")
    if eta_fresh.get(): selected.append("새내기게시판")
    if eta_info.get(): selected.append("정보게시판")
    if eta_promo.get(): selected.append("홍보게시판")
    return selected

Checkbutton(frame_option, text="에타", variable=is_eta, command=toggle_eta).pack(anchor="w", padx=10)

eta_frame = Frame(frame_option)
Label(eta_frame, text="에타 게시판 선택").pack(anchor="w")
Checkbutton(eta_frame, text="동아리·학회", variable=eta_club).pack(anchor="w")
Checkbutton(eta_frame, text="자유게시판", variable=eta_free).pack(anchor="w")
Checkbutton(eta_frame, text="새내기게시판", variable=eta_fresh).pack(anchor="w")
Checkbutton(eta_frame, text="정보게시판", variable=eta_info).pack(anchor="w")
Checkbutton(eta_frame, text="홍보게시판", variable=eta_promo).pack(anchor="w")
'''
# ==== 서담 토글 ====
def toggle_sedam():
    if is_sedam.get():
        sedam_frame.pack(pady=5)
    else:
        sedam_frame.pack_forget()

Checkbutton(frame_option, text="서담", variable=is_sedam, command=toggle_sedam).pack(anchor="w", padx=10)

sedam_frame = Frame(frame_option)
Label(sedam_frame, text="서담 게시판 선택").pack(anchor="w")
Checkbutton(sedam_frame, text="동아리 게시판", variable=sedam_club).pack(anchor="w")
Checkbutton(sedam_frame, text="일반 게시판", variable=sedam_normal).pack(anchor="w")
'''
selected_eta = []
# ==== 제출 ====
def submit():
    global selected_eta 
    selected_eta = get_selected_eta_boards()
    print("✔ 에타 선택됨:", is_eta.get())
    print("✔ 선택된 게시판들:", selected_eta)
    '''
    print("✔ 서담 선택됨:", is_sedam.get())
    print("  - 동아리 게시판:", sedam_club.get())
    print("  - 일반 게시판:", sedam_normal.get())
    '''
    get_login_eta(selected_eta, e.get(), txt.get("1.0", END), file_list_file.get(0, END), hash_code.get())

Button(scrollable_frame, text="올리기", command=submit).pack(pady=20)

root.mainloop()