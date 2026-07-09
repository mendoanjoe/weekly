#!/usr/bin/env python3
from pathlib import Path
import re
import sys

INTRO_REPLACEMENTS = {
    "# 科技爱好者周刊": "# Mingguan Penggemar Teknologi",
    "记录每周值得分享的科技内容，周五发布。": "Mencatat konten teknologi yang layak dibagikan setiap minggu, terbit setiap Jumat.",
    "欢迎投稿文章/软件/资源，请[提交 issue](https://github.com/ruanyf/weekly/issues) 。": "Silakan kirim kontribusi artikel/perangkat lunak/sumber daya melalui [issue](https://github.com/ruanyf/weekly/issues).",
    "> P.S. 讨论区的[《谁在招人》](https://github.com/ruanyf/weekly/issues/10517)，是一个免费的程序员招聘帖，提供大量就业信息，欢迎发布工作/实习岗位。": "> P.S. Diskusi [\"Siapa yang sedang merekrut\"](https://github.com/ruanyf/weekly/issues/10517) adalah posting lowongan programmer gratis yang menyediakan banyak info pekerjaan. Silakan unggah lowongan kerja/magang.",
}

MONTH_MAP = {
    "一月": "Januari",
    "二月": "Februari",
    "三月": "Maret",
    "四月": "April",
    "五月": "Mei",
    "六月": "Juni",
    "七月": "Juli",
    "八月": "Agustus",
    "九月": "September",
    "十月": "Oktober",
    "十一月": "November",
    "十二月": "Desember",
}


def translate_line(line: str) -> str:
    stripped = line.rstrip("\n")

    if stripped in INTRO_REPLACEMENTS:
        return INTRO_REPLACEMENTS[stripped] + "\n"

    month_match = re.match(r"^\*\*(.+)\*\*$", stripped)
    if month_match:
        month = month_match.group(1)
        if month in MONTH_MAP:
            return f"**{MONTH_MAP[month]}**\n"

    issue_match = re.match(r"^(\s*-\s*)第\s*(\d+)\s*期：", stripped)
    if issue_match:
        prefix, num = issue_match.group(1), issue_match.group(2)
        return re.sub(r"^(\s*-\s*)第\s*\d+\s*期：", f"{prefix}Edisi {num}: ", stripped, count=1) + "\n"

    return line


def translate_file(input_path: Path, output_path: Path) -> None:
    lines = input_path.read_text(encoding="utf-8").splitlines(keepends=True)
    translated = [translate_line(line) for line in lines]
    output_path.write_text("".join(translated), encoding="utf-8")


def should_translate(path: Path) -> bool:
    return path.suffix == ".md" and not path.name.endswith(".id.md")


def target_path_for(source_path: Path) -> Path:
    return source_path.with_suffix(".id.md")


def translate_repository(root: Path) -> None:
    for source in sorted(root.rglob("*.md")):
        if ".git" in source.parts or not should_translate(source):
            continue
        translate_file(source, target_path_for(source))


def main() -> int:
    args = sys.argv[1:]

    if len(args) == 0:
        translate_repository(Path("."))
        return 0

    if len(args) == 2:
        translate_file(Path(args[0]), Path(args[1]))
        return 0

    print("Usage: generate_readme_id.py [<input.md> <output.id.md>]", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
