#All original code and credit goes to HackerShackOfficial, as this code was heavily influenced by theirs.
#Code By TWrecks

# Some significant code improvements, updates and changes have been made to the menu.py file.
# These include:
#   - Syntax and compatability updates, updating the codebase from Python 2 to Python 3.
#       - This includes changes such as using the 'super()' function for calling the base class
#         constructor in derived classes, such as the 'Back' and 'Menu' classes.
#   - Some parts of the code have been simplified, such as using the '+=' operate to concatenate lists
#     in the 'addOptions' method.
#   - The code has been reformatted to the best of my ability to follow PEP8 Guidelines and keep it
#     consistent. This includes spacing and indentation. This should keep maintenance easy!
#   - Heavily commented code. Comments have been left throughout the code to explain the functionality
#     of each class and method. Hopefully this helps out those of you who are unfamiliar with Python,
#     and allows you to make changes and modifications easily.

# The MenuItem class represents a basic menu item.
class MenuItem:
    def __init__(self, type, name, attributes=None, visible=True):
        self.type = type  # The type of menu item (e.g. "menu", "back")
        self.name = name  # The name of the menu item (e.g. "Drinks", "Settings")
        self.attributes = attributes  # Additional attributes for the menu item
        self.visible = visible  # Whether the menu item is visible or not


# The Back class represents a menu item that navigates to the previous menu.
class Back(MenuItem):
    def __init__(self, name):
        super().__init__("back", name)  # Initialize the MenuItem with the "back" type


# The Menu class represents a menu with a list of options and functionality to navigate between them.
class Menu(MenuItem):
    def __init__(self, name, attributes=None, visible=True):
        super().__init__("menu", name, attributes, visible)
        self.options = []  # List of menu options
        self.selectedOption = 0  # The currently selected option
        self.parent = None  # The parent menu (for navigating back)

    # Add multiple options to the menu
    def addOptions(self, options):
        self.options += options
        self.selectedOption = 0

    # Add a single option to the menu
    def addOption(self, option):
        self.options.append(option)
        self.selectedOption = 0

    # Set the parent menu for this menu
    def setParent(self, parent):
        self.parent = parent

    # Move to the next option in the menu
    def nextSelection(self):
        self.selectedOption = (self.selectedOption + 1) % len(self.options)

    # Get the currently selected option
    def getSelection(self):
        return self.options[self.selectedOption]


# The MenuContext class handles menu navigation and interaction with the help of a delegate.
class MenuContext:
    def __init__(self, menu, delegate):
        self.topLevelMenu = menu  # The top-level menu in the menu hierarchy
        self.currentMenu = menu  # The currently active menu
        self.delegate = delegate  # The delegate responsible for handling menu actions
        self.showMenu()  # Display the initial menu

    # Display the current menu
    def showMenu(self):
        self.display(self.currentMenu.getSelection())

    # Set a new menu as the current menu
    def setMenu(self, menu):
        if len(menu.options) == 0:
            raise ValueError("Cannot setMenu on a menu with no options")
        self.topLevelMenu = menu
        self.currentMenu = menu
        self.showMenu()

    # Display a menu item using the delegate
    def display(self, menuItem):
        self.delegate.prepareForRender(self.topLevelMenu)
        if not menuItem.visible:
            self.advance()
        else:
            self.delegate.displayMenuItem(menuItem)

    # Move to the next visible menu option
    def advance(self):
        for _ in self.currentMenu.options:
            self.currentMenu.nextSelection()
            selection = self.currentMenu.getSelection()
            if selection.visible:
                self.display(selection)
                return
        raise ValueError("At least one option in a menu must be visible!")

    # Select the current menu option and perform the appropriate action
    def select(self):
        selection = self.currentMenu.getSelection()
        if not self.delegate.menuItemClicked(selection):
            if selection.type == "menu":
                self.setMenu(selection)# The MenuItem class represents a basic menu item.
class MenuItem:
    def __init__(self, type, name, attributes=None, visible=True):
        self.type = type  # The type of menu item (e.g. "menu", "back")
        self.name = name  # The name of the menu item (e.g. "Drinks", "Settings")
        self.attributes = attributes  # Additional attributes for the menu item
        self.visible = visible  # Whether the menu item is visible or not


