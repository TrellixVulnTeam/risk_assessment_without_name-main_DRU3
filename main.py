"""Main function"""
from __future__ import annotations

import streamlit as st

from main_utils import select_function


def main() -> None:
    """Main function to run the app"""
    st.title("Third Party Audit Analysis")
    function_name = select_function()

main()
