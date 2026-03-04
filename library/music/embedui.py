import discord

from discord.ui import View, Select

class QueueSelect(Select):
    def __init__(self, player):
        self.player = player

        queue = list(player.queue.queue)[:25]

        if not queue:
            options = [
                discord.SelectOption(
                    label="Queue Is Empty",
                    value="none",
                    description="Add Some Songs First"
                )
            ]
        else:
            options = [
                discord.SelectOption(
                    label=str(song)[:100],
                    value=str(i)
                )
                for i, song in enumerate(queue)
            ]

        super().__init__(
            placeholder="Select A Song To Play",
            options=options,
            disabled=not bool(player.queue.queue)
        )

class QueueView(View):
    def __init__(self, player):
        super().__init__(timeout=60)

        if not player.queue.queue:
            return

        self.add_item(QueueSelect(player))
