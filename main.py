from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock


class FarmGameApp(App):
    SEED_COST = 5
    SELL_PRICE = 15
    GROW_TIME = 5

    def build(self):
        self.coins = 20
        self.tiles = []

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.hud = Label(
            text="",
            font_size=22,
            halign="center",
        )
        self.update_hud()

        grid = GridLayout(cols=4, spacing=8)

        for i in range(16):
            btn = Button(text="EMPTY", font_size=22)
            btn.bind(on_press=lambda instance, idx=i: self.on_tile(idx))
            grid.add_widget(btn)

            self.tiles.append({
                "stage": 0,
                "btn": btn
            })

        root.add_widget(self.hud)
        root.add_widget(grid)

        Clock.schedule_interval(self.tick, 1.0)

        return root

    def update_hud(self):
        self.hud.text = (
            f"Coins: {self.coins}\n"
            f"Plant cost: {self.SEED_COST} | Harvest reward: {self.SELL_PRICE}"
        )

    def on_tile(self, i):
        tile = self.tiles[i]

        # Empty land: plant seed
        if tile["stage"] == 0:
            if self.coins >= self.SEED_COST:
                self.coins -= self.SEED_COST
                tile["stage"] = 1
                tile["btn"].text = "SEED"

        # Ready crop: harvest
        elif tile["stage"] >= self.GROW_TIME:
            self.coins += self.SELL_PRICE
            tile["stage"] = 0
            tile["btn"].text = "EMPTY"

        self.update_hud()

    def tick(self, dt):
        for tile in self.tiles:
            if 1 <= tile["stage"] < self.GROW_TIME:
                tile["stage"] += 1

                if tile["stage"] >= self.GROW_TIME:
                    tile["btn"].text = "READY"
                else:
                    tile["btn"].text = f"GROW {tile['stage']}"


if __name__ == "__main__":
    FarmGameApp().run()
