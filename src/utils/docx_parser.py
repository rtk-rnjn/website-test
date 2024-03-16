from __future__ import annotations

import re
import zipfile
from xml.etree import ElementTree as ET


class DocxParser:
    def __init__(self, file_path: str, image_directory: str = None):
        self.__docs = file_path
        self.__image_directory = image_directory
        self.__cached_text = {}

    @property
    def file_path(self) -> str:
        return self.__docs

    @file_path.setter
    def file_path(self, file_path: str):
        if self.__docs != file_path:
            path = self.__docs
            self.__docs = file_path

            if path in self.__cached_text:
                del self.__cached_text[path]

            self.__cached_text[file_path] = self.process(file_path)

    namespaces = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
        "v": "urn:schemas-microsoft-com:vml",
        "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
        "w10": "urn:schemas-microsoft-com:office:word",
        "wne": "http://schemas.microsoft.com/office/word/2006/wordml",
        "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsd": "http://www.w3.org/2001/XMLSchema",
        "wpc": "http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas",
        "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
        "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
        "w16se": "http://schemas.microsoft.com/office/word/2015/wordml/symex",
        "w16cid": "http://schemas.microsoft.com/office/word/2016/wordml/cid",
        "w16": "http://schemas.microsoft.com/office/word/2018/wordml",
        "w16cex": "http://schemas.microsoft.com/office/word/2018/wordml/cex",
        "w16sdtdh": "http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash",
        "w16sdtdt": "http://schemas.microsoft.com/office/word/2020/wordml/sdtdata",
        "w16sdtd": "http://schemas.microsoft.com/office/word/2020/wordml/sdtdata",
    }

    def qualified_name(self, name: str) -> str:
        prefix, local_name = name.split(":")
        return f"{{{self.namespaces[prefix]}}}{local_name}"

    def xml2text(self, xml: str) -> str:
        text = ""
        root = ET.fromstring(xml)

        for child in root.iter():
            if child.tag == self.qualified_name("w:t"):
                t_text = child.text
                text += t_text if t_text is not None else ""
            elif child.tag == self.qualified_name("w:tab"):
                text += "\t"
            elif child.tag in (
                self.qualified_name("w:br"),
                self.qualified_name("w:cr"),
            ):
                text += "\n"
            elif child.tag == self.qualified_name("w:p"):
                text += "\n\n"
        return text

    _image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"]

    def process(self, docx: str | None = None, image_directory: str = None) -> str:
        text = ""

        with zipfile.ZipFile(self.__docs or docx, "r") as zipf:
            filelist = zipf.namelist()

            header_xml = "word/header[0-9]*.xml"
            for fname in filelist:
                if re.match(header_xml, fname):
                    with zipf.open(fname) as f:
                        text += self.xml2text(f.read().decode("utf-8"))

            doc_xml = "word/document.xml"
            with zipf.open(doc_xml) as f:
                text += self.xml2text(f.read().decode("utf-8"))

            footer_xml = "word/footer[0-9]*.xml"
            for fname in filelist:
                if re.match(footer_xml, fname):
                    with zipf.open(fname) as f:
                        text += self.xml2text(f.read().decode("utf-8"))

            image_directory = image_directory or self.__image_directory

            if image_directory:
                for fname in filelist:
                    if fname.startswith("word/media/") and any(
                        fname.lower().endswith(ext) for ext in self._image_extensions
                    ):
                        with zipf.open(fname) as f:
                            with open(
                                f"{image_directory}/{fname.split('/')[-1]}",
                                "wb",
                            ) as img_file:
                                img_file.write(f.read())

        return text.strip()


def parse_questions(text: str):
    questions = []
    question_regex_sep = r"Question\s*\d+:"
    correct_option_regex = r"Answer:\s*\(?([A-D])\)?"

    _questions: list[str] = re.split(question_regex_sep, text)

    for ques in _questions[1:]:
        if not ques.strip():
            continue

        splits = ques.split("\n")

        for split in splits:
            if not split.strip():
                splits.remove(split)

        question = splits[0].strip()
        option_a = splits[1].strip()[3:].strip()
        option_b = splits[2].strip()[3:].strip()
        option_c = splits[3].strip()[3:].strip()
        option_d = splits[4].strip()[3:].strip()

        correct_option = re.search(correct_option_regex, splits[5]).group(1)

        explanation = "\n".join(splits[6:]).strip()
        if explanation.startswith("Explanation:"):
            explanation = explanation[13:].strip()

        questions.append(
            {
                "question": question,
                "A": option_a,
                "B": option_b,
                "C": option_c,
                "D": option_d,
                "correct_option": correct_option,
                "explanation": explanation,
            },
        )

    return questions
