# Web adaptation of def_hkg.py

def tu_dien_co_ban_course(A, B, C, D):
    block = "\\begin{tikzpicture}[scale=1,>=stealth, line join=round, line cap=round, line width=1pt]"\
        + f"\n\t\\foreach \\x/\\y/\\p in {{0/0/{B},1.3/-1.6/{C},4.5/0/{D},1/3.5/{A}}}{{\\path (\\x,\\y) coordinate (\\p);}}"\
        + f"\n\t\\draw ({A})--({B})--({C})--({D})--({A})--({C});"\
        + f"\n\t\\draw[dashed, line width=.8pt]({B})--({D});"\
        + f"\n\t\\foreach \\x/\\g in {{{A}/90,{B}/-170,{C}/-110,{D}/-10}}\\draw[fill=white] (\\x) circle (.045)+(\\g:.3) node[black]{{$\\x$}};"\
        + "\n\\end{tikzpicture}"
    return block

def chop_tam_giac_loai_mot_source(S, A, B, C):
    block = "\\begin{tikzpicture}[scale=1,>=stealth, line join=round, line cap=round, line width=1pt]"\
        + f"\n\t\\foreach \\x/\\y/\\p in {{0/0/{A},1.2/-1.5/{B},4/0/{C}}}{{\\path (\\x,\\y) coordinate (\\p);}}"\
        + f"\n\t\\path ($({A})+(0,3)$) coordinate ({S});"\
        + f"\n\t\\draw ({S})--({A})--({B})--({C})--({S})--({B});"\
        + f"\n\t\\draw[dashed, line width=.8pt]({A})--({C});"\
        + f"\n\t\\foreach \\x/\\g in {{{A}/-170,{B}/-110,{C}/-10,{S}/90}}\\draw[fill=white] (\\x) circle (.045)+(\\g:.3) node[black]{{$\\x$}};"\
        + "\n\\end{tikzpicture}"
    return block

def chop_tam_giac_loai_hai_source(S, A, B, C, G, M):
    block = "\\begin{tikzpicture}[scale=1,>=stealth, line join=round, line cap=round, line width=1pt]"\
        + f"\n\t\\foreach \\x/\\y/\\p in {{0/0/{A},1.2/-1.6/{B},4.5/0/{C}}}{{\\path (\\x,\\y) coordinate (\\p);}}"\
        + f"\n\t\\path ($({B})!1/2!({C})$) coordinate ({M})"\
        + f"\n\t($({A})!2/3!({M})$) coordinate ({G})"\
        + f"\n\t($({G})+(0,3.5)$) coordinate({S});"\
        + f"\n\t\\draw ({S})--({A})--({B})--({C})--cycle ({S})--({B});"\
        + f"\n\t\\draw[dashed, line width=.8pt] ({M})--({A})--({C}) ({S})--({G});"\
        + f"\n\t\\foreach \\x/\\g in {{{A}/-170,{B}/-110,{C}/-10,{S}/90,{G}/-90,{M}/-30}}\\draw[fill=white] (\\x) circle (.045)+(\\g:.3) node[black]{{$\\x$}};"\
        + "\n\\end{tikzpicture}"
    return block

def chop_tam_giac_loai_ba_source(S, A, B, C, H):
    block = "\\begin{tikzpicture}[scale=1,>=stealth, line join=round, line cap=round, line width=1pt]"\
        + f"\n\t\\foreach \\x/\\y/\\p in {{0/0/{B},1/-1.5/{A},4/0/{C}}}{{\\path (\\x,\\y) coordinate (\\p);}}"\
        + f"\n\t\\path ($({B})!1/2!({C})$) coordinate ({H})"\
        + f"\n\t($({H})+(0,3.5)$) coordinate ({S});"\
        + f"\n\t\\draw ({S})--({B})--({A})--({C})--({S})--({A});"\
        + f"\n\t\\draw[dashed, line width=.8pt] ({S})--({H}) ({B})--({C});"\
        + f"\n\t\\foreach \\x/\\g in {{{A}/-110,{B}/-170,{C}/-10,{S}/90,{H}/-90}}\\draw[fill=white] (\\x) circle (.045)+(\\g:.3) node[black]{{$\\x$}};"\
        + "\n\\end{tikzpicture}"
    return block

