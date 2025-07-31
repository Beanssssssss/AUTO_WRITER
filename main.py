from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.font as tkfont
import tkinter.messagebox as msgbox
from get_access import get_login_eta, get_login_sdam
import threading
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
def choose_file(platform):
    file = filedialog.askopenfilename(
        title='텍스트 파일을 선택하세요',
        filetypes=(('txt 파일', "*.txt"), ("모든 파일", "*.*")),
        initialdir=r"/Users/kjb/Desktop/python/PROJECT/AUTO_WRITER/"
    )

    if not file:
        return

    if platform == 'eta':
        eta_list_file.delete(0, END)
        eta_list_file.insert(END, file)
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            eta_txt.config(state='normal')
            eta_txt.delete("1.0", END)
            eta_txt.insert(END, content)
            eta_txt.config(state='disabled')

    elif platform == 'sdam':
        sdam_list_file.delete(0, END)
        sdam_list_file.insert(END, file)
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            sdam_txt.config(state='normal')
            sdam_txt.delete("1.0", END)
            sdam_txt.insert(END, content)
            sdam_txt.config(state='disabled')

def del_file(platform):
    if platform == 'eta':
        for index in reversed(eta_list_file.curselection()):
            eta_list_file.delete(index)
    elif platform == 'sdam':
        for index in reversed(sdam_list_file.curselection()):
            sdam_list_file.delete(index)

