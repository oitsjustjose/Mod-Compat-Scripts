"""
Author: Jose Stovall | oitsjustjose
A script for iterating over every plank in the game (provided by CraftDumper)
    Uses this plank to create compatibility for all Woodcutting recipes from Druidcraft
"""

import json
import os
from typing import List, Tuple, Union


class Block:
    """A block constructor that makes my life easier"""

    def __init__(self, resource_location: str):
        modid, path = resource_location.replace("\n", "").split(":")
        self._modid = modid
        self._path = path

    def get_modid(self) -> str:
        """Gets the modid of the Block instance"""
        return self._modid

    def get_path(self) -> str:
        """Gets the path of the Block instance"""
        return self._path

    def get_resource_location(self) -> str:
        """Gets the resource_location of the Block instance"""
        return f"{self._modid}:{self._path}"

    def __eq__(self, o: object) -> bool:
        return (
            isinstance(o, Block)
            and o.get_modid() == self.get_modid()
            and o.get_path() == self.get_path()
        )

    def __str__(self) -> str:
        return self.get_resource_location()

    def __unicode__(self):
        return self.get_resource_location()

    def __repr__(self):
        return self.get_resource_location()


def try_get(
    all_blocks: List[Block], source: Block, variant: str, tag_name: str
) -> Union[Block, None]:
    """
    Tries to get the fence for a given block if it can.
        If it cannot then it it will return None
    """
    modid = source.get_modid()
    path = source.get_path()
    base: str = (
        source.get_resource_location()
        .replace(f"_{tag_name}", "")
        .replace(f"{tag_name}_", "")
    )

    variants: List[Block] = [
        Block(f"{base}_{variant}"),
        Block(f"{variant}_{base}"),
        Block(f"{base}_{tag_name}_{variant}"),
        Block(f"{variant}_{base}_{tag_name}"),
        Block(f"{modid}:{variant}_{path}"),
        # modid:{a}_log -> modid:{a}_stripped_log
        Block(f"{modid}:{path.replace('_log', '')}_{variant}_{tag_name}"),
    ]

    for var in variants:
        if var in all_blocks:
            return var
    return None


def generate_plank_crafting(all_blocks: List[Block]) -> None:
    """
    Generates the plank -> <ITEM> recipes for Woodcutting
    """
    variant_map = {
        "slab": 2,
        "stair": 1,
        "stairs": 1,
        "fence": 1,
        "fence_gate": 1,
        "gate": 1,
        "button": 4,
        "door": 1,
        "sign": 1,
        "trapdoor": 2,
        "pressure_plate": 3,
    }

    anti_matchers = [
        "vertical",
        "slab",
        "stair",
        "fence",
        "gate",
        "chipped:",
        "minecraft:",
        "quark:",
        "druidcraft:",
    ]

    # Filter out any things we don't want to see in the anti_matchers list
    planks: List[Block] = list(
        filter(
            lambda x: "planks" in x.get_resource_location()
            and not any(y in x.get_resource_location() for y in anti_matchers),
            all_blocks,
        )
    )

    created_count = 0

    for plank in planks:
        for_plank: List[Tuple[Block, int]] = [
            (try_get(all_blocks, plank, var, "planks"), cnt)
            for var, cnt in variant_map.items()
        ]

        for_plank: List[Tuple[Block, int]] = list(
            filter(lambda x: x[0] is not None, for_plank)
        )

        for (result, count) in for_plank:
            filename = f"{result.get_path()}_from_woodcutting_{plank.get_path()}.json"
            data = {
                "type": "druidcraft:woodcutting",
                "ingredient": {"item": plank.get_resource_location()},
                "result": result.get_resource_location(),
                "count": count,
            }

            with open(f"./out/woodcutting/{filename}", "w") as file:
                file.write(json.dumps(data))

        created_count += len(for_plank)
    print(f"Created {created_count} new plank recipes for woodcutter")


def generate_log_stripping(all_blocks: List[Block]) -> None:
    """
    Generates Woodcutting recipes to strip logs
    """
    logs: List[Block] = list(
        filter(
            lambda x: x.get_resource_location().endswith("log")
            and "minecraft:" not in x.get_resource_location()
            and "druidcraft:" not in x.get_resource_location()
            and "stripped" not in x.get_resource_location(),
            all_blocks,
        )
    )

    created_count = 0

    for log in logs:
        stripped_log = try_get(all_blocks, log, "stripped", "log")
        if not stripped_log:
            print(f"Could not find stripped variant of {log.get_resource_location()}")
            continue

        filename = f"{stripped_log.get_path()}_from_{log.get_path()}_stripping_woodcutting.json"
        data = {
            "type": "druidcraft:woodcutting",
            "ingredient": {"item": log.get_resource_location()},
            "result": stripped_log.get_resource_location(),
            "count": 1,
        }

        with open(f"./out/woodcutting/{filename}", "w") as file:
            file.write(json.dumps(data))

        created_count += 1
    print(f"Created {created_count} new log -> stripped log recipes")


def main() -> None:
    """
    The main Python run-function for this file
    """
    all_blocks: List[Block] = []
    with open("./all_blocks.txt", "r") as file:
        all_blocks = [Block(x) for x in file.readlines()]

    if not os.path.exists("./out/woodcutting"):
        os.makedirs("./out/woodcutting")

    generate_plank_crafting(all_blocks)
    generate_log_stripping(all_blocks)


if __name__ == "__main__":
    main()
