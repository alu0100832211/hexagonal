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

    def award_text_block(self, user_id, badge_name, award_png_url):
        return [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Nueva medalla para {user_id}*\n¡Felicidades {user_id}! has recibido {badge_name}"
                        }
                    },
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": f"{badge_name}",
                        "emoji": True
                        },
                    "image_url": f"{award_png_url}",
                    "alt_text": f"{badge_name}"
                    }
                ]



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