def chop_tu_giac_loai_mot_source(S, A, B, C, D):
    block = "\\begin{tikzpicture}[scale=1,>=stealth, line join=round, line cap=round, line width=1pt]"\
        + f"\n\t\\foreach \\x/\\y/\\p in {{0/0/{A},-1.4/-1.6/{B},2.5/-1.6/{C}}}{{\\path (\\x,\\y) coordinate (\\p);}}"\
        + f"\n\t\\path ($({A})+({C})-({B})$) coordinate ({D})"\
        + f"\n\t($({A})+(0,3.5)$) coordinate ({S});"\
        + f"\n\t\\draw ({S})--({B})--({C})--({D})--({S})--({C});"\
        + f"\n\t\\draw[dashed, line width=.8pt] ({A})--({S})({B})--({A})--({D});"\
        + f"\n\t\\foreach \\x/\\g in {{{A}/-85,{B}/-110,{C}/-30,{S}/90,{D}/-10}}\\draw[fill=white] (\\x) circle (.045)+(\\g:.3) node[black]{{$\\x$}};"\
        + "\n\\end{tikzpicture}"
    return block

def chop_tu_giac_loai_hai_source(S, A, B, C, D, G):
    block = "\\begin{tikzpicture}[scale=1,>=stealth, line join=round, line cap=round, line width=1pt]"\
        + f"\n\t\\foreach \\x/\\y/\\p in {{0/0/{A},-1.4/-1.6/{B},2.5/-1.6/{C}}}{{\\path (\\x,\\y) coordinate (\\p);}}"\
        + f"\n\t\\path ($({A})+({C})-({B})$) coordinate ({D})"\
        + f"\n\t(intersection of {A}--{C} and {B}--{D}) coordinate ({G})"\
        + f"\n\t($({G})+(0,3.5)$) coordinate ({S});"\
        + f"\n\t\\draw ({S})--({B})--({C})--({D})--({S})--({C});"\
        + f"\n\t\\draw[dashed, line width=.8pt] ({C})--({A})--({S}) ({B})--({A})--({D})--cycle ({S})--({G});"\
        + f"\n\t\\foreach \\x/\\g in {{{A}/-85,{B}/-110,{C}/-30,{S}/90,{D}/-10,{G}/-90}}\\draw[fill=white] (\\x) circle (.045)+(\\g:.3) node[black]{{$\\x$}};"\
        + "\n\\end{tikzpicture}"
    return block

def chop_tu_giac_loai_ba_source(S, A, B, C, D, H):
    block = "\\begin{tikzpicture}[scale=1,>=stealth, line join=round, line cap=round, line width=1pt]"\
        + f"\n\t\\foreach \\x/\\y/\\p in {{0/0/{A},-1.4/-1.6/{B},2.5/-1.6/{C}}}{{\\path (\\x,\\y) coordinate (\\p);}}"\
        + f"\n\t\\path ($({A})+({C})-({B})$) coordinate ({D})"\
        + f"\n\t($({A})!1/2!({B})$) coordinate ({H})"\
        + f"\n\t($({H})+(0,3.5)$) coordinate ({S});"\
        + f"\n\t\\draw ({S})--({B})--({C})--({D})--({S})--({C});"\
        + f"\n\t\\draw[dashed, line width=.8pt] ({A})--({S})--({H}) ({B})--({A})--({D});"\
        + f"\n\t\\foreach \\x/\\g in {{{A}/170,{B}/-110,{C}/-30,{S}/90,{D}/-10,{H}/-60}}\\draw[fill=white] (\\x) circle (.045)+(\\g:.3) node[black]{{$\\x$}};"\
        + "\n\\end{tikzpicture}"
    return block

def lang_tru_dung_source(A, B, C, M, N, P):
    block = "\\begin{tikzpicture}[scale=1,>=stealth, line join=round, line cap=round, line width=1pt]"\
        + f"\n\t\\foreach \\x/\\y/\\p in {{0/0/{A},1.1/-1.5/{B},3.5/0/{C}}}{{\\path (\\x,\\y) coordinate (\\p);}}"\
        + f"\n\t\\path ($({A})+(0,3.2)$) coordinate ({M});"\
        + f"\\foreach \\x/\\y in {{{B}/{N},{C}/{P}}}{{\\path ($({M})+(\\x)-({A})$) coordinate (\\y);}}"\
        + f"\n\t\\draw ({A})--({B})--({C})--({P})--({N})--({M})--cycle ({M})--({P}) ({B})--({N});"\
        + f"\n\t\\draw[dashed, line width=.8pt]({A})--({C});"\
        + f"\n\t\\foreach \\x/\\g in {{{A}/-170,{B}/-110,{C}/-10,{M}/170,{N}/80,{P}/10}}\\draw[fill=white] (\\x) circle (.045)+(\\g:.3) node[black]{{$\\x$}};"\
        + "\n\\end{tikzpicture}"
    return block

