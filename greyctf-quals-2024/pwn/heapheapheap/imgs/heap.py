# Script to generate the HEAP layout svg

import svgwrite
import svgwrite.drawing

heap_len = 0x1000 // 8
heap_height = 128

node_len = 0x28 / 8 * 4

img_len = int(heap_len * 1.6)
img_height = heap_height + int(heap_len * 0.425)


print((img_len, img_height))

offset_x = 0.55 * heap_len
offset_y = 0.05 * heap_len

white = "#ffffff"
black = "#000000"

red = "#ff0000"

cyan = "#00ffff"
magenta = "#ff00ff"
orange = "#ffa500"

text_style = "font-size:25px; font-family:Arial"

dwg = svgwrite.Drawing('heap.svg', (img_len, img_height), profile="full")
# background
dwg.add(dwg.rect((0, 0), (img_len, img_height), fill = white))

# heap
dwg.add(dwg.rect((offset_x, offset_y), (heap_len, heap_height / 2), fill=white, stroke=black))
dwg.add(dwg.rect((offset_x, offset_y + heap_height / 2), (heap_len, heap_height / 2), fill=white, stroke=black))

def draw_chunk(offset, data_len):
    dwg.add(dwg.rect(offset, (node_len, heap_height / 2), fill=cyan, stroke=black))
    dwg.add(dwg.rect((offset[0] + node_len, offset[1]), (node_len, heap_height / 2), fill=magenta, stroke=black))
    dwg.add(dwg.rect((offset[0] + node_len * 2, offset[1]), (node_len, heap_height / 2), fill=cyan, stroke=black))
    dwg.add(dwg.rect((offset[0] + node_len * 3, offset[1]), (data_len, heap_height / 2), fill=orange, stroke=black))

# first chunk
first_chunk_len = 0x700 + 0x28 * 3
draw_chunk((offset_x, offset_y), first_chunk_len / 8 - node_len * 3)

# second chunk
second_chunk_len = 0x300 + 0x28 * 3
print(second_chunk_len / 8 - node_len * 3)
assert(second_chunk_len / 8 - node_len * 3 > 0)
draw_chunk((offset_x + first_chunk_len / 8, offset_y), second_chunk_len / 8 - node_len * 3)

# third chunk
third_chunk_len = 0x1000 - first_chunk_len - second_chunk_len
draw_chunk((offset_x + (first_chunk_len + second_chunk_len) / 8, offset_y), third_chunk_len / 8 - node_len * 3)

# misaligned chunk
misaligned_chunk_offset = offset_x + first_chunk_len / 8 - node_len * 0.6
dwg.add(dwg.rect((misaligned_chunk_offset, offset_y + heap_height / 2), (node_len, heap_height / 2), fill=red, stroke=black))

# leaking chunks
dwg.add(dwg.rect((misaligned_chunk_offset + node_len, offset_y + heap_height / 2), (second_chunk_len / 8, heap_height / 2), fill=orange, stroke=black))
dwg.add(dwg.rect((misaligned_chunk_offset + node_len + second_chunk_len / 8, offset_y + heap_height / 2), (node_len, heap_height / 2), fill=cyan, stroke=black))


# descriptions
dwg.add(dwg.text("Initialization", insert=(0.05 * heap_len, offset_y + heap_height * 0.35), fill = black,  style = text_style))
dwg.add(dwg.text("Image Address Leak", insert=(0.05 * heap_len, offset_y + heap_height * 0.85), fill = black, style = text_style))

# legend
legend_box_size = 1 / 6
dwg.add(dwg.rect((offset_x, offset_y + heap_height + heap_height * legend_box_size), (heap_height * legend_box_size, heap_height * legend_box_size), fill=cyan, stroke=black))
dwg.add(dwg.text("Management Node", insert=(offset_x + heap_height * legend_box_size * 1.5, offset_y + heap_height + heap_height * legend_box_size * 1.9), fill=black, style = text_style))
dwg.add(dwg.rect((offset_x, offset_y + heap_height + heap_height * legend_box_size * (2 + 1)), (heap_height * legend_box_size, heap_height * legend_box_size), fill=magenta, stroke=black))
dwg.add(dwg.text("Heap Node", insert=(offset_x + heap_height * legend_box_size * 1.5, offset_y + heap_height + heap_height * legend_box_size * (2 + 1.9)), fill=black, style = text_style))
dwg.add(dwg.rect((offset_x, offset_y + heap_height + heap_height * legend_box_size * (4 + 1)), (heap_height * legend_box_size, heap_height * legend_box_size), fill=orange, stroke=black))
dwg.add(dwg.text("Data", insert=(offset_x + heap_height * legend_box_size * 1.5, offset_y + heap_height + heap_height * legend_box_size * (4 + 1.9)), fill=black, style = text_style))
dwg.add(dwg.rect((offset_x, offset_y + heap_height + heap_height * legend_box_size * (6 + 1)), (heap_height * legend_box_size, heap_height * legend_box_size), fill=red, stroke=black))
dwg.add(dwg.text("Misaligned Chunk / Bug", insert=(offset_x + heap_height * legend_box_size * 1.5, offset_y + heap_height + heap_height * legend_box_size * (6 + 1.9)), fill=black, style = text_style))

dwg.save()