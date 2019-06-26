#encoding: utf-8
"""
Esta clase está pensada
para enviar mensajes de slakc
con un formato bonito.
"""

class TextBlock:
    def __init__(self):
        pass

    def badges_text_block(self, badges):
        print(badges)
        text_blocks = []
        for badge in badges:
            image = badges[badge]['image']
            title = badges[badge]['name']
            for thing in self._section_with_image(text = title, image_url = image):
                text_blocks.append(thing)
        return text_blocks

    def _section_with_image(self, text, image_url):
        return [{
                "type": "divider"
                },
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text,
                    },
                "accessory": {
                    "type": "image",
                    "image_url": image_url,
                    "alt_text": "plants"
                    }
                }]