# The Back class represents a menu item that navigates to the previous menu.
class Back(MenuItem):
    def __init__(self, name):
        super().__init__("back", name)  # Initialize the MenuItem with the "back" type


# The Menu class represents a menu with a list of options and functionality to navigate between them.
class Menu(MenuItem):
    def __init__(self, name, attributes=None, visible=True):
        super().__init__("menu", name, attributes, visible)
        self.options = []  # List of menu options
        self.selectedOption = 0  # The currently selected option
        self.parent = None  # The parent menu (for navigating back)

    # Add multiple options to the menu
    def addOptions(self, options):
        self.options += options
        self.selectedOption = 0

    # Add a single option to the menu
    def addOption(self, option):
        self.options.append(option)
        self.selectedOption = 0

    # Set the parent menu for this menu
    def setParent(self, parent):
        self.parent = parent

    # Move to the next option in the menu
    def nextSelection(self):
        self.selectedOption = (self.selectedOption + 1) % len(self.options)

    # Get the currently selected option
    def getSelection(self):
        return self.options[self.selectedOption]


# The MenuContext class handles menu navigation and interaction with the help of a delegate.
class MenuContext:
    def __init__(self, menu, delegate):
        self.topLevelMenu = menu  # The top-level menu in the menu hierarchy
        self.currentMenu = menu  # The currently active menu
        self.delegate = delegate  # The delegate responsible for handling menu actions
        self.showMenu()  # Display the initial menu

    # Display the current menu
    def showMenu(self):
        self.display(self.currentMenu.getSelection())

    # Set a new menu as the current menu
    def setMenu(self, menu):
        if len(menu.options) == 0:
            raise ValueError("Cannot setMenu on a menu with no options")
        self.topLevelMenu = menu
        self.currentMenu = menu
        self.showMenu()

    # Display a menu item using the delegate
    def display(self, menuItem):
        self.delegate.prepareForRender(self.topLevelMenu)
        if not menuItem.visible:
            self.advance()
        else:
            self.delegate.displayMenuItem(menuItem)

    # Move to the next visible menu option
    def advance(self):
        for _ in self.currentMenu.options:
            self.currentMenu.nextSelection()
            selection = self.currentMenu.getSelection()
            if selection.visible:
                self.display(selection)
                return
        raise ValueError("At least one option in a menu must be visible!")

    # Select the current menu option and perform the appropriate action
    def select(self):
        selection = self.currentMenu.getSelection()
        if not self.delegate.menuItemClicked(selection):
            if selection.type == "menu":
                self.setMenu(selection)
            elif selection.type == "back":
                            if not self.currentMenu.parent:
                                raise ValueError("Cannot navigate back when parent is None")
                                self.setMenu(self.currentMenu.parent)
            else:
                self.display(self.currentMenu.getSelection())


# The MenuDelegate class defines the interface that a delegate must implement to handle menu actions.
class MenuDelegate:
    # Prepare for rendering the menu. Useful for updating menu item visibility.
    def prepareForRender(self, menu):
        raise NotImplementedError

    # Called when a menu item is clicked. Perform an action in response to the click.
    def menuItemClicked(self, menuItem):
        raise NotImplementedError

    # Called when a menu item should be displayed. Display the menu item in the UI.
    def displayMenuItem(self, menuItem):
        raise NotImplementedError


    #For The MenuContext Class       
    def select(self):
        selection = self.currentMenu.getSelection()
        if not self.delegate.menuItemClicked(selection):
            if selection.type == "menu":
                self.setMenu(selection)
            elif selection.type == "back":
                if not self.currentMenu.parent:
                    raise ValueError("Cannot navigate back when parent is None")
                self.setMenu(self.currentMenu.parent)
        else:
            self.display(self.currentMenu.getSelection())


# The MenuDelegate class defines the interface that a delegate must implement to handle menu actions.
class MenuDelegate:
    # Prepare for rendering the menu. Useful for updating menu item visibility.
    def prepareForRender(self, menu):
        raise NotImplementedError

    # Called when a menu item is clicked. Perform an action in response to the click.
    def menuItemClicked(self, menuItem):
        raise NotImplementedError

    # Called when a menu item should be displayed. Display the menu item in the UI.
    def displayMenuItem(self, menuItem):
        raise NotImplementedError
