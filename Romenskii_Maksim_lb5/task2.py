import sys

DEBUG_MODE = False

class Node:
    def __init__(self):
        self.son = [-1] * 5
        self.fail = 0
        self.out = -1
        self.offsets = []
        self.depth = 0

class AhoCorasick:
    def __init__(self):
        self.trie = [Node()]
        self.char_to_idx = {"A": 0, "C": 1, "G": 2, "T": 3, "N": 4}
        self.idx_to_char = ["A", "C", "G", "T", "N"]

    def add_fragment(self, s, offset):
        if DEBUG_MODE:
            print(f"добавляем фрагмент {s} со смещением {offset}")
        v = 0
        for char in s:
            idx = self.char_to_idx[char]
            if self.trie[v].son[idx] == -1:
                self.trie[v].son[idx] = len(self.trie)
                new_node = Node()
                new_node.depth = self.trie[v].depth + 1
                self.trie.append(new_node)
                if DEBUG_MODE:
                    print(f"  символ {char}: новая вершина {len(self.trie) - 1}, глубина {new_node.depth}")
            else:
                if DEBUG_MODE:
                    print(f"  символ {char}: переход в вершину {self.trie[v].son[idx]}")
            v = self.trie[v].son[idx]
        self.trie[v].offsets.append(offset)
        if DEBUG_MODE:
            print(f"  фрагмент завершён в вершине {v}")

    def build_automaton(self):
        q = []
        self.trie[0].fail = 0
        for c in range(5):
            if self.trie[0].son[c] != -1:
                v = self.trie[0].son[c]
                self.trie[v].fail = 0
                q.append(v)
            else:
                self.trie[0].son[c] = 0

        if DEBUG_MODE:
            print("\nПОСТРОЕНИЕ АВТОМАТА")
        
        while q:
            v = q.pop(0)
            if DEBUG_MODE:
                print(f"вершина {v}, глубина {self.trie[v].depth}")
            
            if self.trie[self.trie[v].fail].offsets:
                self.trie[v].out = self.trie[v].fail
                if DEBUG_MODE:
                    print(f"  out = {self.trie[v].fail}")
            else:
                self.trie[v].out = self.trie[self.trie[v].fail].out
                if DEBUG_MODE:
                    print(f"  out = {self.trie[v].out}")

            for c in range(5):
                u = self.trie[v].son[c]
                if u != -1:
                    self.trie[u].fail = self.trie[self.trie[v].fail].son[c]
                    if DEBUG_MODE:
                        print(f"  {self.idx_to_char[c]} -> {u}, fail = {self.trie[u].fail}")
                    q.append(u)
                else:
                    self.trie[v].son[c] = self.trie[self.trie[v].fail].son[c]

    def print_automaton(self):
        if not DEBUG_MODE:
            return
        print("\nОПИСАНИЕ КАЖДОЙ ВЕРШИНЫ АВТОМАТА")
        for i in range(len(self.trie)):
            edges = []
            for c in range(5):
                to = self.trie[i].son[c]
                if to != -1:
                    edges.append(f"{self.idx_to_char[c]}->{to}")
            edges_text = " ".join(edges) if edges else "-"
            offsets_info = f", offsets={self.trie[i].offsets}" if self.trie[i].offsets else ""
            print(f"вершина {i}: переходы=[{edges_text}], fail={self.trie[i].fail}, out={self.trie[i].out}, depth={self.trie[i].depth}{offsets_info}")

    def process_text(self, text, pattern_len):
        C = [0] * (len(text) + 2)
        current = 0

        if DEBUG_MODE:
            print("\nПРОЦЕСС ИСПОЛЬЗОВАНИЯ АВТОМАТА")
            print(f"текст: {text}")
        
        for i in range(len(text)):
            char_idx = self.char_to_idx[text[i]]
            prev = current
            current = self.trie[current].son[char_idx]
            
            if DEBUG_MODE:
                print(f"позиция {i + 1} ({text[i]}): {prev} -> {current}")

            temp = current
            while temp != 0:
                if self.trie[temp].offsets:
                    for offset in self.trie[temp].offsets:
                        start = i - self.trie[temp].depth - offset + 2
                        if 1 <= start <= len(text) - pattern_len + 1:
                            if DEBUG_MODE:
                                print(f"  фрагмент со смещением {offset}, start = {start}")
                            C[start] += 1
                temp = self.trie[temp].out
                if temp == -1:
                    break

        return C

def split_pattern(pattern, wildcard):
    fragments = []
    current = ""
    for i, char in enumerate(pattern):
        if char == wildcard:
            if current:
                offset = i - len(current)
                fragments.append((current, offset))
                current = ""
        else:
            current += char
    if current:
        offset = len(pattern) - len(current)
        fragments.append((current, offset))
    return fragments

def verify_jokers(text, pattern, wildcard, forbidden, start_pos):
    text_start = start_pos - 1
    for i, char in enumerate(pattern):
        if char == wildcard:
            if text[text_start + i] == forbidden:
                return False
    return True

def main():
    data = sys.stdin.read().split()
    T = data[0]
    P = data[1]
    wildcard = data[2]
    forbidden = data[3] if len(data) > 3 else None

    if DEBUG_MODE:
        print("=== ВХОДНЫЕ ДАННЫЕ ===")
        print(f"текст: {T}")
        print(f"образец: {P}")
        print(f"джокер: {wildcard}")
        print(f"запрещённый: {forbidden}")

    fragments = split_pattern(P, wildcard)
    
    if DEBUG_MODE:
        print("\nРАЗБИЕНИЕ ОБРАЗЦА")
        for frag, offset in fragments:
            print(f"  фрагмент {frag}, смещение {offset}")
        print(f"всего фрагментов: {len(fragments)}")

    if not fragments:
        for i in range(1, len(T) - len(P) + 2):
            if forbidden is None or verify_jokers(T, P, wildcard, forbidden, i):
                print(i)
        return

    if DEBUG_MODE:
        print("\n=== ПОСТРОЕНИЕ БОРА ===")
    
    aho = AhoCorasick()
    for frag, offset in fragments:
        aho.add_fragment(frag, offset)
    
    if DEBUG_MODE:
        print(f"\nвершин в боре: {len(aho.trie)}")

    aho.build_automaton()
    aho.print_automaton()
    
    C = aho.process_text(T, len(P))

    for i in range(1, len(T) - len(P) + 2):
        if C[i] == len(fragments):
            if forbidden is None or verify_jokers(T, P, wildcard, forbidden, i):
                print(i)

if __name__ == "__main__":
    main()