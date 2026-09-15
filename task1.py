import sys

DEBUG_MODE = False

class Node:
    def __init__(self, parent=0, char_to_parent="#"):
        self.son = [-1] * 5
        self.go = [-1] * 5
        self.parent = parent
        self.char_to_parent = char_to_parent
        self.suff_link = None
        self.up = None
        self.is_leaf = False
        self.leaf_pattern_numbers = []

class AhoCorasick:
    def __init__(self):
        self.root = 0
        self.bor = [Node()]
        self.bor[self.root].suff_link = self.root
        self.bor[self.root].up = self.root
        self.pattern_lengths = [0]
        self.char_to_index = {"A": 0, "C": 1, "G": 2, "T": 3, "N": 4}
        self.index_to_char = ["A", "C", "G", "T", "N"]

    def get_char_index(self, char):
        return self.char_to_index[char]

    def get_suff_link(self, v):
        if self.bor[v].suff_link is None:
            parent = self.bor[v].parent
            if v == self.root or parent == self.root:
                self.bor[v].suff_link = self.root
            else:
                parent_suff = self.get_suff_link(parent)
                char_to_parent = self.bor[v].char_to_parent
                self.bor[v].suff_link = self.get_link(parent_suff, char_to_parent)
        return self.bor[v].suff_link

    def get_link(self, v, char):
        char_index = self.get_char_index(char)
        if self.bor[v].go[char_index] == -1:
            if self.bor[v].son[char_index] != -1:
                self.bor[v].go[char_index] = self.bor[v].son[char_index]
            elif v == self.root:
                self.bor[v].go[char_index] = self.root
            else:
                suff_link = self.get_suff_link(v)
                self.bor[v].go[char_index] = self.get_link(suff_link, char)
        return self.bor[v].go[char_index]

    def get_up(self, v):
        if self.bor[v].up is None:
            suff_link = self.get_suff_link(v)
            if self.bor[suff_link].is_leaf:
                self.bor[v].up = suff_link
            elif suff_link == self.root:
                self.bor[v].up = self.root
            else:
                self.bor[v].up = self.get_up(suff_link)
        return self.bor[v].up

    def add_string(self, string, pattern_number):
        if DEBUG_MODE:
            print(f"добавляем образец {pattern_number}: {string}")
        cur = self.root
        for char in string:
            char_index = self.get_char_index(char)
            if self.bor[cur].son[char_index] == -1:
                self.bor[cur].son[char_index] = len(self.bor)
                self.bor.append(Node(cur, char))
                if DEBUG_MODE:
                    print(f"  символ {char}: новая вершина {len(self.bor) - 1}")
            else:
                if DEBUG_MODE:
                    print(f"  символ {char}: переход в вершину {self.bor[cur].son[char_index]}")
            cur = self.bor[cur].son[char_index]
        self.bor[cur].is_leaf = True
        self.bor[cur].leaf_pattern_numbers.append(pattern_number)
        while len(self.pattern_lengths) <= pattern_number:
            self.pattern_lengths.append(0)
        self.pattern_lengths[pattern_number] = len(string)
        if DEBUG_MODE:
            print(f"  образец {pattern_number} завершён в вершине {cur}")

    def print_bor(self):
        if not DEBUG_MODE:
            return
        print("\nБОР")
        for v, node in enumerate(self.bor):
            edges = []
            for i in range(5):
                to = node.son[i]
                if to != -1:
                    edges.append(f"{self.index_to_char[i]}->{to}")
            edges_text = " ".join(edges) if edges else "-"
            patterns_info = f", образцы={node.leaf_pattern_numbers}" if node.leaf_pattern_numbers else ""
            print(f"вершина {v}: переходы: {edges_text}{patterns_info}")

    def print_links(self):
        if not DEBUG_MODE:
            return
        print("\nИТОГОВЫЕ ССЫЛКИ")
        for v in range(len(self.bor)):
            suff = self.get_suff_link(v)
            up = self.get_up(v)
            print(f"вершина {v}: суфф={suff}; конечная={up}")

    def print_automaton(self):
        if not DEBUG_MODE:
            return
        print("\nОПИСАНИЕ КАЖДОЙ ВЕРШИНЫ АВТОМАТА")
        for v, node in enumerate(self.bor):
            edges = []
            for i in range(5):
                to = node.son[i]
                if to != -1:
                    edges.append(f"{self.index_to_char[i]}->{to}")
            edges_text = " ".join(edges) if edges else "-"
            print(f"вершина {v}: переходы=[{edges_text}], suff={self.get_suff_link(v)}, term={self.get_up(v)}, patterns={node.leaf_pattern_numbers}")

    def process_text(self, text):
        result = []
        cur = self.root
        
        if DEBUG_MODE:
            print("\nПРОЦЕСС ИСПОЛЬЗОВАНИЯ АВТОМАТА")
            print(f"текст: {text}")
        
        for i, char in enumerate(text):
            old_cur = cur
            cur = self.get_link(cur, char)
            
            if DEBUG_MODE:
                print(f"позиция {i + 1} ({char}): {old_cur} -> {cur}")
            
            if self.bor[cur].is_leaf:
                for pattern_number in self.bor[cur].leaf_pattern_numbers:
                    start_position = i - self.pattern_lengths[pattern_number] + 2
                    result.append((start_position, pattern_number))
                    if DEBUG_MODE:
                        print(f"  найдено: позиция {start_position}, образец {pattern_number}")
            
            up_vertex = self.get_up(cur)
            while up_vertex != self.root:
                for pattern_number in self.bor[up_vertex].leaf_pattern_numbers:
                    start_position = i - self.pattern_lengths[pattern_number] + 2
                    result.append((start_position, pattern_number))
                    if DEBUG_MODE:
                        print(f"  найдено по конечной ссылке: позиция {start_position}, образец {pattern_number}")
                up_vertex = self.get_up(up_vertex)
        
        result.sort()
        return result

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    text = data[0]
    n = int(data[1])
    patterns = data[2:2+n]
    
    if DEBUG_MODE:
        print("=== ВХОДНЫЕ ДАННЫЕ ===")
        print(f"текст: {text}")
        print(f"количество шаблонов: {n}")
        for i, p in enumerate(patterns, 1):
            print(f"  шаблон {i}: {p}")
        print()
        print("=== ПОСТРОЕНИЕ БОРА ===")
    
    aho = AhoCorasick()
    for i in range(n):
        pattern = patterns[i]
        aho.add_string(pattern, i + 1)
    
    aho.print_bor()
    aho.print_links()
    aho.print_automaton()
    
    answer = aho.process_text(text)
    
    if DEBUG_MODE:
        print("\n=== ОТВЕТ ===")
    
    for position, pattern_number in answer:
        print(position, pattern_number)

if __name__ == "__main__":
    main()