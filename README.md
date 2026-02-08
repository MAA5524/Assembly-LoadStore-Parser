# 🛠️ Assembly Load/Store Parser & Visualizer

A modern, Python-based compiler simulator designed to analyze and visualize **x86 Load/Store instructions**. This tool performs lexical analysis, simulates a bottom-up **Shift-Reduce parser**, and renders a dynamic **Graphical Parse Tree**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![UI](https://img.shields.io/badge/UI-CustomTkinter-orange.svg)
![Parser](https://img.shields.io/badge/Parser-Shift--Reduce-green.svg)

## 🚀 Features

*   **Multi-Line Parsing:** Analyze entire assembly blocks, not just single lines.
*   **Instruction Support:** Full support for `MOV`, `PUSH`, `POP`, `XCHG`, and `LEA`.
*   **Graphical Parse Tree:** Real-time rendering of the derivation tree using a colored Canvas with horizontal/vertical scrolling.
*   **Step-by-Step Parse Table:** A detailed `Treeview` table showing the **Stack Content**, **Input Buffer**, and **Action Taken** at every step.
*   **Instruction Builder:** A GUI-based tool to generate valid assembly code without manual typing errors.
*   **Semantic Validation:** Specialized logic for `XCHG` instructions:
    *   ❌ Prevents Memory-to-Memory transfers.
    *   ❌ Prevents use of Immediate data (numbers) in XCHG.
    *   ✅ Validates register size matching (e.g., 8-bit vs 16-bit).

## 📋 Supported Instruction Set

| Mnemonic | Description | Example |
| :--- | :--- | :--- |
| **MOV** | Data transfer between reg/mem/imm | `MOV AX, 10` |
| **PUSH** | Store operand onto the stack | `PUSH AX` |
| **POP** | Load operand from the stack | `POP BX` |
| **XCHG** | Exchange contents of two operands | `XCHG AX, BX` |
| **LEA** | Load Effective Address | `LEA SI, [BX]` |

## 🏗️ Grammar (CFG)

The parser is based on the following Context-Free Grammar:

```bnf
<Program>     ::= <StmtList>
<StmtList>    ::= <Instruction> NEWLINE <StmtList> | <Instruction>
<Instruction> ::= <DualOp> | <SingleOp>
<DualOp>      ::= <OpCode2> <Dest> , <Source>
<SingleOp>    ::= <OpCode1> <Operand>
<OpCode2>     ::= MOV | XCHG | LEA
<OpCode1>     ::= PUSH | POP
<Dest>        ::= <Register> | <Memory>
<Source>      ::= <Register> | <Memory> | <Number>
<Register>    ::= AX | BX | CX | DX | AL | BL ...
<Memory>      ::= [ <Register> ]
```

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MAA5524/Assembly-LoadStore-Parser.git
   cd Assembly-LoadStore-Parser
   ```

2. **Install dependencies:**
   This project requires `customtkinter`.
   ```bash
   pip install customtkinter
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## 🖥️ How to Use

1. **Code Builder:** Use the dropdown menus to select an operation and operands. Click **"ADD LINE"** to insert it into the editor.
2. **Editor:** You can also manually type or edit your assembly code in the text area.
3. **Analysis:** Click **"RUN ANALYSIS"**.
4. **Lexical Tab:** View the generated tokens (Mnemonic, Register, Comma, etc.).
5. **Parse Table:** Observe how the Stack evolves and which Shift/Reduce actions are triggered.
6. **Parse Tree:** Explore the hierarchical structure of your program in the graphical tree view.

## 🤖 Technical Implementation

*   **Lexical Analyzer (Lexer):** Uses Regular Expressions (Regex) to tokenize the input stream.
*   **Syntax Analyzer (Parser):** Implements a recursive-descent approach to handle multi-line programs, combined with a stack-based simulation to visualize Shift-Reduce transitions.
*   **UI Framework:** Built with `CustomTkinter` for a professional dark-themed experience and `Tkinter.Canvas` for high-performance tree rendering.

## 🤝 Author
**MAA5524**  
*Computer Science / Compiler Design Project*

---
*If you find this project helpful, feel free to ⭐ the repository!*