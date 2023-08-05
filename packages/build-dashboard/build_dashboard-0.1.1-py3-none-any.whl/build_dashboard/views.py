"""
A module containing the views for build_dashboard
"""
from asciimatics.widgets import Frame, Layout, Label, Background, Divider, ListBox, MultiColumnListBox
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from datetime import datetime
from build_dashboard import logger

class BuildbotView(Frame):
    """ Entrypoint view of the build-dashboard.

    Args:
        screen: The screen used for displaying the view.
        model: The BuildbotModel for retrieving data.
    """

    def __init__(self, screen, model):
        super(BuildbotView, self).__init__(screen, screen.height, screen.width)
        self.set_theme("monochrome")
        self.model = model
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._render_builders(layout) 
        self.fix()


    def _render_builders(self, layout):
        """Renders the list of builders and their build status.

        Args:
            layout (:obj:`Layout`): The layout to which to add the builders

        """
        layout.add_widget(Label("Buildbot"))
        layout.add_widget(Divider())
        builders = [ BuildbotView.format_builder_info(builder) 
            for builder in self.model.builders() ]
        logger.debug("Found %s builder.", len(builders))
        self.builder_list = MultiColumnListBox(20,
            columns=[20, 40, 20, 20],
            options=builders,
            titles=['Builder', 'Description', 'Last Build', 'Status'],
            name='builder')
        layout.add_widget(self.builder_list)
    
    def update(self, frame):
        builders = [ BuildbotView.format_builder_info(builder) 
            for builder in self.model.builders() ]
        logger.debug("Found %s builder.", len(builders))
        self.builder_list.options = builders
        Frame.update(self, frame) 

        
    @staticmethod
    def format_builder_info(builder):
        """ Formats the merged builder and builds message into the columns
        for a :obj:`MultiColumnListBox` in :obj:`BuildbotView`.

        Args:
            builder (:obj:`dict`): A builder :obj:`dict` with the merged
                builds :obj:`dict`.

        Returns:
            A :obj:`tuple` with four columns and id.
        """
        name = builder['name'] or 'None'
        description = builder['description'] or 'None'
        last_build = builder['builds'][-1]
        if last_build['complete']:
            last_build_time = datetime.utcfromtimestamp(
                        last_build['complete_at']).strftime(
                                '%Y-%m-%d %H:%M:%S')
        else:
            last_build_time = ''
        state_string = last_build['state_string']
        formatted = ([name,
            description,
            last_build_time,
            state_string],
            name)
        return formatted
