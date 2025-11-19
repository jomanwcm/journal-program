import tkinter as tk

# Optional: tkcalendar for date picker (pip install tkcalendar)
try:
    from tkcalendar import DateEntry as _BaseDateEntry

    class DateEntry(_BaseDateEntry):
        """
        Small wrapper around tkcalendar.DateEntry to avoid the bug where
        the calendar popup closes when you click the month/year header
        after reopening the dropdown.
        """
        def __init__(self, master=None, **kw):
            super().__init__(master, **kw)
            # Remove the original FocusOut handler
            try:
                self._calendar.unbind('<FocusOut>')
            except Exception:
                pass
            # Bind our safer handler
            self._calendar.bind('<FocusOut>', self._safe_focus_out)

        def _safe_focus_out(self, event):
            """
            Only close the popup when the mouse is clearly outside the
            calendar Toplevel. Clicking inside (e.g. month/year header)
            should NOT close it.
            """
            try:
                # Current pointer position (global screen coords)
                x, y = self._top_cal.winfo_pointerxy()
                xc = self._top_cal.winfo_rootx()
                yc = self._top_cal.winfo_rooty()
                w = self._top_cal.winfo_width()
                h = self._top_cal.winfo_height()

                inside = (xc <= x <= xc + w) and (yc <= y <= yc + h)

                if not inside:
                    # Pointer is outside the calendar popup -> close it
                    self._top_cal.withdraw()
                    self.state(['!pressed'])
                # If inside, do nothing: keep the calendar open so the
                # month/year selector can work normally.
            except Exception:
                # If something goes wrong, fall back to closing.
                self._top_cal.withdraw()
                self.state(['!pressed'])

except ImportError:
    DateEntry = None  # fallback to simple Entry widget








root = tk.Tk()
root.title("DateEntry test")

var = tk.StringVar()
e = DateEntry(root, width=12, date_pattern="yyyy-mm-dd", textvariable=var)
e.pack(padx=20, pady=20)

root.mainloop()
