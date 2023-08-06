import os
import warnings

from sphinx.errors import ConfigError

from .version import version as __version__

assert __version__

__copyright__ = "2018 Applied Brain Research"
current_dir = os.path.abspath(os.path.dirname(__file__))


def setup(app):
    app.add_html_theme(
        "nengo_sphinx_theme", os.path.join(current_dir, "theme")
    )
    # Add CSS files
    app.add_stylesheet(os.path.join("css", "normalize.css"))
    app.add_stylesheet(os.path.join("css", "bootstrap.css"))
    app.add_stylesheet(os.path.join("css", "mmenu.all.css"))
    app.add_stylesheet(os.path.join("css", "components.css"))
    app.add_stylesheet(os.path.join("css", "nengo.css"))

    # Add JS files
    app.add_javascript(os.path.join("js", "modernizr.js"))
    app.add_javascript(os.path.join("js", "underscore.min.js"))
    app.add_javascript("doctools.js")
    app.add_javascript(os.path.join("js", "searchtools.js"))
    app.add_javascript(os.path.join("js", "webflow.js"))
    app.add_javascript(os.path.join("js", "bootstrap.js"))
    app.add_javascript(os.path.join("js", "mmenu.all.min.js"))
    app.add_javascript(os.path.join("js", "fontawesome.js"))
    app.add_javascript(os.path.join("js", "custom.js"))

    # validate config
    def validate_config(_, config):
        theme_config = getattr(config, "html_theme_options", {})

        # check nengo_logo config
        html_logo = getattr(config, "html_logo", "")
        nengo_logo = theme_config.get("nengo_logo", None)

        if html_logo and nengo_logo:
            warnings.warn("'html_logo' and 'nengo_logo' are both set; "
                          "'nengo_logo' will take precedence")
        elif html_logo:
            warnings.warn("Logo set using 'html_logo', consider using "
                          "'nengo_logo' instead")

        # check versioning config
        html_context = getattr(config, "html_context", {})
        releases = html_context.get("releases", "").split(",")
        building = html_context.get("building_version", "")

        if "latest" in releases:
            raise ConfigError(
                "nengo_sphinx_theme.ext.versions: 'latest' cannot be a "
                "release name (link to the most up-to-date version of the "
                "docs will be added automatically)")

        if building == "":
            warnings.warn(
                "'building_version' not set, versions will not be rendered")

        # check Google Analytics ID
        analytics_id = theme_config.get("analytics_id", None)
        if analytics_id is not None and not analytics_id.startswith("UA-"):
            warnings.warn("'analytics_id' looks strange. It should look like "
                          "'UA-000000-2'; got %r" % (analytics_id,))

    app.connect("config-inited", validate_config)
