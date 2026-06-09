"""
news_summarizer.py
------------------
A GUI application that fetches news articles, generates AI summaries,
and categorizes topics using the call_gpt API.

Author  : News Summarizer App
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import json
import datetime

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
APP_TITLE        = "AI News Summarizer"
WINDOW_WIDTH     = 900
WINDOW_HEIGHT    = 680
FONT_HEADING     = ("Segoe UI", 13, "bold")
FONT_BODY        = ("Segoe UI", 10)
FONT_MONO        = ("Consolas", 10)
FONT_SMALL       = ("Segoe UI", 9)

COLOR_BG         = "#0f1117"
COLOR_SURFACE    = "#1a1d27"
COLOR_PANEL      = "#22263a"
COLOR_ACCENT     = "#4f8ef7"
COLOR_ACCENT2    = "#a78bfa"
COLOR_SUCCESS    = "#34d399"
COLOR_WARNING    = "#fbbf24"
COLOR_TEXT       = "#e2e8f0"
COLOR_MUTED      = "#64748b"
COLOR_BORDER     = "#2e3248"
COLOR_INPUT_BG   = "#13162b"

CATEGORIES = [
    "Technology", "Science", "Politics", "Business",
    "Health", "Sports", "Entertainment", "World",
    "Environment", "Education"
]

# AI prompt templates
SUMMARY_SYSTEM_PROMPT = (
    "You are an expert news analyst. When given a topic, you:\n"
    "1. Provide a concise, factual overview (2-3 sentences).\n"
    "2. List 4-5 key recent developments or talking points.\n"
    "3. Mention relevant context or background.\n"
    "Keep the tone neutral and informative."
)

CATEGORY_SYSTEM_PROMPT = (
    "You are a topic classifier. Given a news topic, respond ONLY with a JSON object:\n"
    '{"category": "<one of: Technology, Science, Politics, Business, '
    'Health, Sports, Entertainment, World, Environment, Education>", '
    '"confidence": "<High|Medium|Low>", "tags": ["tag1","tag2","tag3"]}\n'
    "No extra text—JSON only."
)


# ---------------------------------------------------------------------------
# AI interface (wraps the provided call_gpt import)
# ---------------------------------------------------------------------------

def get_news_summary(topic: str) -> str:
    """
    Calls the AI API to generate a news summary for the given topic.

    Args:
        topic: The news topic string entered by the user.

    Returns:
        A formatted summary string from the AI model.
    """
    try:
        from ai import call_gpt
        prompt = f"Summarize the latest news and developments about: {topic}"
        return call_gpt(prompt, system=SUMMARY_SYSTEM_PROMPT)
    except ImportError:
        return _mock_summary(topic)


def get_topic_category(topic: str) -> dict:
    """
    Calls the AI API to classify the topic and return category metadata.

    Args:
        topic: The news topic string.

    Returns:
        A dict with keys: category, confidence, tags.
    """
    try:
        from ai import call_gpt
        prompt = f"Classify this news topic: {topic}"
        raw = call_gpt(prompt, system=CATEGORY_SYSTEM_PROMPT)
        raw = raw.strip().strip("```json").strip("```").strip()
        return json.loads(raw)
    except ImportError:
        return _mock_category(topic)
    except (json.JSONDecodeError, ValueError):
        return {"category": "World", "confidence": "Low", "tags": [topic]}


# ---------------------------------------------------------------------------
# Mock helpers (used when `ai` module is not installed)
# ---------------------------------------------------------------------------

def _mock_summary(topic: str) -> str:
    """Returns a placeholder summary when the AI module is unavailable."""
    return (
        f"[DEMO MODE — install 'ai' package to enable live summaries]\n\n"
        f"Topic: {topic}\n\n"
        f"Overview\n"
        f"This is a demonstration summary for '{topic}'. In live mode, "
        f"the AI would provide a factual, up-to-date overview based on "
        f"recent developments.\n\n"
        f"Key Developments\n"
        f"• Development 1 related to {topic}\n"
        f"• Development 2 related to {topic}\n"
        f"• Development 3 related to {topic}\n"
        f"• Development 4 related to {topic}\n\n"
        f"Background\n"
        f"Additional context about {topic} would appear here in live mode."
    )


def _mock_category(topic: str) -> dict:
    """Returns a placeholder category when the AI module is unavailable."""
    return {
        "category": "Technology",
        "confidence": "Medium",
        "tags": [topic, "news", "demo"]
    }


# ---------------------------------------------------------------------------
# GUI Application
# ---------------------------------------------------------------------------

class NewsSummarizerApp:
    """
    Main application class.  Builds the Tkinter GUI and orchestrates
    calls to the AI backend on a background thread.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialises the application.

        Args:
            root: The root Tkinter window.
        """
        self.root = root
        self.history: list[dict] = []          # stores past searches
        self._configure_root()
        self._build_ui()

    # ------------------------------------------------------------------
    # Setup helpers
    # ------------------------------------------------------------------

    def _configure_root(self) -> None:
        """Configures root window geometry and style."""
        self.root.title(APP_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(True, True)
        self.root.configure(bg=COLOR_BG)
        self.root.minsize(720, 500)

    def _build_ui(self) -> None:
        """Constructs every widget in the window."""
        self._build_header()
        self._build_main_area()
        self._build_status_bar()

    def _build_header(self) -> None:
        """Creates the top header bar."""
        header = tk.Frame(self.root, bg=COLOR_SURFACE, height=64)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Logo area
        logo_frame = tk.Frame(header, bg=COLOR_SURFACE)
        logo_frame.pack(side="left", padx=20, pady=12)

        tk.Label(
            logo_frame, text="◈", font=("Segoe UI", 18),
            fg=COLOR_ACCENT, bg=COLOR_SURFACE
        ).pack(side="left", padx=(0, 8))

        tk.Label(
            logo_frame, text=APP_TITLE,
            font=("Segoe UI", 13, "bold"),
            fg=COLOR_TEXT, bg=COLOR_SURFACE
        ).pack(side="left")

        # Date badge
        today = datetime.date.today().strftime("%B %d, %Y")
        tk.Label(
            header, text=today, font=FONT_SMALL,
            fg=COLOR_MUTED, bg=COLOR_SURFACE
        ).pack(side="right", padx=20)

    def _build_main_area(self) -> None:
        """Builds the two-column main content area."""
        main = tk.Frame(self.root, bg=COLOR_BG)
        main.pack(fill="both", expand=True, padx=16, pady=12)

        # Left column: input + results
        left = tk.Frame(main, bg=COLOR_BG)
        left.pack(side="left", fill="both", expand=True)

        self._build_search_panel(left)
        self._build_result_panel(left)

        # Right column: sidebar
        right = tk.Frame(main, bg=COLOR_BG, width=220)
        right.pack(side="right", fill="y", padx=(12, 0))
        right.pack_propagate(False)

        self._build_sidebar(right)

    def _build_search_panel(self, parent: tk.Frame) -> None:
        """Creates the topic input and action buttons."""
        panel = tk.Frame(parent, bg=COLOR_SURFACE, padx=18, pady=16)
        panel.pack(fill="x", pady=(0, 10))

        tk.Label(
            panel, text="Enter a News Topic",
            font=FONT_HEADING, fg=COLOR_TEXT, bg=COLOR_SURFACE
        ).pack(anchor="w")

        tk.Label(
            panel,
            text="Type any topic — AI will fetch a summary and categorise it",
            font=FONT_SMALL, fg=COLOR_MUTED, bg=COLOR_SURFACE
        ).pack(anchor="w", pady=(2, 10))

        # Input row
        input_row = tk.Frame(panel, bg=COLOR_SURFACE)
        input_row.pack(fill="x")

        self.topic_var = tk.StringVar()
        self.topic_entry = tk.Entry(
            input_row, textvariable=self.topic_var,
            font=("Segoe UI", 11), bg=COLOR_INPUT_BG,
            fg=COLOR_TEXT, insertbackground=COLOR_ACCENT,
            relief="flat", bd=0, highlightthickness=2,
            highlightbackground=COLOR_BORDER,
            highlightcolor=COLOR_ACCENT
        )
        self.topic_entry.pack(side="left", fill="x", expand=True,
                              ipady=9, padx=(0, 10))
        self.topic_entry.bind("<Return>", lambda _e: self._start_search())

        self.search_btn = tk.Button(
            input_row, text="Summarise  →",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_ACCENT, fg="white",
            activebackground="#3b7de8", activeforeground="white",
            relief="flat", bd=0, padx=18, pady=9,
            cursor="hand2", command=self._start_search
        )
        self.search_btn.pack(side="left")

        # Quick-topic chips
        chip_row = tk.Frame(panel, bg=COLOR_SURFACE)
        chip_row.pack(fill="x", pady=(10, 0))

        tk.Label(
            chip_row, text="Quick:", font=FONT_SMALL,
            fg=COLOR_MUTED, bg=COLOR_SURFACE
        ).pack(side="left", padx=(0, 6))

        quick_topics = ["AI", "Climate", "Space", "Economy", "Healthcare"]
        for qt in quick_topics:
            btn = tk.Button(
                chip_row, text=qt, font=FONT_SMALL,
                bg=COLOR_PANEL, fg=COLOR_ACCENT,
                activebackground=COLOR_ACCENT, activeforeground="white",
                relief="flat", bd=0, padx=10, pady=4, cursor="hand2",
                command=lambda t=qt: self._quick_search(t)
            )
            btn.pack(side="left", padx=3)

    def _build_result_panel(self, parent: tk.Frame) -> None:
        """Creates the scrollable result display area."""
        panel = tk.Frame(parent, bg=COLOR_SURFACE, padx=18, pady=16)
        panel.pack(fill="both", expand=True)

        # Category badge row (hidden until search runs)
        self.badge_frame = tk.Frame(panel, bg=COLOR_SURFACE)
        self.badge_frame.pack(fill="x", pady=(0, 10))

        self.category_badge = tk.Label(
            self.badge_frame, text="",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_ACCENT2, fg="white",
            padx=10, pady=3, relief="flat"
        )
        self.confidence_badge = tk.Label(
            self.badge_frame, text="",
            font=FONT_SMALL, bg=COLOR_PANEL,
            fg=COLOR_MUTED, padx=8, pady=3
        )
        self.tags_label = tk.Label(
            self.badge_frame, text="",
            font=FONT_SMALL, fg=COLOR_MUTED, bg=COLOR_SURFACE
        )

        # Result text area
        self.result_text = scrolledtext.ScrolledText(
            panel, font=FONT_BODY,
            bg=COLOR_INPUT_BG, fg=COLOR_TEXT,
            insertbackground=COLOR_ACCENT,
            relief="flat", bd=0, wrap="word",
            state="disabled", padx=12, pady=12
        )
        self.result_text.pack(fill="both", expand=True)
        self._set_result_placeholder()

    def _build_sidebar(self, parent: tk.Frame) -> None:
        """Creates the search history sidebar."""
        tk.Label(
            parent, text="Recent Searches",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_TEXT, bg=COLOR_BG
        ).pack(anchor="w", pady=(4, 8))

        frame = tk.Frame(parent, bg=COLOR_SURFACE)
        frame.pack(fill="both", expand=True)

        self.history_box = tk.Listbox(
            frame, font=FONT_SMALL,
            bg=COLOR_SURFACE, fg=COLOR_TEXT,
            selectbackground=COLOR_ACCENT,
            selectforeground="white",
            relief="flat", bd=0,
            activestyle="none",
            highlightthickness=0
        )
        self.history_box.pack(fill="both", expand=True, padx=2, pady=2)
        self.history_box.bind("<<ListboxSelect>>", self._on_history_select)

        # Clear button
        tk.Button(
            parent, text="Clear History",
            font=FONT_SMALL,
            bg=COLOR_PANEL, fg=COLOR_MUTED,
            activebackground=COLOR_BORDER, activeforeground=COLOR_TEXT,
            relief="flat", bd=0, padx=10, pady=6,
            cursor="hand2", command=self._clear_history
        ).pack(fill="x", pady=(8, 0))

    def _build_status_bar(self) -> None:
        """Creates the bottom status bar."""
        bar = tk.Frame(self.root, bg=COLOR_SURFACE, height=28)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        self.status_var = tk.StringVar(value="Ready — enter a topic above")
        tk.Label(
            bar, textvariable=self.status_var,
            font=FONT_SMALL, fg=COLOR_MUTED, bg=COLOR_SURFACE
        ).pack(side="left", padx=14, pady=5)

        self.progress = ttk.Progressbar(
            bar, mode="indeterminate", length=120
        )
        self.progress.pack(side="right", padx=14, pady=6)

    # ------------------------------------------------------------------
    # Search logic
    # ------------------------------------------------------------------

    def _start_search(self) -> None:
        """Validates input and launches the background search thread."""
        topic = self.topic_var.get().strip()
        if not topic:
            messagebox.showwarning("No Topic", "Please enter a topic to search.")
            return

        self._set_loading_state(True)
        thread = threading.Thread(
            target=self._run_search, args=(topic,), daemon=True
        )
        thread.start()

    def _quick_search(self, topic: str) -> None:
        """Fills the entry and starts a search for a quick-topic chip."""
        self.topic_var.set(topic)
        self._start_search()

    def _run_search(self, topic: str) -> None:
        """
        Background worker: fetches summary + category, then updates UI.

        Args:
            topic: The topic string to research.
        """
        try:
            summary  = get_news_summary(topic)
            category = get_topic_category(topic)
            self.root.after(0, self._display_results,
                            topic, summary, category)
        except Exception as exc:                         # broad catch on thread
            self.root.after(0, self._display_error, str(exc))

    # ------------------------------------------------------------------
    # UI update helpers (always called from main thread via after())
    # ------------------------------------------------------------------

    def _display_results(
        self, topic: str, summary: str, category: dict
    ) -> None:
        """
        Renders the AI results into the result panel.

        Args:
            topic   : Original search topic.
            summary : AI-generated summary text.
            category: Dict with keys category, confidence, tags.
        """
        # Badges
        cat  = category.get("category", "Unknown")
        conf = category.get("confidence", "")
        tags = ", ".join(category.get("tags", []))

        self.category_badge.config(text=f"  {cat}  ")
        self.confidence_badge.config(text=f"Confidence: {conf}")
        self.tags_label.config(text=f"Tags: {tags}")

        self.category_badge.pack(side="left")
        self.confidence_badge.pack(side="left", padx=6)
        self.tags_label.pack(side="left", padx=4)

        # Result text
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert(
            "end",
            f"NEWS SUMMARY: {topic.upper()}\n"
            f"{'─' * 50}\n\n"
            f"{summary}\n\n"
            f"{'─' * 50}\n"
            f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        )
        self.result_text.config(state="disabled")

        # History
        self._add_to_history(topic, cat)
        self._set_loading_state(False)
        self.status_var.set(
            f"Summary ready — category: {cat}  |  {datetime.datetime.now():%H:%M}"
        )

    def _display_error(self, message: str) -> None:
        """
        Shows an error message in the result area.

        Args:
            message: Human-readable error description.
        """
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", f"⚠  Error\n\n{message}")
        self.result_text.config(state="disabled")
        self._set_loading_state(False)
        self.status_var.set("Error — see result panel")

    def _set_result_placeholder(self) -> None:
        """Inserts placeholder text into the result area on startup."""
        self.result_text.config(state="normal")
        self.result_text.insert(
            "end",
            "Your news summary will appear here.\n\n"
            "Type a topic in the field above and press Summarise  →  "
            "or hit Enter.\n\n"
            "Examples: 'Artificial Intelligence', 'Mars exploration', "
            "'Global economy 2025'"
        )
        self.result_text.config(state="disabled")

    def _set_loading_state(self, loading: bool) -> None:
        """
        Toggles loading indicators and button states.

        Args:
            loading: True to show spinner; False to stop.
        """
        if loading:
            self.search_btn.config(text="Loading…", state="disabled")
            self.topic_entry.config(state="disabled")
            self.progress.start(12)
            self.status_var.set("Fetching summary from AI…")

            # Clear old badges
            for widget in self.badge_frame.winfo_children():
                widget.pack_forget()
        else:
            self.search_btn.config(text="Summarise  →", state="normal")
            self.topic_entry.config(state="normal")
            self.progress.stop()

    # ------------------------------------------------------------------
    # History helpers
    # ------------------------------------------------------------------

    def _add_to_history(self, topic: str, category: str) -> None:
        """
        Saves a search to the history list and sidebar widget.

        Args:
            topic   : Searched topic.
            category: Detected category for the topic.
        """
        entry = {"topic": topic, "category": category,
                 "time": datetime.datetime.now().strftime("%H:%M")}
        self.history.insert(0, entry)

        self.history_box.insert(0, f"{entry['time']}  {topic}")
        if self.history_box.size() > 20:
            self.history_box.delete("end")
            self.history.pop()

    def _on_history_select(self, _event: tk.Event) -> None:
        """Re-searches a topic when the user clicks a history item."""
        selection = self.history_box.curselection()
        if not selection:
            return
        index = selection[0]
        topic = self.history[index]["topic"]
        self.topic_var.set(topic)
        self._start_search()

    def _clear_history(self) -> None:
        """Clears all search history."""
        self.history.clear()
        self.history_box.delete(0, "end")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Creates the Tkinter root window and starts the event loop."""
    root = tk.Tk()
    _app = NewsSummarizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()