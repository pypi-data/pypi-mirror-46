from configparser import ConfigParser


light_theme = ConfigParser()
light_theme["tweetmagick_theme"] = {
    "text_color": "#14171a",
    "name_color": "#14171a",
    "handle_color": "#657786",
    "icon_color": "#657786",
    "verified_icon_color": "#1da1f2",
    "background_color": "#ffffff",
}
light_theme["DEFAULT"] = light_theme["tweetmagick_theme"]

dark_theme = ConfigParser()
dark_theme["tweetmagick_theme"] = {
    "text_color": "#ffffff",
    "name_color": "#ffffff",
    "handle_color": "#8899a6",
    "icon_color": "#8899a6",
    "verified_icon_color": "#ffffff",
    "background_color": "#15202b",
}
