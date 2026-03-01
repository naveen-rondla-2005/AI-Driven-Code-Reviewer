import ast
import re
import textwrap

class CodeScorer(ast.NodeVisitor):
    """
    Advanced AST-based Python Code Quality Analyzer.
    Evaluates naming, structure, usage, cleanliness, and formatting.
    """
    def __init__(self, original_code):
        self.original_code = textwrap.dedent(original_code).strip()
        
        # Categorized tracking with line numbers
        self.defined_imports = {}   # {name: lineno}
        self.defined_classes = set()
        self.defined_functions = set()
        self.defined_vars = set()
        self.used_names = set() 
        
        # Violations & Warnings
        self.naming_violations = [] 
        self.infinite_loops = []
        self.params = set()

        # Metrics for scoring
        self.total_functions = 0
        self.snake_case_funcs = 0
        self.total_classes = 0
        self.pascal_case_classes = 0
        self.functions_short_args = True 
        self.functions_short_lines = 0

    def visit_Import(self, node):
        for alias in node.names:
            self.defined_imports[alias.asname or alias.name] = node.lineno
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.defined_imports[alias.asname or alias.name] = node.lineno
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.total_classes += 1
        self.defined_classes.add(node.name)
        if re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name): 
            self.pascal_case_classes += 1
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.total_functions += 1
        if not node.name.startswith('__'): 
            self.defined_functions.add(node.name)
        
        for arg in node.args.args:
            p_name = arg.arg
            if p_name != 'self':
                self.params.add(p_name)
                if len(p_name) < 4 and p_name not in ['i', 'j', 'k', '_']:
                    msg = f"Argument '{p_name}' at line {node.lineno} is too short. Use a descriptive name."
                    if msg not in self.naming_violations:
                        self.naming_violations.append(msg)
            
        if re.match(r'^[a-z_][a-z0-9_]*$', node.name): 
            self.snake_case_funcs += 1
        
        start, end = node.lineno, getattr(node, 'end_lineno', node.lineno)
        if (end - start) <= 40: self.functions_short_lines += 1
        if len(node.args.args) > 5: self.functions_short_args = False
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name): 
            self.used_names.add(node.func.id)
        elif isinstance(node.func, ast.Attribute): 
            self.used_names.add(node.func.attr)
        self.generic_visit(node)

    def visit_While(self, node):
        if isinstance(node.test, ast.Constant) and bool(node.test.value) is True:
            has_break = any(isinstance(child, ast.Break) for child in ast.walk(node))
            if not has_break:
                self.infinite_loops.append(node.lineno)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            if node.id not in self.defined_classes and node.id not in self.defined_functions:
                self.defined_vars.add(node.id)
            
            is_loop_var = node.id in ['i', 'j', 'k', '_']
            if len(node.id) < 4 and not (is_loop_var or node.id in self.params):
                msg = f"Variable '{node.id}' at line {node.lineno} is too short. Use descriptive names."
                if msg not in self.naming_violations:
                    self.naming_violations.append(msg)
        
        elif isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        self.generic_visit(node)

    def calculate_final_score(self):
        category_scores = {
            "Naming Standards": 0,
            "Code Structure": 0,
            "Logic Utilization": 0,
            "Cleanliness (Usage)": 0,
            "Quality & Formatting": 0
        }
        breakdown = {"Gained": [], "Lost": []}

        # 1. Naming Standards (20 pts)
        f_pts = (self.snake_case_funcs / self.total_functions * 10) if self.total_functions > 0 else 10
        c_pts = (self.pascal_case_classes / self.total_classes * 10) if self.total_classes > 0 else 10
        category_scores["Naming Standards"] = round(f_pts + c_pts)

        # 2. Code Structure (20 pts)
        s_pts = 10 if self.functions_short_args else 0
        l_pts = (self.functions_short_lines / self.total_functions * 10) if self.total_functions > 0 else 10
        category_scores["Code Structure"] = round(s_pts + l_pts)

        # 3. Logic Utilization (20 pts)
        u_classes = self.defined_classes - self.used_names
        u_funcs = self.defined_functions - self.used_names
        logic_pts = 20
        if u_classes: 
            logic_pts -= 10
            breakdown["Lost"].append(f"Logic: Class '{list(u_classes)}' defined but never instantiated.")
        if u_funcs: 
            logic_pts -= 10
            breakdown["Lost"].append(f"Logic: Function '{list(u_funcs)}' defined but never called.")
        category_scores["Logic Utilization"] = max(0, logic_pts)

        # 4. Cleanliness (20 pts)
        unused_imports = set(self.defined_imports.keys()) - self.used_names
        u_vars = (self.defined_vars | self.params) - self.used_names
        clean_pts = 20
        if unused_imports:
            clean_pts -= 10
            for imp in unused_imports:
                breakdown["Lost"].append(f"Import: Unused '{imp}' at line {self.defined_imports[imp]}. (Action: Try to Remove or use {imp} library in your code)")
        if u_vars:
            clean_pts -= 10
            breakdown["Lost"].append(f"Variable: Unused items detected: {u_vars}")
        category_scores["Cleanliness (Usage)"] = max(0, clean_pts)

        # 5. Formatting & Quality (20 pts)
        v_pts = 10 if not self.naming_violations else 0 
        space_pts = 10
        for line in self.original_code.split('\n'):
            if line.strip() and (len(line) - len(line.lstrip())) % 4 != 0:
                space_pts = 0; break
        
        quality_pts = v_pts + space_pts
        if self.infinite_loops: 
            quality_pts = 0 
            breakdown["Lost"].append(f"Critical: Potential infinite loop at line(s) {self.infinite_loops}")
        
        category_scores["Formatting & Quality"] = max(0, quality_pts)

        # Final Polish
        for v in self.naming_violations: breakdown["Lost"].append(f"Naming: {v}")
        if space_pts < 10: breakdown["Lost"].append("Formatting: Indentation must be exactly 4 spaces.")

        final_score = sum(category_scores.values())
        return final_score, category_scores, breakdown

# --- Example Driver Code ---
code_to_review = """

class MyCalculator:
    def solve(self, num1, num2):
        result = num1 + num2
        return result

calc = MyCalculator()
print(calc.solve(10, 20))
"""

try:
    clean_code = textwrap.dedent(code_to_review).strip()
    tree = ast.parse(clean_code)
    scorer = CodeScorer(code_to_review)
    scorer.visit(tree)
    
    score, cat_scores, report = scorer.calculate_final_score()

    print(f"\n{'='*40}")
    print(f" 🏆 CODE QUALITY SCORECARD 🏆 ")
    print(f"{'='*40}")
    for category, pts in cat_scores.items():
        print(f" {category.ljust(28)}: {pts}/20")
    print(f"{'-'*40}")
    print(f" {'OVERALL SCORE'.ljust(28)}: {score}/100")
    print(f"{'='*40}\n")

    if report["Lost"]:
        print("❌ SUGGESTIONS TO IMPROVE SCORE:")
        for item in report["Lost"]: print(f"  - {item}")
    else:
        print("🔥 PERFECT SCORE! Your code follows all professional standards.")

except Exception as e:
    print(f"Critical Error during analysis: {e}")