def extra_add_file(platform):
    files = filedialog.askopenfilenames(
        title='이미지 파일을 선택하세요',
        filetypes=(
            ('이미지 파일', ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif")),
            ('모든 파일', "*.*")
        ),
        initialdir=r"/Users/kjb/Desktop/python/PROJECT/AUTO_WRITER/"
    )
    for file in files:
        if platform == 'eta':
            eta_file_list_file.insert(END, file)
        elif platform == 'sdam':
            sdam_file_list_file.insert(END, file)

def extra_del_file(platform):
    if platform == 'eta':
        for index in reversed(eta_file_list_file.curselection()):
            eta_file_list_file.delete(index)
    elif platform == 'sdam':
        for index in reversed(sdam_file_list_file.curselection()):
            sdam_file_list_file.delete(index)

# ==== 에타 토글 ====
def toggle_post_frames():
    # 에타 조건
    if is_eta.get() and is_sdam.get():
        auto_frame.pack(pady=10)
        eta_frame.pack(pady=5)
        eta_post_frame.pack(fill='x', padx=5, pady=5)
        sedam_frame.pack(pady=5)
        sdam_post_frame.pack(fill='x', padx=5, pady=5)

    elif is_eta.get():
        auto_frame.pack(pady=10)
        eta_frame.pack(pady=5)
        eta_post_frame.pack(fill='x', padx=5, pady=5)
        sedam_frame.pack_forget()
        sdam_post_frame.pack_forget()

    elif is_sdam.get():
        auto_frame.pack(pady=10)
        sedam_frame.pack(pady=5)
        sdam_post_frame.pack(fill='x', padx=5, pady=5)
        eta_frame.pack_forget()
        eta_post_frame.pack_forget()

    else:
        eta_frame.pack_forget()
        eta_post_frame.pack_forget()
        sedam_frame.pack_forget()
        sdam_post_frame.pack_forget()
        auto_frame.pack_forget()

def get_selected_eta_boards():
    selected = []
    if eta_club.get(): selected.append("동아리·학회")
    if eta_free.get(): selected.append("자유게시판")
    if eta_fresh.get(): selected.append("새내기게시판")
    if eta_info.get(): selected.append("정보게시판")
    if eta_promo.get(): selected.append("홍보게시판")
    return selected

def get_selected_sdam():
    selected = []
    if sdam_free.get(): selected.append("자유게시판")
    if sdam_an1.get(): selected.append("익게1")
    if sdam_an2.get(): selected.append("익게2")
    if sdam_club.get(): selected.append("모집공고")
    return selected
#옵션 프레임
frame_option = LabelFrame(scrollable_frame, text='옵션')
frame_option.pack(fill='x', padx=5, pady=5)

# 최상위 선택 여부
is_eta = BooleanVar()
is_sdam = BooleanVar()

# 하위 체크박스 변수들
eta_club = BooleanVar()
eta_free = BooleanVar()
eta_fresh = BooleanVar()
eta_info = BooleanVar()
eta_promo = BooleanVar()
sdam_free = BooleanVar()
sdam_an1 = BooleanVar()
sdam_an2 = BooleanVar()
sdam_club = BooleanVar()

Checkbutton(frame_option, text="에타", variable=is_eta, command=toggle_post_frames).pack(anchor="w", padx=10)

eta_frame = Frame(frame_option)
Label(eta_frame, text="에타 게시판 선택").pack(anchor="w")
Checkbutton(eta_frame, text="동아리·학회", variable=eta_club).pack(anchor="w")
Checkbutton(eta_frame, text="자유게시판", variable=eta_free).pack(anchor="w")
Checkbutton(eta_frame, text="새내기게시판", variable=eta_fresh).pack(anchor="w")
Checkbutton(eta_frame, text="정보게시판", variable=eta_info).pack(anchor="w")
Checkbutton(eta_frame, text="홍보게시판", variable=eta_promo).pack(anchor="w")

Checkbutton(frame_option, text="서담", variable=is_sdam, command=toggle_post_frames).pack(anchor="w", padx=10)

sedam_frame = Frame(frame_option)
Label(sedam_frame, text="서담 게시판 선택").pack(anchor="w")
Checkbutton(sedam_frame, text="자유게시판", variable=sdam_free).pack(anchor="w")
Checkbutton(sedam_frame, text="익게1", variable=sdam_an1).pack(anchor="w")
Checkbutton(sedam_frame, text="익게2", variable=sdam_an2).pack(anchor="w")
Checkbutton(sedam_frame, text="모집공고", variable=sdam_club).pack(anchor="w")
########################################################################
# 에타용 전체 프레임
eta_post_frame = LabelFrame(
    scrollable_frame,
    text="에타 글 작성",
    font=tkfont.Font(size=14, weight="bold")  # 글자 크기 14, 굵게
)
eta_post_frame.pack(fill='x', padx=5, pady=5)
eta_post_frame.pack_forget()
# 에타 파일 프레임
eta_file_frame = LabelFrame(eta_post_frame, text="텍스트 파일")
eta_file_frame.pack(fill='x', padx=5, pady=5)

# 버튼 묶는 프레임 따로 생성해서 위쪽에 배치
eta_button_frame = Frame(eta_file_frame)
eta_button_frame.pack(fill='x')

eta_btn_add_file = Button(eta_button_frame, text="파일 선택", command=lambda: choose_file('eta'))
eta_btn_add_file.pack(side='left')

eta_btn_del_file = Button(eta_button_frame, text='선택 삭제', command=lambda: del_file('eta'))
eta_btn_del_file.pack(side='right')

#  리스트 박스를 버튼 아래로 배치
eta_list_frame = Frame(eta_file_frame)
eta_list_frame.pack(fill='both', padx=5, pady=5)

eta_list_file = Listbox(eta_list_frame, selectmode='extended', height=3)
eta_list_file.pack(side='left', fill='both', expand=True)

#첨부 파일 프레임
eta_extra_file_frame = LabelFrame(eta_post_frame, text = "첨부 파일")
eta_extra_file_frame.pack(fill='x', padx=5, pady=5)

eta_file_button_frame = Frame(eta_extra_file_frame)
eta_file_button_frame.pack(fill='x')


eta_file_btn_add_file = Button(eta_file_button_frame, text="파일 선택", command=lambda: extra_add_file('eta'))
eta_file_btn_add_file.pack(side='left')

eta_file_btn_del_file = Button(eta_file_button_frame, text='선택 삭제', command=lambda: extra_del_file('eta'))
eta_file_btn_del_file.pack(side='right')

# ✅ 리스트 박스를 버튼 아래로 배치
eta_file_list_frame = Frame(eta_extra_file_frame)
eta_file_list_frame.pack(fill='both', padx=5, pady=5)

eta_file_list_file = Listbox(eta_file_list_frame, selectmode='extended', height=3)
eta_file_list_file.pack(side='left', fill='both', expand=True)
#제목 프레임
eta_title_frame = LabelFrame(eta_post_frame, text = "제목")
eta_title_frame.pack(fill='both', padx=5, pady=5)
eta_e = Entry(eta_title_frame, width=50)
eta_e.pack()
#내용 프레임
eta_content_frame = LabelFrame(eta_post_frame, text = '내용')
eta_content_frame.pack(fill='both', padx=5, pady=5)
eta_scrbar = Scrollbar(eta_content_frame)
eta_scrbar.pack(side='right', fill = 'y')
eta_txt = Text(eta_content_frame, width=60, height=20,padx=5, pady=5,yscrollcommand=eta_scrbar.set)
eta_txt.pack()
eta_scrbar.config(command=eta_txt.yview)
# 해시태그 프레임
eta_hash_frame = LabelFrame(eta_post_frame, text='해시태그')
eta_hash_frame.pack(fill='both', padx=5, pady=5)
eta_hash_code = Entry(eta_hash_frame, width=50)
eta_hash_code.insert(0, "#헤이트슬롭")
eta_hash_code.pack()
####################################################################
# 서담용 전체 프레임
sdam_post_frame = LabelFrame(
    scrollable_frame,
    text="서담 글 작성",
    font=tkfont.Font(size=14, weight="bold")  # 글자 크기 14, 굵게
)
sdam_post_frame.pack(fill='x', padx=5, pady=5)
sdam_post_frame.pack_forget()
# 서담 파일 프레임
sdam_file_frame = LabelFrame(sdam_post_frame, text="텍스트 파일")
sdam_file_frame.pack(fill='x', padx=5, pady=5)

# 버튼 묶는 프레임 따로 생성해서 위쪽에 배치
sdam_button_frame = Frame(sdam_file_frame)
sdam_button_frame.pack(fill='x')

sdam_btn_add_file = Button(sdam_button_frame, text="파일 선택", command=lambda: choose_file('sdam'))
sdam_btn_add_file.pack(side='left')

sdam_btn_del_file = Button(sdam_button_frame, text='선택 삭제', command=lambda: del_file('sdam'))
sdam_btn_del_file.pack(side='right')

#  리스트 박스를 버튼 아래로 배치
sdam_list_frame = Frame(sdam_file_frame)
sdam_list_frame.pack(fill='both', padx=5, pady=5)

sdam_list_file = Listbox(sdam_list_frame, selectmode='extended', height=3)
sdam_list_file.pack(side='left', fill='both', expand=True)

#첨부 파일 프레임
sdam_extra_file_frame = LabelFrame(sdam_post_frame, text = "첨부 파일")
sdam_extra_file_frame.pack(fill='x', padx=5, pady=5)
sdam_file_button_frame = Frame(sdam_extra_file_frame)
sdam_file_button_frame.pack(fill='x')

sdam_file_btn_add_file = Button(sdam_file_button_frame, text="파일 선택", command=lambda: extra_add_file('sdam'))
sdam_file_btn_add_file.pack(side='left')

sdam_file_btn_del_file = Button(sdam_file_button_frame, text='선택 삭제', command=lambda: extra_del_file('sdam'))
sdam_file_btn_del_file.pack(side='right')

# ✅ 리스트 박스를 버튼 아래로 배치
sdam_file_list_frame = Frame(sdam_extra_file_frame)
sdam_file_list_frame.pack(fill='both', padx=5, pady=5)

sdam_file_list_file = Listbox(sdam_file_list_frame, selectmode='extended', height=3)
sdam_file_list_file.pack(side='left', fill='both', expand=True)
#제목 프레임
sdam_title_frame = LabelFrame(sdam_post_frame, text = "제목")
sdam_title_frame.pack(fill='both', padx=5, pady=5)
sdam_e = Entry(sdam_title_frame, width=50)
sdam_e.pack()
#내용 프레임
sdam_content_frame = LabelFrame(sdam_post_frame, text = '내용')
sdam_content_frame.pack(fill='both', padx=5, pady=5)
sdam_scrbar = Scrollbar(sdam_content_frame)
sdam_scrbar.pack(side='right', fill = 'y')
sdam_txt = Text(sdam_content_frame, width=60, height=20,padx=5, pady=5,yscrollcommand=sdam_scrbar.set)
sdam_txt.pack()
sdam_scrbar.config(command=sdam_txt.yview)
# 해시태그 프레임
sdam_hash_frame = LabelFrame(sdam_post_frame, text='해시태그')
sdam_hash_frame.pack(fill='both', padx=5, pady=5)
sdam_hash_code = Entry(sdam_hash_frame, width=50)
sdam_hash_code.insert(0, "#헤이트슬롭")
sdam_hash_code.pack()
####################################################################
selected_eta = []
selected_sdm = []
auto_upload = BooleanVar()
upload_interval_min = IntVar(value=10)
upload_timer = None

# ===== 제출 함수 =====
def submit():
    global selected_eta, selected_sdm
    selected_eta = get_selected_eta_boards()
    selected_sdm = get_selected_sdam()
    print("✔ 에타 선택됨:", is_eta.get())
    print("✔ 선택된 게시판들:", selected_eta)
    print("✔ 서담 선택됨:", is_sdam.get())
    print("✔ 선택된 게시판들:", selected_sdm)
    if(is_eta.get()):
        get_login_eta(selected_eta, eta_e.get(), eta_txt.get("1.0", END), eta_file_list_file.get(0, END), eta_hash_code.get())
    if(is_sdam.get()):
        get_login_sdam(selected_sdm, sdam_e.get(), sdam_txt.get("1.0", END), sdam_file_list_file.get(0, END), sdam_hash_code.get())
# ===== 자동 업로드 반복 함수 =====
def auto_upload_loop():
    global upload_timer  
    if auto_upload.get():
        print("🔁 자동 업로드 실행됨")
        submit()
        interval = upload_interval_min.get() * 60
        upload_timer = threading.Timer(interval, auto_upload_loop)
        upload_timer.start()
def stop_auto_upload():
    global upload_timer
    auto_upload.set(False)
    if upload_timer is not None:
        upload_timer.cancel()
        upload_timer = None
        print("⛔ 자동 업로드 중지됨")
# ===== 시작 버튼 핸들러 =====
def handle_start():
    if auto_upload.get():
        print(f"✅ 자동 업로드 시작됨 (간격: {upload_interval_min.get()}분)")
        auto_upload_loop()
    else:
        print("📤 단일 업로드 실행")
        submit()

# 업로드 옵션
auto_frame = Frame(scrollable_frame)
auto_frame.pack(pady=10)
auto_frame.forget()

Label(auto_frame, text="업로드 간격 (분): ").pack(side='left')
interval_combo = ttk.Combobox(auto_frame, width=5, textvariable=upload_interval_min)
interval_combo['values'] = [1, 10, 20, 30, 60, 120, 180]
interval_combo.current(2)
interval_combo.pack(side='left', padx=5)

Checkbutton(auto_frame, text="자동 업로드", variable=auto_upload).pack(side='left')
Button(auto_frame, text="시작", command=handle_start).pack(side='left', padx=10)
Button(auto_frame, text="중지", command=stop_auto_upload).pack(side='left', padx=10)
root.mainloop()