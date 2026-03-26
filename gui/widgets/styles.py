"""Shared Qt stylesheets for MCDA method screens."""

STYLE_BACK_BUTTON = """
    QPushButton {
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 8px;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: #e0e0e0;
    }
"""

STYLE_PRIMARY_ACTION_BUTTON = """
    QPushButton {
        background-color: #2196F3;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 15px;
    }
    QPushButton:hover {
        background-color: #0b7dda;
    }
"""

STYLE_CALCULATE_BUTTON = """
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
        margin-top: 20px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QPushButton:disabled {
        background-color: #cccccc;
        color: #666666;
    }
"""

STYLE_SECTION_LABEL = "font-weight: bold; font-size: 14px; margin-top: 10px;"

STYLE_SECTION_LABEL_MATRIX = "font-weight: bold; font-size: 14px; margin-top: 20px;"

STYLE_EMPTY_LIST_HINT = "color: #666; margin: 5px 0 15px 0;"

STYLE_RESULT_SECTION_LABEL = "font-weight: bold; font-size: 14px; margin-top: 20px;"
