from copy import deepcopy
from typing import Any

from mkdocs.config import base
from mkdocs.config import config_options as c
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Navigation, Page, Section


class TopicNavConfig(base.Config):
    sections = c.ListOfItems(c.Type(str), default=[])


class TopicNavPlugin(BasePlugin[TopicNavConfig]):
    """Modify the nav to show focused topics within a varied docs structure."""

    sections: list[str]

    def on_config(self, config: MkDocsConfig):
        self.sections = config.plugins["topic-nav"].config.sections

    def on_page_context(
        self, context: dict[str, Any], page: Page, config, nav: Navigation, **kwargs
    ):
        """Hook called by mkdocs when rendering a specific page."""
        if len(page.ancestors) == 1 and page.title in self.sections:
            # This page is a root section index configured to be filtered
            context["nav"] = self._filter_section_nav(nav)
        elif any(s.title in self.sections for s in page.ancestors):
            # This page is a topic section index (or child of a section index)
            # Only display this topic and its child pages
            context["nav"] = self._filter_topic_nav(nav, page)

        return context

    def _filter_section_nav(self, nav: Navigation):
        """Filter nav to this section and its topic indexes without their children."""

        new_nav = deepcopy(nav)
        for item in new_nav.items:
            if isinstance(item, Section) and item.title in self.sections:
                # This is the a root section within the nav panel
                for topic in item.children:
                    if isinstance(topic, Section):
                        # This is a topic section
                        # Filter nav to display only the index page of the topic
                        topic.children = [
                            p
                            for p in topic.children
                            if isinstance(p, Page) and p.is_index
                        ]

        return new_nav

    @staticmethod
    def _filter_topic_nav(nav: Navigation, page: Page):
        """Filter nav to this topic and its child pages."""

        root_section = page.ancestors[-1]
        topic_section = page.ancestors[-2]

        new_nav = deepcopy(nav)
        for item in new_nav.items:
            if item.title == root_section.title:
                # This is the topic section containing the topic for the current page
                # Filter nav to only display this topic section and its pages
                item.children = [
                    i
                    for i in item.children
                    if i.title == topic_section.title or isinstance(i, Page)
                ]

        return new_nav
