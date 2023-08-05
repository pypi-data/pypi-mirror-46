#!/usr/bin/env python3


from io import BytesIO
from textwrap import wrap, shorten
from pathlib import Path
from configparser import ConfigParser

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
from wand.display import display

from .themes import light_theme, dark_theme


__version__ = "0.2"


class TweetGenerator:
    def __init__(self, name, handle, avatar, text, theme=None):
        self.name = name
        self.handle = handle
        self.avatar = avatar
        self.text = text
        self.filename = f"{self.name} on Twitter: {self.shorten_text(text)}.png"
        self.text = "\n".join(wrap(self.text, width=90))
        self._instance_bin = set()
        self.edgefontpath = str(Path(__file__).parent / "font/edge-icons-Regular.ttf")
        if theme == "light" or not theme:
            self.theme = light_theme["tweetmagick_theme"]
        elif theme == "dark":
            self.theme = dark_theme["tweetmagick_theme"]
        elif isinstance(theme, str):
            cfg_path = Path(theme)
            if not cfg_path.exists():
                raise ValueError(f"{cfg_path}: This path doesn't exist.")
            cfg = ConfigParser()
            cfg.read(str(cfg_path))
            cfg["DEFAULT"] = light_theme["DEFAULT"]
            self.theme = cfg["tweetmagick_theme"]
        else:
            raise ValueError(f"{theme}: Invalid theme value.")

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        for instance in self._instance_bin:
            instance.destroy()

    @staticmethod
    def shorten_text(txt):
        txtshort = shorten(txt, width=100, placeholder="...")
        txtshort = txtshort.replace("/", "_")
        return txtshort

    def tweetgen(self, verified=False, debug=False):
        avatar = self.create_circular_image(self.avatar)
        reply = self.create_icon(
            "\uf151", fg=self.theme["icon_color"], bg="transparent", size=20
        )
        retweet = self.create_icon(
            "\uf152", fg=self.theme["icon_color"], bg="transparent", size=20
        )
        if verified:
            verified = self.create_icon(
                "\uF099",
                fg=self.theme["verified_icon_color"],
                bg="transparent",
                size=16,
            )
        like = self.create_icon(
            "\uf148", fg=self.theme["icon_color"], bg="transparent", size=20
        )
        name = self.create_text(
            self.name, fg=self.theme["name_color"], bg="transparent", weight=600
        )
        handle = self.create_text(
            f"@{self.handle}", fg=self.theme["handle_color"], bg="transparent"
        )
        text = self.create_text(
            self.text, fg=self.theme["text_color"], bg="transparent"
        )
        twidth, theight = text.width, text.height
        twidth = twidth + 130 if twidth > 200 else 330
        with Image(
            width=twidth, height=150, background=Color(self.theme["background_color"])
        ) as tweet:
            tweet.format = "png"
            tweet.composite(avatar, left=10, top=20)
            tweet.composite(name, left=120, top=20)
            name_header = 120
            if verified:
                name_header = 138
                tweet.composite(verified, left=name.width + 120, top=20)
            tweet.composite(handle, left=name.width + name_header, top=21)
            tweet.composite(text, left=120, top=42)
            button_height = theight + 50
            tweet.composite(reply, left=120, top=button_height)
            tweet.composite(retweet, left=200, top=button_height)
            tweet.composite(like, left=280, top=button_height)
            if debug:
                display(tweet)
            return BytesIO(tweet.make_blob())

    def create_icon(self, codepoint, size=14, fg="black", bg="white"):
        with Drawing() as draw:
            draw.font_size = size
            draw.fill_color = Color(fg)
            draw.font = self.edgefontpath
            img = Image(width=size, height=size, background=Color(bg))
            self._instance_bin.add(img)
            draw.text(0, size, codepoint)
            draw(img)
            return img

    def create_text(self, text, size=14, fg="black", bg="white", weight=400):
        with Drawing() as draw:
            draw.font_size = size
            draw.fill_color = Color(fg)
            draw.font_family = "sans-serif"
            draw.font_weight = weight
            img = Image(width=1, height=1, background=Color(bg))
            self._instance_bin.add(img)
            draw.text(0, size, text)
            metrics = draw.get_font_metrics(img, text, multiline=True)
            img.resize(int(metrics.text_width + 1), int(metrics.text_height + 2))
            draw(img)
            return img

    def create_circular_image(self, img, radius=50):
        img = img if hasattr(img, "read") else open(img, "rb")
        imgsize = radius * 2
        img.seek(0)
        img = Image(file=img)
        self._instance_bin.add(img)
        img.resize(imgsize, imgsize)
        with img.clone() as mask:
            mask.threshold(-1)
            mask.negate()
            with Drawing() as draw:
                draw.fill_color = Color("white")
                draw.circle((radius, radius), (radius, 1))
                draw(mask)
            mask.alpha_channel = False
            img.composite(mask, operator="copy_opacity")
        return img
