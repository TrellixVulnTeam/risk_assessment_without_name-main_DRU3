"""BRC OCR Module"""
from __future__ import annotations

import re
import pdfplumber as plumber
import streamlit as st
from contextlib import suppress
from typing import Dict, Iterable, List

from pdfplumber import PDF

AUDIT_RESULT_HEADERS = ("audit grade", "audit type", "audit result")
PDFPLUMBER_EXTRACTOR_HEADERS = (
    "critical",
    "fundamental",
    "minor",
    "major",
    "audit start date",
    "audit finish date",
    "re-audit date due date",
    "certificate expiry date",
    "certificate expiry",
    "certificate issue date",
    "site code",
    "previous audit date",
    "site name",
)


def regex_checker(text: str,
                  headers: Iterable[str],
                  results: Dict[str, str]) -> None:
    """Checking regex stuff

    Arguments:
    -----------
    text: :class:`str`
        The input text that extract from the pdf file
    headers: :class:`List[str]`
        A list of key values that want to extract info from the pdf
    results: :class:`Dict[str, str]`
        The dictionary contains the result
    """
    regex_delimiter = re.compile("|".join(headers), re.IGNORECASE)

    splitters = tuple(t.strip() for t in regex_delimiter.split(text)[1:])
    delimiters = regex_delimiter.findall(text)
    if not splitters or not delimiters:
        return

    for splitter, delimiter in zip(splitters, delimiters):
        if splitter.strip() != "":
            results[delimiter] = splitter


def get_company_name(file: PDF,
                     results: Dict[str, str]) -> None:
    """Get the company information

    Arguments:
    -----------
    pdf_file: :class:`bytes`
    results: :class:`Dict[str, str]`
    """
    first_page = file.pages[0]
    words: List[Dict[str, str | float]] = first_page.extract_words()

    words_unique = [dict(t) for t in {tuple(word.items()) for word in words}]
    words_unique_sorted = sorted(
        words_unique, key=lambda d: (d["top"], d['x0']))

    result_texts = [str(i["text"]) for i in words_unique_sorted]
    index_start = result_texts.index("Summary")
    index_end = result_texts.index("name")

    results["company name"] = " ".join(result_texts[index_start + 1: index_end])


def extract_date(file: PDF,
                 results: Dict[str, str]) -> None:
    """Extract the start date audit from the BRC

    Arguments:
    -----------
    pdf_file: :class:`bytes`
    results: :class:`dict`
    """
    for page_number in range(2, 5):
        page = file.pages[page_number]
        sentences: List[str] = page.extract_text(y_tolerance=5).split(
            "\n")  # extract text and split by line
        sentences = [text_stripped for text in sentences if (
            text_stripped := text.strip())]  # strip the word
        with suppress(StopIteration):
            index = next(i for i, s in enumerate(
                sentences) if "Audit Day" in s)
            # date returned will be a datetime.datetime object. here we are only using the first match.
            results["audit start date"] = sentences[index + 1]
            return


def check_major(text: str,
                results: Dict[str, str]) -> None:
    """Checking the major non conformities value

    Arguments:
    -----------
    text: :class:`str`
    results: :class:`Dict[str, str]`
    """
    splitter = text.split("major")
    try:
        text = next(s for s in splitter if s).strip()
        if text.isdigit():
            results["major"] = text
    except StopIteration:
        results["major"] = "0"
        results["minor"] = "0"
        results["critical"] = "0"
        results["fundamental"] = "0"

def get_auditor_info(sentences: List[str],
                     text: str, results: Dict[str, str]) -> None:
    results["auditor company"] = sentences[sentences.index(text) - 1]
    results["auditor name"] = text.lower().split("auditor: ")[-1]


def check_audit_result(text: str,
                       results: Dict[str, str]):
    if "audit grade" in text:
        regex_checker(text, AUDIT_RESULT_HEADERS, results)


def get_address(file: PDF,
                results: Dict[str, str]):
    for page_number in range(1, 5):
        page = file.pages[page_number]
        words = page.extract_words()

        words_unique = [dict(t) for t in {tuple(d.items()) for d in words}]
        words_unique_sorted = sorted(
            words_unique, key=lambda d: (d["top"], d['x0']))

        with suppress(ValueError):
            result_texts = [str(i["text"]) for i in words_unique_sorted]
            index_start = result_texts.index("Address")
            index_end = result_texts.index("Country")
            results["address"] = " ".join(result_texts[index_start + 1: index_end])
            return

def plumber_extractor(file: PDF, results: Dict[str, str]):
    """Main Function for extracting key information from PDF

    Arguments:
    -----------
    file: :class:`PDF`
    results: :class:`Dict[str, Tuple[str, int]]`
    """
    for page_number in range(2):
        page = file.pages[page_number]
        sentences = page.extract_text(y_tolerance=5).split("\n")  # extract text and split by line
        sentences = [t for text in sentences if (t := text.strip())]  # strip the word

        for text in sentences:
            text_lowered = text.lower()
            if "auditor:" in text_lowered:
                get_auditor_info(sentences, text, results)
            elif "major" in text_lowered:
                check_major(text_lowered, results)
            elif "audit result" in text_lowered:
                check_audit_result(text_lowered, results)
            else:
                regex_checker(text, PDFPLUMBER_EXTRACTOR_HEADERS, results)

def brc_scan(file_contents: st.UploadedFile):
    results = {}
    with plumber.open(file_contents) as pdf_file:
        plumber_extractor(pdf_file, results)
        extract_date(pdf_file, results)
        get_company_name(pdf_file, results)
        get_address(pdf_file, results)

    results =  {k.lower(): v for k, v in results.items()}
    return results