def lang_tru_xien_source(A, B, C, M, N, P):
    block = "\\begin{tikzpicture}[scale=1,>=stealth, line join=round, line cap=round, line width=1pt]"\
        + f"\n\t\\foreach \\x/\\y/\\p in {{0/0/{A},1.1/-1.5/{B},3.5/0/{C}}}{{\\path (\\x,\\y) coordinate (\\p);}}"\
        + f"\n\t\\path ($({A})+(0.7,3.2)$) coordinate ({M});"\
        + f"\\foreach \\x/\\y in {{{B}/{N},{C}/{P}}}{{\\path ($({M})+(\\x)-({A})$) coordinate (\\y);}}"\
        + f"\n\t\\draw ({A})--({B})--({C})--({P})--({N})--({M})--cycle ({M})--({P}) ({B})--({N});"\
        + f"\n\t\\draw[dashed, line width=.8pt]({A})--({C});"\
        + f"\n\t\\foreach \\x/\\g in {{{A}/-170,{B}/-110,{C}/-10,{M}/170,{N}/80,{P}/10}}\\draw[fill=white] (\\x) circle (.045)+(\\g:.3) node[black]{{$\\x$}};"\
        + "\n\\end{tikzpicture}"
    return block

def hinh_hop_chu_nhat_source(A, B, C, D, M, N, P, Q):
    block = "\\begin{tikzpicture}[scale=1,>=stealth, line join=round, line cap=round, line width=1pt]"\
        + f"\n\t\\foreach \\x/\\y/\\p in {{0/0/{A},-1.1/-1.5/{B},2.5/-1.5/{C}}}{{\\path (\\x,\\y) coordinate (\\p);}}"\
        + f"\n\t\\path ($({A})+({C})-({B})$) coordinate ({D})"\
        + f"\n\t($({A})+(0,3.2)$) coordinate ({M});"\
        + f"\n\t\\foreach \\x/\\y in {{{B}/{N},{C}/{P},{D}/{Q}}}{{\\path ($({M})+(\\x)-({A})$) coordinate (\\y);}}"\
        + f"\n\t\\draw ({C})--({P}) ({N})--({M})--({Q})--({P})--({N})--({B})--({C})--({D})--({Q});"\
        + f"\n\t\\draw[dashed, line width=.8pt] ({M})--({A})--({D})({A})--({B});"\
        + f"\n\t\\foreach \\x/\\g in {{{A}/-170,{B}/-120,{C}/-50,{D}/-10,{M}/170,{N}/-145,{P}/-30,{Q}/10}}\\draw[fill=white] (\\x) circle (.045)+(\\g:.3) node[black]{{$\\x$}};"\
        + "\n\\end{tikzpicture}"
    return block

def hinh_hop_thuong_source(A, B, C, D, M, N, P, Q):
    block = "\\begin{tikzpicture}[scale=1,>=stealth, line join=round, line cap=round, line width=1pt]"\
        + f"\n\t\\foreach \\x/\\y/\\p in {{0/0/{A},-1.1/-1.5/{B},2.5/-1.5/{C}}}{{\\path (\\x,\\y) coordinate (\\p);}}"\
        + f"\n\t\\path ($({A})+({C})-({B})$) coordinate ({D})"\
        + f"\n\t($({A})+(0.7,3.2)$) coordinate ({M});"\
        + f"\n\t\\foreach \\x/\\y in {{{B}/{N},{C}/{P},{D}/{Q}}}{{\\path ($({M})+(\\x)-({A})$) coordinate (\\y);}}"\
        + f"\n\t\\draw ({C})--({P}) ({N})--({M})--({Q})--({P})--({N})--({B})--({C})--({D})--({Q});"\
        + f"\n\t\\draw[dashed, line width=.8pt] ({M})--({A})--({D})({A})--({B});"\
        + f"\n\t\\foreach \\x/\\g in {{{A}/-170,{B}/-120,{C}/-50,{D}/-10,{M}/170,{N}/-145,{P}/-30,{Q}/10}}\\draw[fill=white] (\\x) circle (.045)+(\\g:.3) node[black]{{$\\x$}};"\
        + "\n\\end{tikzpicture}"
    return block

