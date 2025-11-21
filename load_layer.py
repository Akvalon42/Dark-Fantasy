import pytmx
from platform import Platform
from coin import Coin
def load_layer(all_sprites, platforms, coins, level ):
    tmx_map = pytmx.load_pygame(f"maps/LVL_{level}.tmx")
    for layer in tmx_map:
        if layer.name == "карта":
            for x, y, gid in layer:
                tile = tmx_map.get_tile_image_by_gid(gid)

                if tile:
                    platform = Platform(tile, x * tmx_map.tilewidth, y * tmx_map.tileheight,
                                        tmx_map.tilewidth,
                                        tmx_map.tileheight)
                    all_sprites.add(platform)
                    platforms.add(platform)
        elif layer.name == "монеты":
            for x, y, gid in layer:
                tile = tmx_map.get_tile_image_by_gid(gid)

                if tile:
                    coin = Coin(x * tmx_map.tilewidth, y * tmx_map.tileheight)
                    all_sprites.add(coin)
                    coins.add(coin)
    return tmx_map