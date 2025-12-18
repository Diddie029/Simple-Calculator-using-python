
"""
Simple Calculator Application using Tkinter
A beginner-friendly GUI calculator with basic arithmetic operations.
"""

import tkinter as tk
from tkinter import font
from tkinter import messagebox

class Calculator:
    """A simple calculator class that manages the GUI and calculation logic."""
    
    def __init__(self, root):
        """
        Initialize the calculator window and UI components.
        
        Args:
            root: The main Tkinter window object
        """
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Store the current calculation expression
        self.expression = ""
        
        # Define color scheme for a modern look
        self.bg_color = "#2c3e50"           # Dark background
        self.display_color = "#ecf0f1"      # Light text for display
        self.button_color = "#34495e"       # Button background
        self.button_hover = "#1a252f"       # Darker hover color
        self.operator_color = "#e74c3c"     # Red for operators
        self.equals_color = "#27ae60"       # Green for equals button
        
        # Configure the root window
        self.root.config(bg=self.bg_color)
        
        # Create the display and buttons
        self.create_display()
        self.create_buttons()
    
    def create_display(self):
        """Create the display screen that shows input and results."""
        # Frame for the display
        display_frame = tk.Frame(self.root, bg=self.display_color, relief=tk.SUNKEN, bd=5)
        display_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)
        
        # Display label (shows current expression and results)
        self.display = tk.Label(
            display_frame,
            text="0",
            font=("Arial", 28, "bold"),
            bg=self.display_color,
            fg=self.bg_color,
            justify=tk.RIGHT,
            anchor="e",
            padx=10,
            pady=10
        )
        self.display.pack(fill=tk.BOTH, expand=True)
    
    def create_buttons(self):
        """Create all calculator buttons and arrange them in a grid layout."""
        # Frame for buttons
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Define button layout - each row contains different buttons
        buttons = [
            ["C", "←", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]
        
        # Create buttons in a grid layout
        for row_index, row in enumerate(buttons):
            for col_index, button_text in enumerate(row):
                self.create_button(button_frame, button_text, row_index, col_index)
    
    def create_button(self, parent, text, row, col):
        """
        Create a single button with appropriate styling and command.
        
        Args:
            parent: The parent frame to place the button in
            text: The text to display on the button
            row: The row position in the grid
            col: The column position in the grid
        """
        # Determine button properties based on its function
        if text == "C":
            bg = self.operator_color
            fg = "white"
            command = self.clear
        elif text == "←":
            bg = self.operator_color
            fg = "white"
            command = self.backspace
        elif text == "=":
            bg = self.equals_color
            fg = "white"
            command = self.calculate
        elif text in ["÷", "×", "−", "+", "%"]:
            bg = self.operator_color
            fg = "white"
            command = lambda: self.append_to_expression(text)
        else:
            bg = self.button_color
            fg = self.display_color
            command = lambda: self.append_to_expression(text)
        
        # Create the button
        button = tk.Button(
            parent,
            text=text,
            font=("Arial", 18, "bold"),
            bg=bg,
            fg=fg,
            activebackground=self.button_hover,
            activeforeground="white",
            bd=0,
            padx=20,
            pady=20,
            command=command
        )
        
        # Place button in grid
        # "=" button spans 2 columns for better layout
        if text == "=":
            button.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=5, pady=5)
        else:
            button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        
        # Configure grid weights for responsiveness
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
    
    def append_to_expression(self, value):
        """
        Append a value (number or operator) to the current expression.
        
        Args:
            value: The number or operator to append
        """
        self.expression += str(value)
        self.update_display()
    
    def update_display(self):
        """Update the display screen with the current expression."""
        # If expression is empty, show 0
        if self.expression == "":
            self.display.config(text="0")
        else:
            self.display.config(text=self.expression)
    
    def clear(self):
        """Clear the entire expression and reset the calculator."""
        self.expression = ""
        self.update_display()
    
    def backspace(self):
        """Remove the last character from the expression."""
        self.expression = self.expression[:-1]
        self.update_display()
    
    def calculate(self):
        """
        Evaluate the mathematical expression and display the result.
        Handles errors gracefully.
        """
        try:
            # Replace display symbols with Python operators
            calculation = self.expression.replace("÷", "/").replace("×", "*").replace("−", "-")
            
            # Evaluate the expression
            result = eval(calculation)
            
            # Handle division by zero (eval may not catch this)
            if isinstance(result, float) and result == float('inf'):
                messagebox.showerror("Error", "Division by zero is not allowed!")
                self.expression = ""
            else:
                # Display result with appropriate decimal places
                if isinstance(result, float):
                    # Remove trailing zeros and unnecessary decimal points
                    result = round(result, 10)
                    if result == int(result):
                        self.expression = str(int(result))
                    else:
                        self.expression = str(result)
                else:
                    self.expression = str(result)
            
            self.update_display()
        
        except ZeroDivisionError:
            # Handle division by zero explicitly
            messagebox.showerror("Error", "Cannot divide by zero!")
            self.expression = ""
            self.update_display()
        
        except SyntaxError:
            # Handle invalid expressions (e.g., incomplete operations like "5+")
            messagebox.showerror("Error", "Invalid expression! Please check your input.")
            self.expression = ""
            self.update_display()
        
        except Exception as e:
            # Handle any other unexpected errors
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.expression = ""
            self.update_display()


def main():
    """Create the main window and start the calculator application."""
    # Create the root window
    root = tk.Tk()
    
    # Initialize the calculator
    calculator = Calculator(root)
    
    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
