# pages/page1_plot.py
'''
Matplotlib-based velocity-time preview plot for page 1.
This module defines the Page1Plot class:
    - encapsulates the creation and management of a Matplotlib plot embedded in a Tkinter frame. 
    - the plot dynamically updates based on user inputs from page 1, providing an interactive preview of the velocity profile.
'''
import tkinter as tk
from tkinter import ttk
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Font for CJK and Latin character support
FONTNAME = "Microsoft YaHei"
matplotlib.rcParams['axes.unicode_minus'] = False


class Page1Plot:
    """Modern canvas-based velocity-time preview for the right pane."""
    # ===========================================================================
    # INITIALIZATION
    # ===========================================================================
    # _build_plot() -> _init_plt() -> _init_axes() ->
    def __init__(self, parent_frame: ttk.Frame, app):
        """
        Args:
            parent_frame: The right-pane frame to host the preview card.
            app: The main MyApp instance for accessing shared state (language, plot_texts).
        """
        self.canvas = None
        self.toolbar = None
        self.fig = None
        self.ax = None
        self._plot_container_frame = None
        self.parent_frame = parent_frame # parent_frame is the right_pane frame passed in from Page1
        self.app = app
       
        self._build_plot()

    # ===========================================================================
    # UI / Widget Creation
    # ===========================================================================
    # right_pane (self.parent_frame)
    #     └── plot_container (pack, expand)
    #             └── FigureCanvasTkAgg canvas (grid)
    def _build_plot(self) -> None:
        """Build the plot preview widget: container, header label, matplotlib canvas, and resize handler."""
    
        # container frame for the plot and toolbar
        plot_container = ttk.Frame(self.parent_frame, padding=0)
        plot_container.pack(fill="both", expand=True)

        # Initialize Matplotlib figure and embed it into the plot_container frame
        self._create_plot_canvas(plot_container) 
        plot_container.bind("<Configure>", self._on_plot_resize)
        
        # Display default empty plot with message (since there is no data yet)
        self.update_plot(None) 

    def _create_plot_canvas(self, parent: ttk.Frame) -> None:
        """Initialize the Matplotlib figure and embed it into the given parent frame.
        Args:
            parent: The frame to embed the Matplotlib canvas into (plot_container in this case).
        """
       
        # style
        try:
            plt.style.use("seaborn-v0_8")
        except OSError:
            plt.style.use("ggplot")
    
        self.fig, self.ax = plt.subplots( #----------------------------------------------<- change preview figzie here
            figsize=(3.5, 2), # default size in inches (width, height) try (3.5, 2)
            dpi=100,          
            )

        # match background color to current theme for seamless integration 
        style = ttk.Style(parent)
        theme_bg = style.lookup("TFrame", "background") or style.lookup(".", "background") or "SystemButtonFace"
        try:
            r, g, b = parent.winfo_rgb(theme_bg)
            theme_bg = f"#{r // 256:02x}{g // 256:02x}{b // 256:02x}"
        except tk.TclError:
            theme_bg = "#f0f0f0"
        self.fig.patch.set_facecolor(theme_bg)

        # Configure axes with initial settings (labels, grid, etc.)
        self._init_axes()

        # Embed the Matplotlib figure into the Tkinter frame using FigureCanvasTkAgg
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)   # Put Matplotlib plot inside Tkinter frame(plot_container)
        

        # Use grid to allocate separate rows for canvas and toolbar
        parent.grid_rowconfigure(0, weight=1)  # canvas gets most space
        parent.grid_rowconfigure(1, weight=0)  # toolbar gets minimal space
        parent.grid_columnconfigure(0, weight=1) # single column that expands with the frame

        # Place canvas in row 0 and toolbar in row 1 of the parent frame
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Add Matplotlib's built-in navigation toolbar for interactivity (zoom, pan, save, etc.)
        self.toolbar = NavigationToolbar2Tk(self.canvas, parent, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(row=1, column=0, sticky="e", padx=0, pady=0)
        
        # Schedule initial resize for after the window is fully displayed.
        # During __init__, the container doesn't have its final dimensions yet.
        parent.after(150, self._canvas_resize) # DO NOT DELETE - this ensures the plot is properly sized after the window is rendered, preventing initial tiny plot issue on some platforms.

    #==============================================================================
    # RESIZE HANDLER
    #==============================================================================
    def _canvas_resize(self) -> None:
        """One-time resize after the window is fully rendered."""
        if not self.fig or not self.canvas:
            return
        canvas_widget = self.canvas.get_tk_widget()
        width = canvas_widget.winfo_width()
        height = canvas_widget.winfo_height() 
        if width > 100 and height > 100:
            self.fig.set_size_inches(width / self.fig.dpi, height / self.fig.dpi, forward=False)
            self.canvas.draw_idle()

    def _get_plot_text(self, key: str) -> str:
        """Get language-aware text for the plot from plot_texts config."""
        lang = self.app.current_language.get()
        text_dict = self.app.plot_texts.get("page1", {}).get("plot1", {}).get(key, {})
        return text_dict.get(lang) or text_dict.get("EN", "")

    def _init_axes(self) -> None:
        """Configure the axes layout, labels, and grid (called once during initialization)."""
        self.ax.set_title(self._get_plot_text("title"), fontname=FONTNAME)
        self.ax.set_xlabel(self._get_plot_text("x_label"), fontname=FONTNAME)
        self.ax.set_ylabel(self._get_plot_text("y_label"), fontname=FONTNAME)
        self.ax.grid(True, alpha=0.35)

    def _refresh_axes_labels(self) -> None:
        """Update axes title and labels to match current language."""
        self.ax.set_title(self._get_plot_text("title"), fontname=FONTNAME)
        self.ax.set_xlabel(self._get_plot_text("x_label"), fontname=FONTNAME)
        self.ax.set_ylabel(self._get_plot_text("y_label"), fontname=FONTNAME)

    def _on_plot_resize(self, event: tk.Event) -> None:
        """Handle plot resize events by scaling figure to container."""
        if not self.fig or not self.canvas or event.width < 10 or event.height < 10: # minimal size to avoid errors
            return
        width_in  = max(1, event.width) / self.fig.dpi 
        height_in = max(1, event.height) / self.fig.dpi

        #print(f"After stretch - figsize: ({width_in:.2f}, {height_in:.2f}) inches")  # Add this line

        self.fig.set_size_inches(width_in, height_in, forward=False) # forward=False to prevent automatic resizing by Matplotlib
        self.canvas.draw_idle()

    # ===========================================================================
    # PLOT UPDATE
    # ===========================================================================
    def update_plot(self, plot_data: Optional[dict]):
        """Update(draw) the plot with new data.
        Args:            
            plot_data: Dictionary containing 'time' and 'speed' lists for plotting."""
        
        if not self.canvas or not self.ax:
            return

        # Remove old plot lines and text (keep title/labels/grid)
        for line in self.ax.lines:
            line.remove()
        for text in self.ax.texts:
            text.remove()

        self._refresh_axes_labels()

        if not plot_data: 
            self._show_message(self._get_plot_text("no_input_error_message"))
            return

        result = self._parse_plot_data(plot_data)
        if result is None:
            self._show_message(self._get_plot_text("invalid_input_error_message"))
            return
        
        stage_times, speed_points = result
        self._plot_data(stage_times, speed_points)

    def _parse_plot_data(self, plot_data: dict) -> Optional[tuple]:
        """Parse and validate plot data.
        Args:
            plot_data: Dictionary with 'time' and 'speed' keys.
        Returns:
            (stage_times, speed_points) tuple if valid, None if invalid.
        """
        times = plot_data.get("time", [])
        speeds = plot_data.get("speed", [])
        
        try:
            stage_times = [float(v) for v in times[1:]]  # times=["0", "1.5", "3.0"] -> stage_times=[1.5, 3.0]
            speed_points = [float(v) for v in speeds]

             # Return None if parsing was successful but data is empty
            return stage_times, speed_points

        except (TypeError, ValueError):
            return None

    def _plot_data(self, stage_times: list, speed_points: list) -> None:
        """Plot the velocity profile curve.
        Args:
            stage_times: Time intervals for each stage.
            speed_points: Speed values for each stage.
        """
        cumulative_t = [0.0]
        for dt in stage_times:
            cumulative_t.append(cumulative_t[-1] + max(0.0, dt))

        # Reset axes to auto-scale (clears any previous zoom/pan)
        self.ax.autoscale(enable=True, axis='both')

        self.ax.plot(cumulative_t, speed_points, marker="o", linewidth=2, color="C0")
        self.ax.relim() # recalculate limits based on new data
        self.ax.autoscale_view() # rescale axes to fit new data

        # Resize figure to match actual canvas widget, THEN tight_layout for correct margins
        # canvas_widget = self.canvas.get_tk_widget()
        # w = canvas_widget.winfo_width()
        # h = canvas_widget.winfo_height()
        # if w > 100 and h > 100:
        #     self.fig.set_size_inches(w / self.fig.dpi, h / self.fig.dpi, forward=False)
        self._canvas_resize()

        self.fig.tight_layout() # adjust layout to prevent clipping (now with correct dimensions)
        self.canvas.draw_idle() # redraw canvas with updated plot

    def _show_message(self, message: str):
        self.ax.text(
            0.5,
            0.5,
            message,
            ha="center",
            va="center",
            transform=self.ax.transAxes,
            fontname=FONTNAME,
        )
        self.canvas.draw_idle()

    #===============================================================================
    # CLEANUP
    #===============================================================================
    def destroy(self):
        if self.toolbar:
            if self.toolbar.winfo_exists():
                self.toolbar.destroy()
            self.toolbar = None

        if self.canvas:
            widget = self.canvas.get_tk_widget()
            if widget and widget.winfo_exists():
                widget.destroy()    
            self.canvas = None

        if self.fig:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
