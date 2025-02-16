import barcode
import random
from barcode.writer import ImageWriter
from PIL import Image
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist

barcode_width = 300 
barcode_height = 100  
num_barcodes = 3

barcodes_e = []

start_number = 1000

background_image_path = "new.png"
background_img = Image.open(background_image_path)

x_position = (background_img.width - barcode_width) // 2
y_position_background = 0  
y_position_barcode = background_img.height - barcode_height - 230  

for i in range(num_barcodes):
    barcode_number = str(i + start_number)
    barcode_type = random.choice(['code128'])
    data = str(barcode_number)

    barcode_class = barcode.get_barcode_class(barcode_type)
    barcode_instance = barcode_class(data, writer=ImageWriter())
    barcode.base.Barcode.default_writer_options['write_text'] = False


    filename = f'{barcode_type}_{data}'
    barcode_instance.save(filename)
    barcodes_e.append(filename + ".png")

num_figures = (num_barcodes + 2) // 3  

a4_width_inches = 8.27
a4_height_inches = 11.69

for figure_index in range(num_figures):
    fig, axs = plt.subplots(1, 3, figsize=(a4_width_inches * 3, a4_height_inches))
    
    for i in range(3):
        barcode_index = figure_index * 3 + i
        if barcode_index < num_barcodes:
            barcode_filename = barcodes_e[barcode_index]
            barcode_img = Image.open(barcode_filename)
            barcode_img = barcode_img.resize((barcode_width, barcode_height))
            
            combined_width = background_img.width
            combined_height = background_img.height + barcode_height  
            combined_img = Image.new("RGB", (combined_width, combined_height))
            combined_img.paste(background_img, (0, 0))
            combined_img.paste(barcode_img, (x_position, y_position_barcode))
            
            crop_region = (0, 0, combined_width, background_img.height)
            combined_img = combined_img.crop(crop_region)
            combined_img=combined_img.resize((180,250))
            axs[i].imshow(combined_img)
            axs[i].axis('off')
    
    plt.tight_layout()
    plt.show()
