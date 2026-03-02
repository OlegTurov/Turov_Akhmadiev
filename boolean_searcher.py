import json
import re


def load_index(index_file):
    with open(index_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {k: set(v) for k, v in data.items()}


def tokenize(query):
    tokens = re.findall(r'\(|\)|AND|OR|NOT|\w+', query.upper())
    return tokens


def to_postfix(tokens):
    precedence = {'NOT': 3, 'AND': 2, 'OR': 1}
    output = []
    stack = []

    for token in tokens:
        if token not in precedence and token not in ('(', ')'):
            output.append(token.lower())

        elif token in precedence:
            while (stack and stack[-1] != '(' and
                   precedence.get(stack[-1], 0) >= precedence[token]):
                output.append(stack.pop())
            stack.append(token)

        elif token == '(':
            stack.append(token)

        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()

    while stack:
        output.append(stack.pop())

    return output


def evaluate_postfix(postfix, index, all_docs):
    stack = []

    for token in postfix:
        if token == 'AND':
            right = stack.pop()
            left = stack.pop()
            stack.append(left & right)

        elif token == 'OR':
            right = stack.pop()
            left = stack.pop()
            stack.append(left | right)

        elif token == 'NOT':
            operand = stack.pop()
            stack.append(all_docs - operand)

        else:
            stack.append(index.get(token, set()))

    return stack.pop() if stack else set()


def boolean_search(query, index):
    tokens = tokenize(query)
    postfix = to_postfix(tokens)

    all_docs = set()
    for docs in index.values():
        all_docs.update(docs)

    return evaluate_postfix(postfix, index, all_docs)


if __name__ == "__main__":
    index = load_index("inverted_index.json")

    while True:
        query = input("Введите запрос (exit для выхода): ")
        if query.strip().lower() == "exit":
            break

        result = boolean_search(query, index)
        print("Найденные документы:", result)