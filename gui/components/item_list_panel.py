from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PyQt6.QtCore import pyqtSignal
from gui.widgets.named_list_section import NamedListSection


class ItemListPanel(QWidget):
    """
    Self-contained panel that manages the alternatives list.
    Consumers only see: .items, and the item_added / item_removed signals.
    """
    item_added = pyqtSignal(str)
    item_removed = pyqtSignal(str)

    _EMPTY_TEXT = "No alternatives added yet"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items: list[str] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._section = NamedListSection(
            section_title="Alternatives:",
            placeholder="Enter alternative name",
            add_button_text="Add Alternative",
            empty_summary_text=self._EMPTY_TEXT,
        )
        self._section.input.returnPressed.connect(self._handle_add)
        self._section.add_button.clicked.connect(self._handle_add)
        layout.addWidget(self._section)

    # ── Public API ──────────────────────────────────────────────────────────

    @property
    def items(self) -> list[str]:
        return list(self._items)

    def clear(self) -> None:
        self._items.clear()
        self._refresh_summary()

    # ── Private ─────────────────────────────────────────────────────────────

    def _handle_add(self) -> None:
        name = self._section.input.text().strip()
        if not name:
            return
        if name in self._items:
            QMessageBox.warning(self, "Duplicate", "This alternative already exists!")
            return
        self._items.append(name)
        self._section.input.clear()
        self._refresh_summary()
        self.item_added.emit(name)

    def _refresh_summary(self) -> None:
        text = f"Alternatives: {', '.join(self._items)}" if self._items else self