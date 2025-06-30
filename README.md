# MkDocs Topic Nav Plugin

This plugin is intended to enable a clear view of distinct topics within a large
documentation tree, while still allowing links between those topics. It does this by
modifying the nav in two ways:

- Filtering the nav of the given level 2 pages to display only the index of their
  children instead of the full tree
- Filtering all siblings from the nav in level 3 or deeper pages

This plugin is intended to be used with the material theme, but may work with others. It
works best with navigation.tabs and navigation.indexes enabled so that the root sections
are level 2 nested and its pages are rendered as the header of the nav with the topics
at the root.

Example config:

```yaml
plugins:
  - topic-nav:
      sections:
        - Getting Started
        - Developer Environment
        - Software Products
```
