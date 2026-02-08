import customtkinter as ctk
from tkinter import END, Canvas, Scrollbar, ttk
import re

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AssemblyCompilerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Multi-Line Assembly Compiler")
        self.geometry("1300x850")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Compiler Project", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.lbl_info = ctk.CTkLabel(self.sidebar_frame, text="Analyzing:\nStack, Input, Action", text_color="#aab7b8", justify="left")
        self.lbl_info.grid(row=1, column=0, padx=20, pady=10)

        self.analyze_btn = ctk.CTkButton(self.sidebar_frame, text="RUN ANALYSIS", command=self.run_analysis, fg_color="#27ae60", hover_color="#2ecc71")
        self.analyze_btn.grid(row=2, column=0, padx=20, pady=20)

        self.clear_btn = ctk.CTkButton(self.sidebar_frame, text="CLEAR ALL", command=self.clear_inputs, fg_color="#c0392b", hover_color="#e74c3c")
        self.clear_btn.grid(row=3, column=0, padx=20, pady=10)

        self.tabview = ctk.CTkTabview(self, width=1000)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.tab_input = self.tabview.add("Code Editor")
        self.tab_tokens = self.tabview.add("Lexical")
        self.tab_parser = self.tabview.add("Parse Table")
        self.tab_tree = self.tabview.add("Full Parse Tree")

        self.setup_input_tab()
        self.setup_token_tab()
        self.setup_parser_tab()
        self.setup_tree_tab()

    def setup_input_tab(self):
        self.tab_input.grid_columnconfigure(0, weight=1)
        self.tab_input.grid_rowconfigure(2, weight=1)

        builder_frame = ctk.CTkFrame(self.tab_input, fg_color="#2c3e50", corner_radius=10)
        builder_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        builder_frame.grid_columnconfigure((0,1,2,3), weight=1)

        ctk.CTkLabel(builder_frame, text="Instruction Builder", font=("Arial", 16, "bold"), text_color="#3498db").grid(row=0, column=0, columnspan=4, pady=10)

        self.cmb_mnemonic = ctk.CTkOptionMenu(builder_frame, values=["MOV", "XCHG", "LEA", "PUSH", "POP"], command=self.update_ui, fg_color="#2980b9")
        self.cmb_mnemonic.grid(row=1, column=0, padx=10, pady=5)
        self.cmb_mnemonic.set("MOV")

        self.cmb_dest = ctk.CTkOptionMenu(builder_frame, values=["AX", "BX", "CX", "DX", "AL", "BL", "[BX]"], fg_color="#2980b9")
        self.cmb_dest.grid(row=1, column=1, padx=10, pady=5)

        self.src_frame = ctk.CTkFrame(builder_frame, fg_color="transparent")
        self.src_frame.grid(row=1, column=2, padx=10, pady=5)
        self.entry_src = ctk.CTkEntry(self.src_frame, placeholder_text="10 or BX", width=80)
        self.entry_src.pack()

        self.btn_add = ctk.CTkButton(builder_frame, text="ADD LINE", command=self.add_line, fg_color="#d35400")
        self.btn_add.grid(row=1, column=3, padx=10)

        self.code_input = ctk.CTkTextbox(self.tab_input, height=200, font=("Consolas", 18))
        self.code_input.insert("0.0", "MOV AX, 10\nXCHG AX, BX\nXCHG AX, [BX]")
        self.code_input.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

    def update_ui(self, choice):
        if choice in ["PUSH", "POP"]: self.src_frame.grid_remove()
        else: self.src_frame.grid()

    def add_line(self):
        mnem = self.cmb_mnemonic.get()
        dest = self.cmb_dest.get()
        if mnem in ["PUSH", "POP"]: line = f"{mnem} {dest}\n"
        else:
            src = self.entry_src.get().upper() or "AX"
            line = f"{mnem} {dest}, {src}\n"
        self.code_input.insert(END, line)

    def setup_token_tab(self):
        self.token_display = ctk.CTkTextbox(self.tab_tokens, font=("Consolas", 14))
        self.token_display.pack(expand=True, fill="both", padx=10, pady=10)

    def setup_parser_tab(self):
        table_frame = ctk.CTkFrame(self.tab_parser, fg_color="transparent")
        table_frame.pack(expand=True, fill="both", padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", fieldbackground="#2b2b2b", foreground="white", rowheight=50, font=("Consolas", 11))
        style.configure("Treeview.Heading", background="#34495e", foreground="white", font=("Arial", 12, "bold"))
        style.map("Treeview", background=[('selected', '#2980b9')])

        columns = ("stack", "input", "action")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("stack", text="Stack Content")
        self.tree.heading("input", text="Input Buffer")
        self.tree.heading("action", text="Action Taken")
        
        self.tree.column("stack", width=450, minwidth=400, anchor="w")
        self.tree.column("input", width=400, minwidth=350, anchor="w")
        self.tree.column("action", width=250, minwidth=200, anchor="w")

        v_scroll = ctk.CTkScrollbar(table_frame, orientation="vertical", command=self.tree.yview)
        h_scroll = ctk.CTkScrollbar(table_frame, orientation="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

    def setup_tree_tab(self):
        self.tree_frame = ctk.CTkFrame(self.tab_tree)
        self.tree_frame.pack(expand=True, fill="both", padx=5, pady=5)
        self.v_scroll = Scrollbar(self.tree_frame, orient="vertical")
        self.h_scroll = Scrollbar(self.tree_frame, orient="horizontal")
        self.canvas = Canvas(self.tree_frame, bg="#2b2b2b", highlightthickness=0, yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        self.v_scroll.config(command=self.canvas.yview)
        self.h_scroll.config(command=self.canvas.xview)
        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", expand=True, fill="both")

    def clear_inputs(self):
        self.code_input.delete("0.0", END)
        self.token_display.delete("0.0", END)
        for item in self.tree.get_children(): self.tree.delete(item)
        self.canvas.delete("all")

    def lexer(self, code):
        tokens = []
        token_specs = [
            ('MNEMONIC', r'\b(MOV|LEA|XCHG|PUSH|POP)\b'),
            ('REGISTER', r'\b(AX|BX|CX|DX|SI|DI|BP|SP|AL|BL|CL|DL|AH|BH|CH|DH)\b'),
            ('NUMBER',   r'\b\d+\b'),
            ('LBRACK',   r'\['),
            ('RBRACK',   r'\]'),
            ('COMMA',    r','),
            ('NEWLINE',  r'\n'),
            ('SKIP',     r'[ \t]+'),
            ('MISMATCH', r'.'),
        ]
        code = code.upper().strip()
        pos = 0
        while pos < len(code):
            match = None
            for token_type, pattern in token_specs:
                regex = re.compile(pattern)
                match = regex.match(code, pos)
                if match:
                    if token_type != 'SKIP': tokens.append((token_type, match.group(0)))
                    pos = match.end()
                    break
            if not match: return None, "Unknown Token"
        tokens.append(('EOF', '$'))
        return tokens, None

    def parser_recursive(self, tokens):
        log = []
        stack = ["$"]
        input_buffer = [t[1] for t in tokens]
        parsed_instructions = []

        def log_step(action):
            s_val = " ".join(stack)
            i_val = " ".join(input_buffer)
            log.append((s_val, i_val, action))

        def get_op_info(tks):
            if not tks: return None, 0
            if tks[0][0] == 'LBRACK':
                if len(tks) >= 3 and tks[1][0] == 'REGISTER' and tks[2][0] == 'RBRACK':
                    val = f"[{tks[1][1]}]"
                    is_mem = True
                    reg = tks[1][1]
                    consumed = 3
                else: return None, 0
            else:
                val = tks[0][1]
                is_mem = False
                reg = val if tks[0][0] == 'REGISTER' else None
                consumed = 1
            
            size = 8 if reg and reg.endswith(('L', 'H')) else 16
            return {"val": val, "is_mem": is_mem, "size": size, "type": tks[0][0]}, consumed

        def parse_single_instruction(local_tokens):
            if not local_tokens: return None, "Empty"
            op_code = local_tokens[0][1]
            
            if op_code in ["PUSH", "POP"]:
                op1, _ = get_op_info(local_tokens[1:])
                if not op1: return None, "Invalid Operand"
                return {"type": "SINGLE", "op": op_code, "dest": op1['val']}, "OK"
            
            idx = 1
            dest, consumed = get_op_info(local_tokens[idx:])
            if not dest: return None, "Invalid Destination"
            idx += consumed
            
            if idx >= len(local_tokens) or local_tokens[idx][0] != 'COMMA': return None, "Missing Comma"
            idx += 1
            
            src, consumed = get_op_info(local_tokens[idx:])
            if not src: return None, "Invalid Source"
            
            if op_code == "XCHG":
                if dest['is_mem'] and src['is_mem']: return None, "XCHG: Mem-to-Mem Invalid"
                if dest['type'] == 'NUMBER' or src['type'] == 'NUMBER': return None, "XCHG: Immediate Invalid"
                if dest['size'] != src['size']: return None, "XCHG: Size Mismatch"
            
            return {"type": "DUAL", "op": op_code, "dest": dest['val'], "src": src['val']}, "OK"

        try:
            current_line_tokens = []
            while len(input_buffer) > 0:
                current_token_obj = tokens.pop(0)
                token_val = input_buffer.pop(0)
                if current_token_obj[0] == 'EOF':
                    if current_line_tokens:
                        data, msg = parse_single_instruction(current_line_tokens)
                        if not data: return log, False, msg, []
                        parsed_instructions.append(data)
                        stack.append("<Inst>")
                        log_step("Reduce -> <Inst>")
                    stack = ["$", "<Prog>"]
                    log_step("Reduce -> <Prog>")
                    log_step("ACCEPT")
                    return log, True, "SUCCESS", parsed_instructions
                elif current_token_obj[0] == 'NEWLINE':
                    if current_line_tokens:
                        data, msg = parse_single_instruction(current_line_tokens)
                        if not data: return log, False, msg, []
                        parsed_instructions.append(data)
                        stack.append("\\N")
                        log_step("Reduce -> <Inst>")
                        current_line_tokens = []
                else:
                    current_line_tokens.append(current_token_obj)
                    stack.append(token_val)
                    log_step(f"Shift {token_val}")
        except Exception as e: return log, False, str(e), []
        return log, False, "Error", []

    def draw_node(self, x, y, text, color="#3498db"):
        r = 25
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="white", width=2)
        self.canvas.create_text(x, y, text=text, fill="white", font=("Arial", 9, "bold"))
        return x, y, r

    def connect(self, p, c):
        self.canvas.create_line(p[0], p[1]+p[2], c[0], c[1]-c[2], fill="white", width=2)

    def draw_full_tree(self, instructions):
        self.canvas.delete("all")
        width = max(1000, len(instructions) * 250)
        self.canvas.config(scrollregion=(0, 0, width, 800))
        root_x, root_y = width // 2, 50
        root = self.draw_node(root_x, root_y, "<Prog>", "#e74c3c")
        y_instr, spacing = 150, width // (len(instructions) + 1)
        for i, data in enumerate(instructions):
            x_base = spacing * (i + 1)
            instr_node = self.draw_node(x_base, y_instr, "<Inst>", "#9b59b6")
            self.connect(root, instr_node)
            y_d, y_v = 250, 350
            if data['type'] == 'SINGLE':
                op_n = self.draw_node(x_base - 40, y_d, data['op'], "#2ecc71")
                dest_n = self.draw_node(x_base + 40, y_d, "<Dest>", "#3498db")
                val_n = self.draw_node(x_base + 40, y_v, data['dest'], "#2ecc71")
                self.connect(instr_node, op_n); self.connect(instr_node, dest_n); self.connect(dest_n, val_n)
            else:
                op_n = self.draw_node(x_base - 60, y_d, data['op'], "#2ecc71")
                dest_n = self.draw_node(x_base, y_d, "<Dest>", "#3498db")
                dest_v = self.draw_node(x_base, y_v, data['dest'], "#2ecc71")
                src_n = self.draw_node(x_base + 60, y_d, "<Src>", "#3498db")
                src_v = self.draw_node(x_base + 60, y_v, data['src'], "#2ecc71")
                self.connect(instr_node, op_n); self.connect(instr_node, dest_n); self.connect(dest_n, dest_v); self.connect(instr_node, src_n); self.connect(src_n, src_v)

    def run_analysis(self):
        code = self.code_input.get("0.0", END).strip()
        if not code: return
        self.token_display.delete("0.0", END)
        tokens, err = self.lexer(code)
        if err: return
        for t in tokens: self.token_display.insert(END, f"[{t[0]}] {t[1].replace('\\n','\\\\n')}\n")
        for item in self.tree.get_children(): self.tree.delete(item)
        logs, success, msg, parsed_data = self.parser_recursive(tokens)
        for row in logs: self.tree.insert("", "end", values=row)
        if success:
            self.draw_full_tree(parsed_data)
            self.tabview.set("Full Parse Tree")
        else: self.tabview.set("Parse Table")

if __name__ == "__main__":
    app = AssemblyCompilerApp()
    app.mainloop()