from fluent.runtime import FluentLocalization, FluentResourceLoader
import dearpygui.dearpygui as imgui


loader = FluentResourceLoader("l10n/{locale}")
localization = FluentLocalization(["en"], ["demo.ftl"], loader)


def set_locale(locale):
    global localization
    localization = FluentLocalization([locale, "en"], ["demo.ftl"], loader)
    # TODO: there has to be a better way to do this
    imgui.delete_item("main-window")
    imgui.delete_item("config-window")
    render(locale)


imgui.create_context()
imgui.create_viewport(width=1280, height=720)

with imgui.font_registry():
    with imgui.font("FiraSans.ttf", 24) as font:
        imgui.add_font_range(0x20, 0x1EFF)
        imgui.bind_font(font)


def render(locale):
    with imgui.window(
        tag="main-window",
        label=localization.format_value("label-main"),
        autosize=True,
    ):
        imgui.add_text(
            localization.format_value("close-tabs", {"count": 3}),
            tag="close-tabs",
        )
        imgui.add_checkbox(
            label=localization.format_value("confirm"), default_value=True
        )

        with imgui.group(horizontal=True):
            imgui.add_button(label=localization.format_value("close"))
            imgui.add_button(label=localization.format_value("cancel"))

    with imgui.window(
        tag="config-window",
        label=localization.format_value("label-config"),
        autosize=True,
    ):
        imgui.add_text(localization.format_value("n-tabs"))
        imgui.add_slider_int(
            tag="n-tabs",
            default_value=3,
            min_value=2,
            max_value=30,
            clamped=True,
            callback=lambda: imgui.set_value(
                "close-tabs",
                localization.format_value(
                    "close-tabs", {"count": imgui.get_value("n-tabs")}
                ),
            ),
        )
        imgui.add_text(localization.format_value("select-language"))
        imgui.add_combo(
            ("en", "pl"),
            tag="locale",
            default_value=locale,
            callback=lambda: set_locale(imgui.get_value("locale")),
        )


render("en")

imgui.setup_dearpygui()
imgui.show_viewport()
imgui.start_dearpygui()
imgui.destroy_context()