def hinh_lap_phuong_source(A, B, C, D, M, N, P, Q):
    block = "\\begin{tikzpicture}[scale=1,>=stealth, line join=round, line cap=round, line width=1pt]"\
        + f"\n\t\\foreach \\x/\\y/\\p in {{0/0/{A},-1.1/-1.5/{B},2.5/-1.5/{C}}}{{\\path (\\x,\\y) coordinate (\\p);}}"\
        + f"\n\t\\path ($({A})+({C})-({B})$) coordinate ({D})"\
        + f"\n\t($({A})+(0,3.2)$) coordinate ({M});"\
        + f"\n\t\\foreach \\x/\\y in {{{B}/{N},{C}/{P},{D}/{Q}}}{{\\path ($({M})+(\\x)-({A})$) coordinate (\\y);}}"\
        + f"\n\t\\draw ({C})--({P}) ({N})--({M})--({Q})--({P})--({N})--({B})--({C})--({D})--({Q});"\
        + f"\n\t\\draw[dashed, line width=.8pt] ({M})--({A})--({D})({A})--({B});"\
        + f"\n\t\\foreach \\x/\\g in {{{A}/-170,{B}/-120,{C}/-50,{D}/-10,{M}/170,{N}/-145,{P}/-30,{Q}/10}}\\draw[fill=white] (\\x) circle (.045)+(\\g:.3) node[black]{{$\\x$}};"\
        + "\n\\end{tikzpicture}"
    return block

def khoi_non_course(R, h):
    block = "\\begin{tikzpicture}[scale=1, line join=round, line cap=round, line width=1pt]"\
        + "\n\t\\def\\h{"+h+"}"\
        + "\n\t\\def\\R{"+R+"}"\
        + "\n\t\\pgfmathsetmacro\\r{0.45*\\R}"\
        + "\n\t\\pgfmathsetmacro\\g{asin(\\r/\\h)}"\
        + "\n\t\\pgfmathsetmacro\\xo{\\R*cos(\\g)}"\
        + "\n\t\\pgfmathsetmacro\\yo{\\r*sin(\\g)}"\
        + "\n\t\\path (0,0) coordinate (O)"\
        + "\n\t(0,\\h) coordinate (S)"\
        + "\n\t(180:\\R) coordinate (A)"\
        + "\n\t(0:\\R) coordinate (B);"\
        + "\n\t\\draw[dashed, line width=.8pt](\\xo,\\yo) arc (\\g:180-\\g:{\\R} and {\\r}) (A)--(B) (O)--(S);"\
        + "\n\t\\draw (S)--(-\\xo,\\yo) arc (180-\\g:360+\\g:{\\R} and {\\r})--(S);"\
        + "\n\\end{tikzpicture}"
    return block

def khoi_tru_course(R, h):
    block = "\\begin{tikzpicture}[scale=1, line join=round, line cap=round, line width=1pt]"\
        + "\n\t\\def\\h{"+h+"}"\
        + "\n\t\\def\\R{"+R+"}"\
        + "\n\t\\pgfmathsetmacro\\r{0.45*\\R}"\
        + "\n\t\\path (0,0) coordinate (O)"\
        + "\n\t(0,\\h) coordinate (O')"\
        + "\n\t(180:\\R) coordinate (A)"\
        + "\n\t(0:\\R) coordinate (B)"\
        + "\n\t($(B)+(O')$) coordinate (C)"\
        + "\n\t($(A)+(O')$) coordinate (D);"\
        + "\n\t\\draw[dashed, line width=.8pt] (B) arc (0:180:{\\R} and {\\r});"\
        + "\n\t\\draw (O') ellipse ({\\R} and {\\r}) (C)--(B) arc (0:-180:{\\R} and {\\r})--(D);"\
        + "\n\\end{tikzpicture}"
    return block

def khoi_cau_course(R):
    block = "\\begin{tikzpicture}[scale=1, line join=round, line cap=round, line width=1pt]"\
        + "\n\t\\def\\R{"+R+"}"\
        + "\n\t\\pgfmathsetmacro\\r{0.45*\\R}"\
        + "\n\t\\path (0,0) coordinate (O)"\
        + "\n\t(180:\\R) coordinate (A)"\
        + "\n\t(0:\\R) coordinate (B);"\
        + "\n\t\\draw[dashed, line width=.8pt] (B) arc (0:180:{\\R} and {\\r});"\
        + "\n\t\\draw (O) circle (\\R) (B) arc (0:-180:{\\R} and {\\r});"\
        + "\n\\end{tikzpicture}"
    return block
