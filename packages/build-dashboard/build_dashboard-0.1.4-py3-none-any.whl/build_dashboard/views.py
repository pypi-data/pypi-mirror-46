from asciimatics.widgets import Frame, Layout, Label, Divider, MultiColumnListBox, ListBox
from asciimatics.effects import Print
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import NextScene
from asciimatics.screen import Screen
from datetime import datetime
from build_dashboard import logger

class BuildersView(Frame):
    """ Entrypoint view of the build-dashboard.

    Args:
        screen: The screen used for displaying the view.
        model: The BuildbotModel for retrieving data.
    """

    def __init__(self, screen, model):
        super(BuildersView, self).__init__(screen, screen.height, screen.width, can_scroll=False)
        self.set_theme("monochrome")
        self.model = model
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label("Buildbot"))
        layout.add_widget(Divider())
        builders = [ BuildersView.format_builder_info(builder) 
            for builder in self.model.builders() ]
        logger.debug("Found %s builder.", len(builders))
        self.builder_list = MultiColumnListBox(screen.height-4,
            columns=["20%", "30%", "15%", "35%"],
            options=builders,
            on_select=self._select,
            titles=['Builder', 'Description', 'Last Build', 'Status'],
            name='builder')
        layout.add_widget(self.builder_list)
        self.fix()

    def _select(self):
        self.save()
        self.model.select_builder(self.data['builder'])
        raise NextScene(name='BuildsView')
    
    def update(self, frame):
        builders = [ BuildersView.format_builder_info(builder) 
            for builder in self.model.builders() ]
        logger.debug("Found %s builder.", len(builders))
        self.builder_list.options = builders
        self.model.select_builder(builders[0][1])
        Frame.update(self, frame) 

    def process_event(self, event):
        if (event is not None and
                isinstance(event, KeyboardEvent)):
            if event.key_code == ord('f') or event.key_code == ord('F'):
                self.save()
                self.model.run_force_scheduler(self.data['builder'])

        return super(BuildersView, self).process_event(event)
        
    @staticmethod
    def format_builder_info(builder):
        """ Formats the merged builder and builds message into the columns
        for a :obj:`MultiColumnListBox` in :obj:`BuildersView`.

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
        builderid = builder['builderid']
        formatted = ([name,
            description,
            last_build_time,
            state_string],
            builderid)
        return formatted

class BuildsView(Frame):
    """Frame to display the list of builds for a builder

    Args:
        screen (:obj:`Screen`): The screen object
        model: The Buildbot model
    """
    def __init__(self, screen, model):
        super(BuildsView, self).__init__(screen, screen.height, screen.width, can_scroll=False)
        self.set_theme("monochrome")
        self.model = model
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self.builds = []
        layout.add_widget(Label("Builds"))
        layout.add_widget(Divider())
        layout.add_widget(MultiColumnListBox(screen.height - 4,
            columns=["20%", "15%", "15%", "50%"],
            options=self.builds,
            on_select=self._select,
            titles=['Number', 'Started At', 'Completed At', 'Status'],
            name='build'))
        self.fix()

    def update(self, frame):
        if self.model.builder:
            builds = [ BuildsView.format_build_info(builder) 
                for builder in self.model.builder.get('builds',[]) ]
            logger.debug("Found %s builds.", len(builds))
            self.builds.clear()
            self.builds.extend(builds)
        Frame.update(self, frame)
    
    def _select(self):
        self.save()
        self.model.select_build(self.data['build'])
        raise NextScene(name="StepsView")
    
    def process_event(self, event):
        if (event is not None and isinstance(event, KeyboardEvent)):
            if event.key_code == -1:
                raise NextScene(name="BuildersView")
        return super(BuildsView, self).process_event(event)

    @staticmethod
    def format_build_info(build):
        number = build['number']
        if build['complete']:
            complete_time = datetime.utcfromtimestamp(
                    build['complete_at']).strftime('%Y-%m-%d %H:%M:%S')
        else:
            complete_time = ''
        start_time = datetime.utcfromtimestamp(
                    build['started_at']).strftime('%Y-%m-%d %H:%M:%S')
        state_string = build['state_string']
        buildid = build['buildid']
        formatted = ([str(number), start_time, complete_time, state_string], buildid)
        return formatted

class StepsView(Frame):
    """Frame to display the list of steps for a build

    Args:
        screen (:obj:`Screen`): The screen object
        model: The Buildbot model
    """
    def __init__(self, screen, model):
        super(StepsView, self).__init__(screen, screen.height, screen.width, can_scroll=False)
        self.set_theme("monochrome")
        self.model = model
        self.steps = []
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label("Steps"))
        layout.add_widget(Divider())
        layout.add_widget(MultiColumnListBox(screen.height - 4,
                columns=["20%", "15%", "15%", "50%"],
                options=self.steps,
                on_select=self._select,
                titles=['Number', 'Started At', 'Completed At', 'Status'],
                name='step'))

        self.fix()

    def _select(self):
        self.save()
        self.model.select_log(self.data['step'])
        raise NextScene(name='LogView')

    def update(self, frame):
        if self.model.steps:
            steps = [ StepsView.format_step_info(step) 
                for step in self.model.steps ]
            logger.debug("Found %s steps.", len(steps))
            self.steps.clear()
            self.steps.extend(steps)
        Frame.update(self, frame)
    
    def process_event(self, event):
        if (event is not None and isinstance(event, KeyboardEvent)):
            if event.key_code == -1:
                raise NextScene(name="StepsView")
        return Frame.process_event(self, event)

    @staticmethod
    def format_step_info(build):
        number = build['number']
        if build['complete']:
            complete_time = datetime.utcfromtimestamp(
                    build['complete_at']).strftime('%Y-%m-%d %H:%M:%S')
        else:
            complete_time = ''
        start_time = datetime.utcfromtimestamp(
                    build['started_at']).strftime('%Y-%m-%d %H:%M:%S')
        state_string = build['state_string']
        stepid = build['stepid']
        formatted = ([str(number), start_time, complete_time, state_string], stepid)
        return formatted


class LogView(Frame):
    """Frame to display the logs

    Args:
        screen (:obj:`Screen`): The screen object
        model: The Buildbot model
    """
    def __init__(self, screen, model):
        super(LogView, self).__init__(screen, screen.height, screen.width, can_scroll=False)
        self.set_theme("monochrome")
        self.model = model
        self.log_lines = []
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label("Logs"))
        layout.add_widget(Divider())
        layout.add_widget(ListBox(
            screen.height - 4,
            options=self.log_lines,
            add_scroll_bar=True))
        self.fix()

    def update(self, frame):
        if self.model.log:
            self.log_lines.clear()
            self.log_lines.extend(LogView.format_logs(self.model.log))
        Frame.update(self, frame)
    
    def process_event(self, event):
        if (event is not None and isinstance(event, KeyboardEvent)):
            if event.key_code == -1:
                raise NextScene(name="StepsView")
        return Frame.process_event(self, event)

    @staticmethod
    def format_logs(content):
        lines = content.splitlines()
        counter = 0
        lines = [ (line[1:], index) for index, line in enumerate(lines) ]
        return lines

