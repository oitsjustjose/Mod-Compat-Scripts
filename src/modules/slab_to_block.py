"""
Author: Jose Stovall | oitsjustjose
A script for iterating over every slab in the game (provided by CraftDumper)
    Turns 2 slabs into 1 source block of slab
"""

import json
import os
from typing import List
from ..util.file import create_requisite_files


JSON_TEMPLATE = {
    "type": "minecraft:crafting_shapeless",
    "ingredients": [],
    "result": {"item": "", "count": 1},
}

TRANSMUTATIONS = ["s", "_planks"]


def main() -> None:
    """
    The main Python run-function for this file
    """
    create_requisite_files()

    if not os.path.exists("./out/slab_to_block"):
        os.makedirs("./out/slab_to_block")

    slabs: List[str]
    all_blocks: List[str]
    with open("./all_blocks.txt", "r") as file:
        all_blocks = [x.replace("\n", "") for x in file.readlines()]
    with open("./slabs.txt", "r") as file:
        slabs = [x.replace("\n", "") for x in file.readlines()]

    for slab in slabs:
        block = slab.replace("_slab", "").replace("slab_", "")

        if block not in all_blocks:
            found = False
            for trns in TRANSMUTATIONS:
                block_alt = f"{block}{trns}"
                if block_alt in all_blocks:
                    block = block_alt
                    found = True
                    break
            if not found:
                print(f"Neither {block} nor {block_alt} exist in block list")
                continue

        recipe = JSON_TEMPLATE.copy()
        recipe["ingredients"] = [{"item": slab}, {"item": slab}]
        recipe["result"]["item"] = block

        block_cln = block[block.index(":") + 1 :]
        slab_cln = slab[slab.index(":") + 1 :]
        file_name = f"{block_cln}_from_two_{slab_cln}.json"
        with open(f"./out/slab_to_block/{file_name}", "w") as file:
            file.write(json.dumps(recipe, indent=2))


if __name__ == "__main__":
    main()
