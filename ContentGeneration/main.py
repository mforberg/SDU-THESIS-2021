import map_analysis


class Main:

    def run(self):
        x, y = map_analysis.MapAnalysis().run()
        print(len(x))
        print(len(y))

    # def build_surface(self):
    #     blocks = []
    #     for value in total_surface_dict.values():
    #         block = value["block"]
    #         block.type = PACKED_ICE
    #         blocks.append(block)
    #     client.spawnBlocks(Blocks(blocks=blocks))


if __name__ == '__main__':
    Main().run()
