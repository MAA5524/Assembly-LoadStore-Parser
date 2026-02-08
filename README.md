This is the updated **README.md** file for your GitHub repository. It now includes the advanced features we added, such as **Automata Visualization (NFA/DFA)**, **Zooming functionality**, and **Strict Semantic Validation**.

---

# 🛠️ Pro Assembly Load/Store Parser & Automata Visualizer

An advanced, Python-based compiler engine designed to analyze and visualize **x86 Load/Store instructions**. This tool goes beyond simple parsing by offering **Lexer NFA** and **LR Parser DFA** visualizations, alongside a robust **Shift-Reduce** simulation.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![UI](https://img.shields.io/badge/UI-CustomTkinter-orange.svg)
![Automata](https://img.shields.io/badge/Automata-NFA%20%26%20DFA-red.svg)
![Parser](https://img.shields.io/badge/Parser-Shift--Reduce-green.svg)

## 🚀 Key Features

*   **Multi-Line Parsing:** Fully analyzes complex assembly blocks with recursive program handling.
*   **Automata Visualization:** 
    *   **Lexer NFA:** Visualizes the Non-deterministic Finite Automata used for token recognition.
    *   **Parser DFA:** Renders the LR(0) State Machine (DFA) showing Item Sets and transitions.
*   **Dynamic Zooming System:** Integrated **Zoom +** and **Zoom -** buttons for NFA and DFA diagrams to handle complex visualizations.
*   **Graphical Parse Tree:** Real-time rendering of the derivation tree with a dedicated root-to-leaf colored structure.
*   **Professional Parse Table:** A high-fidelity `Treeview` table displaying the **Stack**, **Input Buffer**, and **Parser Actions** with optimized row spacing for readability.
*   **Strict Semantic Validation:**
    *   **XCHG Logic:** Prevents Mem-to-Mem transfers, Immediate data usage, and Register size mismatches (e.g., 8-bit vs 16-bit).
    *   **LEA Logic:** Ensures destination is a Register and source is a Memory address.
    *   **POP Logic:** Prevents popping values directly into Immediate (Number) operands.

## 📋 Supported Instruction Set

| Mnemonic | Description | Strict Rules |
| :--- | :--- | :--- |
| **MOV** | Data transfer | Standard x86 rules |
| **PUSH** | Store onto stack | Reg/Mem/Imm supported |
| **POP** | Load from stack | Destination cannot be Immediate |
| **XCHG** | Swap contents | No Mem-to-Mem, No Imm, Size must match |
| **LEA** | Load Effective Address | Dest: Reg only, Src: Mem only |

## 🏗️ Grammar (CFG)

The system is built upon a recursive Context-Free Grammar:

```bnf
<Program>      ::= <StmtList>
<StmtList>     ::= <Instruction> NEWLINE <StmtList> | <Instruction>
<Instruction>  ::= <DualOp> | <SingleOp>
<DualOp>       ::= <OpCode2> <Dest> , <Source>
<SingleOp>     ::= <OpCode1> <Operand>
<OpCode2>      ::= MOV | XCHG | LEA
<OpCode1>      ::= PUSH | POP
<Dest/Source>  ::= <Register> | <Memory> | <Number>
<Register>     ::= AX, BX, CX, DX, AL, BL, SI, DI...
<Memory>       ::= [ <Register> ]
```

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MAA5524/Assembly-LoadStore-Parser.git
   cd Assembly-LoadStore-Parser
   ```

2. **Install dependencies:**
   ```bash
   pip install customtkinter
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## 🖥️ How to Use

1. **Code Editor:** Type your assembly code or use the **Instruction Builder** to insert valid lines.
2. **Analysis:** Click **"RUN ANALYSIS"**.
3. **Tabs Exploration:**
    *   **Lexical:** Check the token stream.
    *   **Parse Table:** See the Shift-Reduce stack transitions.
    *   **Parse Tree:** View the hierarchical program structure.
    *   **Lexer NFA:** Explore the token recognition states.
    *   **Parser DFA:** Study the LR state machine (Use **Zoom** for details).

## 🤖 Technical Implementation

*   **Lexer:** Built with Python `re` (Regex) module, simulating an NFA-based scanner.
*   **Parser:** Implements a bottom-up Shift-Reduce logic with recursive multi-line statement handling.
*   **Visualization Engine:** Custom-built zooming and scaling engine using `Tkinter.Canvas` for vector-like drawing of nodes and transitions.
*   **GUI:** Powered by `CustomTkinter` for a modern, responsive Dark-themed interface.

## 🤝 Author
**MAA5524**  
*Computer Science / Compiler Design & Automata Theory Project*

---
*If you find this project helpful, feel free to ⭐ the repository!*