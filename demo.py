from fluent.runtime import FluentLocalization, FluentResourceLoader
from imgui.integrations.pygame import PygameRenderer
import OpenGL.GL as gl
import datetime
import pygame
import imgui
import sys

# Fluent setup
loader = FluentResourceLoader("l10n/{locale}")
localization = FluentLocalization(["en"], ["demo.ftl"], loader)

# ImGui backend setup
pygame.init()
size = 800, 600

pygame.display.set_mode(
    size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE
)

# ImGui setup
imgui.create_context()
impl = PygameRenderer()

io = imgui.get_io()
io.display_size = size

new_font = io.fonts.add_font_from_file_ttf(
    "FiraSans.ttf", 24, glyph_ranges=io.fonts.get_glyph_ranges_latin()
)
impl.refresh_font_texture()

# UI/application state
checked = True
n_tabs = 3
locale_idx = 0
locales = ["en", "pl"]

# Render loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        impl.process_event(event)
    impl.process_inputs()

    # ImGui frame rendering
    imgui.new_frame()
    with imgui.font(new_font):
        # Main window
        imgui.begin(f"{localization.format_value('label-main')}##main", True)

        imgui.text(localization.format_value("close-tabs", {"count": n_tabs}))
        _, checked = imgui.checkbox(
            localization.format_value("confirm"), checked
        )

        imgui.button(localization.format_value("close"))
        imgui.same_line()
        imgui.button(localization.format_value("cancel"))

        imgui.end()

        # Configuration window
        imgui.begin(
            f"{localization.format_value('label-config')}##config", True
        )

        imgui.text(localization.format_value("n-tabs"))
        _, n_tabs = imgui.slider_int("##n-tabs", n_tabs, 2, 30)

        imgui.text(localization.format_value("select-language"))
        clicked, locale_idx = imgui.combo("##locale", locale_idx, locales)
        if clicked:
            localization = FluentLocalization(
                [locales[locale_idx], "en"], ["demo.ftl"], loader
            )

        imgui.end()

        # Current datetime
        imgui.begin(f"{localization.format_value('label-datetime')}##datetime")

        imgui.text(
            localization.format_value("now", {"now": datetime.datetime.now()})
        )

        imgui.end()

    # Render frame
    gl.glClearColor(0.1, 0.1, 0.1, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    imgui.render()
    impl.render(imgui.get_draw_data())
    pygame.display.flip()
