import customtkinter as ctk
from tkinter import END, Canvas, Scrollbar, ttk, messagebox
import re

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AssemblyCompilerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pro Assembly Compiler: Zoomable Lexer NFA & Parser DFA")
        self.geometry("1400x950")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # متغیرهای زوم
        self.nfa_zoom = 1.0
        self.dfa_zoom = 1.0
        self.last_insts = [] # برای بازرسم درخت و DFA در هنگام زوم

        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.sidebar_frame, text="Compiler Pro", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        self.analyze_btn = ctk.CTkButton(self.sidebar_frame, text="RUN ANALYSIS", command=self.run_analysis, fg_color="#27ae60")
        self.analyze_btn.pack(pady=10, padx=20)

        self.clear_btn = ctk.CTkButton(self.sidebar_frame, text="CLEAR ALL", command=self.clear_inputs, fg_color="#c0392b")
        self.clear_btn.pack(pady=10, padx=20)

        # --- Tabs ---
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.tab_input = self.tabview.add("Code Editor")
        self.tab_tokens = self.tabview.add("Lexical")
        self.tab_parser = self.tabview.add("Parse Table")
        self.tab_tree = self.tabview.add("Parse Tree")
        self.tab_nfa = self.tabview.add("Lexer NFA")
        self.tab_dfa = self.tabview.add("Parser DFA (LR)")

        self.setup_input_tab()
        self.setup_token_tab()
        self.setup_parser_tab()
        self.setup_tree_tab()
        self.setup_nfa_tab()
        self.setup_dfa_tab()

    # --- Setup Methods ---
    def setup_input_tab(self):
        self.tab_input.grid_columnconfigure(0, weight=1)
        builder = ctk.CTkFrame(self.tab_input, fg_color="#2c3e50")
        builder.pack(fill="x", padx=10, pady=10)
        self.cmb_mnem = ctk.CTkOptionMenu(builder, values=["MOV", "XCHG", "LEA", "PUSH", "POP"], width=100)
        self.cmb_mnem.pack(side="left", padx=5, pady=10)
        self.cmb_d = ctk.CTkOptionMenu(builder, values=["AX", "BX", "AL", "[BX]", "[SI]"], width=100)
        self.cmb_d.pack(side="left", padx=5)
        self.ent_s = ctk.CTkEntry(builder, placeholder_text="Source", width=100)
        self.ent_s.pack(side="left", padx=5)
        ctk.CTkButton(builder, text="INSERT", width=60, command=self.add_line).pack(side="left", padx=5)
        self.code_input = ctk.CTkTextbox(self.tab_input, height=350, font=("Consolas", 18))
        self.code_input.pack(fill="both", expand=True, padx=10, pady=10)
        self.code_input.insert("0.0", "MOV AX, 10\nXCHG AX, BX\nLEA SI, [BX]")

    def add_line(self):
        m, d, s = self.cmb_mnem.get(), self.cmb_d.get(), self.ent_s.get()
        line = f"{m} {d}, {s}\n" if m not in ["PUSH", "POP"] else f"{m} {d}\n"
        self.code_input.insert(END, line)

    def setup_token_tab(self):
        self.token_display = ctk.CTkTextbox(self.tab_tokens, font=("Consolas", 14))
        self.token_display.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_parser_tab(self):
        f = ctk.CTkFrame(self.tab_parser)
        f.pack(fill="both", expand=True, padx=10, pady=10)
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Treeview", background="#2b2b2b", foreground="white", rowheight=45, fieldbackground="#2b2b2b")
        cols = ("s", "i", "a")
        self.tree_table = ttk.Treeview(f, columns=cols, show="headings")
        for col, head in zip(cols, ["Stack", "Input", "Action"]): self.tree_table.heading(col, text=head)
        self.tree_table.pack(fill="both", expand=True)

    def setup_tree_tab(self):
        self.tree_canvas = Canvas(self.tab_tree, bg="#1a1a1a", highlightthickness=0)
        self.tree_canvas.pack(fill="both", expand=True)

    def setup_nfa_tab(self):
        ctrl = ctk.CTkFrame(self.tab_nfa, fg_color="transparent")
        ctrl.pack(fill="x")
        ctk.CTkButton(ctrl, text="Zoom +", width=50, command=lambda: self.change_zoom("nfa", 0.1)).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(ctrl, text="Zoom -", width=50, command=lambda: self.change_zoom("nfa", -0.1)).pack(side="left", padx=5)
        
        f = ctk.CTkFrame(self.tab_nfa)
        f.pack(fill="both", expand=True)
        self.nfa_canvas = Canvas(f, bg="#1a1a1a", highlightthickness=0)
        self.nfa_canvas.pack(fill="both", expand=True)

    def setup_dfa_tab(self):
        ctrl = ctk.CTkFrame(self.tab_dfa, fg_color="transparent")
        ctrl.pack(fill="x")
        ctk.CTkButton(ctrl, text="Zoom +", width=50, command=lambda: self.change_zoom("dfa", 0.1)).pack(side="left", padx=5, pady=5)
        ctk.CTkButton(ctrl, text="Zoom -", width=50, command=lambda: self.change_zoom("dfa", -0.1)).pack(side="left", padx=5)
        
        f = ctk.CTkFrame(self.tab_dfa)
        f.pack(fill="both", expand=True)
        self.dfa_canvas = Canvas(f, bg="#1a1a1a", highlightthickness=0)
        vs = Scrollbar(f, orient="vertical", command=self.dfa_canvas.yview)
        hs = Scrollbar(f, orient="horizontal", command=self.dfa_canvas.xview)
        self.dfa_canvas.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)
        vs.pack(side="right", fill="y"); hs.pack(side="bottom", fill="x")
        self.dfa_canvas.pack(side="left", fill="both", expand=True)

    def change_zoom(self, target, delta):
        if target == "nfa":
            self.nfa_zoom = max(0.5, min(3.0, self.nfa_zoom + delta))
            self.draw_lexer_nfa()
        else:
            self.dfa_zoom = max(0.5, min(3.0, self.dfa_zoom + delta))
            self.draw_parser_dfa()

    def clear_inputs(self):
        self.code_input.delete("0.0", END)
        self.token_display.delete("0.0", END)
        for i in self.tree_table.get_children(): self.tree_table.delete(i)
        self.tree_canvas.delete("all"); self.nfa_canvas.delete("all"); self.dfa_canvas.delete("all")
        self.last_insts = []

    # --- Core Compiler Logic ---
    def lexer(self, code):
        tokens = []
        specs = [('MNEMONIC', r'\b(MOV|LEA|XCHG|PUSH|POP)\b'), ('REGISTER', r'\b(AX|BX|CX|DX|SI|DI|BP|SP|AL|BL|CL|DL|AH|BH|CH|DH)\b'),
                 ('NUMBER', r'\b\d+\b'), ('LBR', r'\['), ('RBR', r'\]'), ('COMMA', r','), ('NL', r'\n'), ('SKIP', r'[ \t]+'), ('ERR', r'.')]
        for ln, line in enumerate(code.split('\n'), 1):
            if not line.strip(): continue
            pos = 0
            while pos < len(line):
                match = None
                for t, p in specs:
                    reg = re.compile(p, re.I); match = reg.match(line, pos)
                    if match:
                        if t == 'ERR': return None, f"Lex Error: '{match.group()}' at line {ln}"
                        if t not in ['SKIP', 'NL']: tokens.append((t, match.group().upper(), ln))
                        pos = match.end(); break
                if not match: break
            tokens.append(('NEWLINE', '\\n', ln))
        tokens.append(('EOF', '$', 0))
        return tokens, None

    def get_op(self, tks):
        if not tks or tks[0][0] == 'EOF': return None, 0
        if tks[0][0] == 'LBR':
            if len(tks) >= 3 and tks[1][0] == 'REGISTER' and tks[2][0] == 'RBR':
                r = tks[1][1]; return {"v": f"[{r}]", "m": True, "s": 8 if r.endswith(('L','H')) else 16, "t": 'MEM'}, 3
            return None, 0
        r = tks[0][1]; sz = 8 if r.endswith(('L','H')) else 16
        return {"v": r, "m": False, "s": sz, "t": tks[0][0]}, 1

    def parser(self, tokens):
        stack, log, insts, i = ["$"], [], [], 0
        def add_log(a): log.append((" ".join(stack), " ".join([t[1] for t in tokens[i:i+6]]), a))
        while i < len(tokens):
            if tokens[i][0] == 'EOF': break
            if tokens[i][0] == 'NEWLINE': i += 1; continue
            ln = tokens[i][2]; mnem = tokens[i][1]
            stack.append(mnem); add_log(f"Shift {mnem}"); i += 1
            op1, c1 = self.get_op(tokens[i:])
            if not op1: return log, False, f"Err Line {ln}: Invalid Op1", []
            for _ in range(c1): stack.append(tokens[i][1]); i += 1
            add_log("Shift Op1")
            if mnem in ["PUSH", "POP"]:
                if mnem == "POP" and op1['t'] == 'NUMBER': return log, False, f"Semantic Line {ln}: POP Imm Invalid", []
                insts.append({"t": "S", "op": mnem, "d": op1['v']})
            else:
                if tokens[i][0] != 'COMMA': return log, False, f"Err Line {ln}: Missing Comma", []
                stack.append(","); add_log("Shift ,"); i += 1
                op2, c2 = self.get_op(tokens[i:])
                if not op2: return log, False, f"Err Line {ln}: Invalid Op2", []
                for _ in range(c2): stack.append(tokens[i][1]); i += 1
                add_log("Shift Op2")
                if mnem == "XCHG":
                    if op1['m'] and op2['m']: return log, False, f"Semantic Line {ln}: XCHG Mem-Mem Invalid", []
                    if op1['t'] == 'NUMBER' or op2['t'] == 'NUMBER': return log, False, f"Semantic Line {ln}: XCHG Imm Invalid", []
                    if op1['s'] != op2['s']: return log, False, f"Semantic Line {ln}: Size Mismatch", []
                if mnem == "LEA":
                    if op1['m'] or op1['t'] == 'NUMBER': return log, False, f"Semantic Line {ln}: LEA Dest must be Reg", []
                    if not op2['m']: return log, False, f"Semantic Line {ln}: LEA Src must be Mem", []
                insts.append({"t": "D", "op": mnem, "d": op1['v'], "s": op2['v']})
            stack = stack[:- (1 + c1 + (1 + c2 if mnem not in ["PUSH", "POP"] else 0))]; stack.append("<Inst>"); add_log("Reduce")
        stack = ["$", "<Prog>"]; add_log("ACCEPT"); return log, True, "Success", insts

    # --- Drawing with Zoom ---
    def draw_lexer_nfa(self):
        c = self.nfa_canvas; c.delete("all"); z = self.nfa_zoom
        states = [(150*z, 250*z, "q0"), (350*z, 100*z, "q1"), (350*z, 250*z, "q2"), (350*z, 400*z, "q3"), (550*z, 250*z, "q_acc")]
        for x, y, name in states:
            r = 30 * z
            c.create_oval(x-r, y-r, x+r, y+r, fill="#2c3e50", outline="white", width=2*z)
            c.create_text(x, y, text=name, fill="white", font=("Arial", int(10*z), "bold"))
        trans = [(0,1,"[A-Z]"), (0,2,"[A-Z]"), (0,3,"[0-9]"), (1,4,"\\s"), (2,4,"\\s/,"), (3,4,"\\s/,")]
        for f, t, lbl in trans:
            x1, y1, _ = states[f]; x2, y2, _ = states[t]; r = 30 * z
            c.create_line(x1+r, y1, x2-r, y2, fill="white", arrow="last", width=1.5*z)
            c.create_text((x1+x2)/2, (y1+y2)/2 - 15*z, text=lbl, fill="#bdc3c7", font=("Arial", int(9*z)))

    def draw_parser_dfa(self):
        c = self.dfa_canvas; c.delete("all"); z = self.dfa_zoom
        def box(x, y, items):
            w, h = 260*z, 110*z
            c.create_rectangle(x, y, x+w, y+h, fill="#2c3e50", outline="white", width=2.5*z)
            for idx, text in enumerate(items):
                c.create_text(x+15*z, y+25*z+(idx*25*z), text=text, fill="white", anchor="w", font=("Consolas", int(12*z), "bold"))
            return x, y, w, h
        s1 = box(50*z, 300*z, ["State I0:", "S' ::= .Prog", "Prog ::= .Inst"])
        s2 = box(400*z, 300*z, ["State I1:", "Inst ::= Mnem. Op1", "Inst ::= Mnem. Op1, Op2"])
        s3 = box(750*z, 150*z, ["State I2 (Acc):", "Inst ::= Mnem Op1 ."])
        s4 = box(750*z, 450*z, ["State I3:", "Inst ::= Mnem Op1 ., Op2"])
        s5 = box(1100*z, 450*z, ["State I4:", "Inst ::= Mnem Op1 ,. Op2"])
        s6 = box(1450*z, 450*z, ["State I5 (Acc):", "Inst ::= Mnem Op1 , Op2 ."])
        def arrow(b1, b2, lbl):
            x1, y1, w1, h1 = b1; x2, y2, w2, h2 = b2
            c.create_line(x1+w1, y1+h1/2, x2, y2+h2/2, fill="#e67e22", arrow="last", width=3*z)
            c.create_text(x1+w1+40*z, y1+h1/2 - 20*z, text=lbl, fill="#f39c12", font=("Arial", int(12*z), "bold"))
        arrow(s1, s2, "Mnemonic"); arrow(s2, s3, "Op1"); arrow(s2, s4, "Op1"); arrow(s4, s5, "Comma"); arrow(s5, s6, "Op2")
        c.config(scrollregion=(0,0, 1800*z, 800*z))

    def draw_tree(self, insts):
        c = self.tree_canvas; c.delete("all")
        if not insts: return
        rx, ry = 600, 60
        c.create_oval(rx-35, ry-25, rx+35, ry+25, fill="#e74c3c", outline="white")
        c.create_text(rx, ry, text="Prog", fill="white", font=("Arial", 10, "bold"))
        for idx, ins in enumerate(insts):
            ix, iy = 150 + idx*280, 180
            c.create_line(rx, ry+25, ix, iy-25, fill="white", width=2)
            c.create_oval(ix-35, iy-25, ix+35, iy+25, fill="#9b59b6", outline="white")
            c.create_text(ix, iy, text="Inst", fill="white", font=("Arial", 10, "bold"))
            c.create_line(ix, iy+25, ix-70, 280, fill="#bdc3c7")
            c.create_text(ix-70, 300, text=ins['op'], fill="#2ecc71", font=("Consolas", 11, "bold"))
            c.create_line(ix, iy+25, ix, 280, fill="#bdc3c7")
            c.create_text(ix, 300, text=ins['d'], fill="#3498db", font=("Consolas", 11, "bold"))
            if ins['t'] == "D":
                c.create_line(ix, iy+25, ix+70, 280, fill="#bdc3c7")
                c.create_text(ix+70, 300, text=ins['s'], fill="#f1c40f", font=("Consolas", 11, "bold"))

    def run_analysis(self):
        code = self.code_input.get("0.0", END).strip()
        if not code: return
        tokens, err = self.lexer(code)
        if err: messagebox.showerror("Lex Error", err); return
        self.token_display.delete("0.0", END)
        for t in tokens: self.token_display.insert(END, f"{t}\n")
        for i in self.tree_table.get_children(): self.tree_table.delete(i)
        logs, ok, msg, self.last_insts = self.parser(tokens)
        for r in logs: self.tree_table.insert("", "end", values=r)
        if not ok: messagebox.showerror("Error", msg); return
        self.draw_tree(self.last_insts); self.draw_lexer_nfa(); self.draw_parser_dfa()
        self.tabview.set("Parse Table")

if __name__ == "__main__":
    app = AssemblyCompilerApp()
    app.mainloop()