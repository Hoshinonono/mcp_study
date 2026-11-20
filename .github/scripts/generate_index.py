# docs フォルダ配下の Markdown・PDF・HTML の一覧 (index.md) を生成する python ファイルです
# フォルダ探索をすることで目次を自動生成します
#
# 使い方: python generate_index.py <docsフォルダ>
#         -> <docsフォルダ>/index.md を作成する
#
# GitHub Pages 用の index.md なので、Markdown へのリンクは公開後の .html に向けています
import re
import sys
from pathlib import Path
from urllib.parse import quote

INDEX_FILE = "index.md"
INDEX_TITLE = "Documentation Index"

# 一覧に載せるファイルの拡張子
MARKDOWN_EXTENSIONS = (".md", ".markdown")
PDF_EXTENSIONS = (".pdf",)
HTML_EXTENSIONS = (".html", ".htm")

# フォルダ名かファイル名が以下に一致するものは探索を禁止する (小文字にして比較する)
BAN_LIST = ("index.md", "readme.md")

# 以下の文字で始まるフォルダやファイルも探索しない
# GitHub Pages (Jekyll) が公開しないので、載せてもリンク切れになるため (例: _includes, .git)
UNPUBLISHED_PREFIXES = (".", "_", "#", "~")

# Markdown の見出しは h6 (######) までなので、それより深いフォルダも h6 で表示する
MAX_HEADING_LEVEL = 6


def is_listed(path):
    """一覧に載せてよい名前のフォルダ・ファイルかどうか"""
    return path.name.lower() not in BAN_LIST and not path.name.startswith(UNPUBLISHED_PREFIXES)


def escape_markdown(text):
    """ファイル名に含まれる記号が Markdown の書式として解釈されないようにする (例: _ -> \\_)"""
    return re.sub(r"([\\`*_\[\]<>{}|~$#])", r"\\\1", text)


def make_title(file):
    """ファイル名から一覧に表示するタイトルを作る (例: getting-started.md -> Getting Started)"""
    words = file.stem.replace("-", " ")
    # 英単語の先頭を大文字にする (str.title() は "MCP" を "Mcp" にしてしまうので使わない)
    return re.sub(r"[A-Za-z]+", lambda m: m.group()[0].upper() + m.group()[1:], words)


def make_link(file, docs_dir):
    """index.md から見たファイルへのリンク先を作る (日本語や空白などは URL エンコードする)"""
    if file.suffix.lower() in MARKDOWN_EXTENSIONS:
        file = file.with_suffix(".html")  # GitHub Pages では Markdown は .html として公開される
    return quote(file.relative_to(docs_dir).as_posix())


def generate_index(folder, docs_dir, depth=1):
    """folder 以下にあるファイルの一覧を Markdown で返す"""
    entries = sorted((e for e in folder.iterdir() if is_listed(e)), key=lambda e: e.name)

    file_list = ""
    for file in entries:
        suffix = file.suffix.lower()
        if file.is_file() and suffix in MARKDOWN_EXTENSIONS + PDF_EXTENSIONS + HTML_EXTENSIONS:
            title = escape_markdown(make_title(file))
            mark = " (PDF)" if suffix in PDF_EXTENSIONS else ""
            file_list += f"- [{title}]({make_link(file, docs_dir)}){mark}\n"

    content = ""
    # 一覧に載せるファイルが無いフォルダは、フォルダ名 (見出し) も出力しない
    if file_list:
        if folder != docs_dir:  # docs 直下のファイルはタイトルのすぐ下に並べるので見出しは付けない
            heading = "#" * min(depth, MAX_HEADING_LEVEL)
            folder_path = folder.relative_to(docs_dir).as_posix()
            content += f"{heading} {escape_markdown(folder_path)}\n\n"
        content += file_list + "\n"

    for sub_folder in entries:
        if sub_folder.is_dir():
            content += generate_index(sub_folder, docs_dir, depth + 1)

    return content


def main():
    # Windows のランナーでも日本語のファイル名をログに出せるよう、出力は UTF-8 に固定する
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    if len(sys.argv) != 2:
        sys.exit("使い方: python generate_index.py <docsフォルダ>")
    docs_dir = Path(sys.argv[1])
    if not docs_dir.is_dir():
        sys.exit(f"docs フォルダが見つかりません: {docs_dir}")

    content = f"# {INDEX_TITLE}\n\n" + generate_index(docs_dir, docs_dir)
    content = content.rstrip("\n") + "\n"

    index_file = docs_dir / INDEX_FILE
    with open(index_file, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    print(f"{index_file} を生成しました:\n")
    print(content)


if __name__ == "__main__":
    main()
