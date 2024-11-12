from copy import deepcopy
import webbrowser

import flet
from flet import (
    AppBar,
    Column,
    Row,
    Container,
    IconButton,
    Icon,
    NavigationRail,
    NavigationRailDestination,
    Page,
    Text,
    Card,
    Divider,
    PopupMenuButton,
    PopupMenuItem,
)
from flet import colors, icons


class DesktopAppLayout(Row):
    """Class representing the layout of a desktop application with a side menu.

    This layout includes a navigation rail on the left and dynamic page content on the right.
    It adjusts based on screen orientation and can be resized.

    Attributes:
        page (Page): The main Flet page object where components are rendered.
        pages (list): List of navigation items paired with corresponding page content.
        navigation_items (list): Navigation items for the side menu.
        navigation_rail (NavigationRail): The navigation rail component on the left.
        content_area (Column): Container for the main content pages.
        window_size (tuple): Tuple containing the width and height of the window.
    """

    def __init__(
        self,
        title,
        page,
        pages,
        *args,
        window_size=(800, 600),
        **kwargs,
    ):
        """Initializes the desktop layout with title, navigation, and page content.

        Args:
            title (str): Title of the window.
            page (Page): Flet page where the layout is rendered.
            pages (list): List of tuples with navigation items and page contents.
            window_size (tuple, optional): Initial size of the window. Defaults to (800, 600).
        """
        super().__init__(*args, **kwargs)

        self.page = page
        self.pages = pages
        self.expand = True

        # Navigation rail setup
        self.navigation_items = [navigation_item for navigation_item, _ in pages]
        self.navigation_rail = self.build_navigation_rail()
        self.update_destinations()
        self._menu_extended = True
        self.navigation_rail.extended = True

        # Define menu panel with navigation rail on the left
        self.menu_panel = Row(
            controls=[
                self.navigation_rail,
            ],
            spacing=0,
            tight=True,
        )

        # Define main content area
        page_contents = [page_content for _, page_content in pages]
        self.content_area = Column(page_contents, expand=True)

        # Initialize screen orientation and panel visibility
        self._was_portrait = self.is_portrait()
        self._panel_visible = self.is_landscape()

        self.set_content()  # Set initial content visibility

        # Update displayed page
        self._change_displayed_page()

        # Handle window resize event
        self.page.on_resize = self.handle_resize

        # Create and assign AppBar for the application
        self.page.appbar = self.create_appbar()

        # Set window size
        self.window_size = window_size
        self.page.window_width, self.page.window_height = self.window_size

        # Set page title
        self.page.title = title

    def select_page(self, page_number):
        """Select a page by its index in the navigation rail.

        Args:
            page_number (int): Index of the page to display.
        """
        self.navigation_rail.selected_index = page_number
        self._change_displayed_page()

    def _navigation_change(self, e):
        """Handler for navigation change event.

        Args:
            e (Event): The event triggered by changing navigation.
        """
        self._change_displayed_page()
        self.page.update()  # Update page layout

    def _change_displayed_page(self):
        """Updates the visibility of pages based on the selected navigation item."""
        page_number = self.navigation_rail.selected_index
        for i, content_page in enumerate(self.content_area.controls):
            content_page.visible = page_number == i  # Show only the selected page

    def build_navigation_rail(self):
        """Constructs the navigation rail for the side menu.

        Returns:
            NavigationRail: Configured navigation rail component.
        """
        return NavigationRail(
            selected_index=0,
            label_type="none",
            on_change=self._navigation_change,
        )

    def update_destinations(self):
        """Sets destinations for navigation rail with corresponding labels."""
        self.navigation_rail.destinations = self.navigation_items
        self.navigation_rail.label_type = "all"  # Show labels for all destinations

    def handle_resize(self, e):
        """Handles window resize events.

        Args:
            e (Event): The resize event triggered by changing window dimensions.
        """
        pass  # Resize handling logic could be implemented here

    def set_content(self):
        """Sets the content layout, managing visibility and navigation panel."""
        self.controls = [self.menu_panel, self.content_area]
        self.update_destinations()
        self.navigation_rail.extended = self._menu_extended
        self.menu_panel.visible = self._panel_visible  # Set panel visibility

    def is_portrait(self) -> bool:
        """Checks if the current window orientation is portrait.

        Returns:
            bool: True if height is greater than or equal to width, indicating portrait mode.
        """
        return self.page.height >= self.page.width

    def is_landscape(self) -> bool:
        """Checks if the current window orientation is landscape.

        Returns:
            bool: True if width is greater than height, indicating landscape mode.
        """
        return self.page.width > self.page.height

    def create_appbar(self) -> AppBar:
        """Creates an AppBar with menu actions.

        Returns:
            AppBar: Configured AppBar component.
        """
        appbar = AppBar(
            toolbar_height=48,
        )

        # AppBar actions (help and report bug)
        appbar.actions = [
            Row(
                [
                    PopupMenuButton(
                        icon=icons.HELP,
                        items=[
                            PopupMenuItem(
                                icon=icons.CONTACT_SUPPORT,
                                text="Ask a question",
                            ),
                            PopupMenuItem(
                                icon=icons.BUG_REPORT,
                                text="Report a bug",
                            ),
                        ],
                    )
                ]
            )
        ]
        return appbar


def create_page(title: str, body: str):
    """Creates a page with a title and body content.

    Args:
        title (str): Title of the page.
        body (str): Body text of the page.

    Returns:
        Row: A Row component containing the page layout.
    """
    return Row(
        controls=[
            Column(
                horizontal_alignment="stretch",
                controls=[
                    Card(content=Container(Text(title, weight="bold"), padding=8)),
                    Text(body),
                ],
                expand=True,
            ),
        ],
        expand=True,
    )


def main(page: Page):
    """Main function to initialize and display the application layout.

    Args:
        page (Page): Flet Page instance where components are rendered.
    """
    pages = [
        (
            NavigationRailDestination(
                icon=icons.LANDSCAPE_OUTLINED,
                selected_icon=icons.LANDSCAPE,
                label="Menu Item A",
            ),
            create_page(
                "Example Page A",
                "This is an example page. It is a simple desktop layout with a menu on the left.",
            ),
        ),
        (
            NavigationRailDestination(
                icon=icons.PORTRAIT_OUTLINED,
                selected_icon=icons.PORTRAIT,
                label="Menu Item B",
            ),
            create_page(
                "Example Page B",
                "This is an example page. It is a simple desktop layout with a menu on the left.",
            ),
        ),
        (
            NavigationRailDestination(
                icon=icons.INSERT_EMOTICON_OUTLINED,
                selected_icon=icons.INSERT_EMOTICON,
                label="Example Page C",
            ),
            create_page(
                "Example Page C",
                "This is an example page. It is a simple desktop layout with a menu on the left.",
            ),
        ),
    ]

    # Initialize and add desktop layout to the page
    menu_layout = DesktopAppLayout(
        page=page,
        pages=pages,
        title="Basic Desktop App Layout",
        window_size=(1280, 720),
    )

    page.add(menu_layout)


if __name__ == "__main__":
    flet.app(
        target=main,
    )
