# -------- Import libraries -------- #
# Built-in
import copy

# 3rd party
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont


def image_grid(images, columns=5):
    """Takes an array of images and a column count, and generates a grid using the images"""

    # Count the images and set row/column count
    image_count = len(images)

    # If the number of images is less than the number of columns,
    # set the number of columns to the number of images
    column_count = min(image_count, columns)

    # Avoid divide by 0 error
    if column_count < 1:
        return None

    # Set row count
    rows = image_count // column_count
    if image_count % column_count != 0:
        rows += 1

    # Create arrays of 0s
    left_x, top_y = [0] * column_count, [0] * rows

    # Calculate max image width and height for each row/column
    for index, image in enumerate(images):
        horizontal_index, vertical_index = index % column_count, index // column_count
        left_x[horizontal_index] = max(left_x[horizontal_index], image.size[0])
        top_y[vertical_index] = max(top_y[vertical_index], image.size[1])

    # Set column width and row height for each row/column
    left_x, top_y = np.cumsum([0] + left_x), np.cumsum([0] + top_y)

    # Create blank image
    image_grid = Image.new('RGB', (left_x[-1], top_y[-1]), color='white')

    # Add images to grid
    for index, image in enumerate(images):
        column = index % column_count
        row = index // column_count # Note: Max height for last row is irrelevant because there is unlimited space below

        if columns == 1:
            x_offset = 0
        else:
            x_offset = (left_x[column + 1] - left_x[column])/2 - image.size[0]/2

        x = left_x[column] + x_offset
        y_offset = (top_y[row + 1] - top_y[row])/2 - image.size[1]/2
        if y_offset < 0:
            y_offset = 0
        y = top_y[row] + y_offset

        x = int(x)
        y = int(y)
        image_grid.paste(image, (x, y))

    return image_grid


def generate_legend(color_dict, font_size, file_name='legend.png'):
    """Creates a legend given a dictionary of colors and names"""

    # Remove base color from legend
    legend_colors = copy.deepcopy(color_dict)
    legend_colors.pop('Base Color')

    # Create list of patches with colors and names
    patch_list = []
    for label, color in sorted(legend_colors.items()):
        # Create patch and add to list
        legend_key = mpatches.Patch(label=label, color=color)
        patch_list.append(legend_key)

    # Plot and save to image
    plt.legend(fontsize=font_size, handles=patch_list)
    plt.axis('off')
    plt.savefig(file_name, bbox_inches='tight')
    plt.close('all')


def append_legend(image, legend_image, title='', include_title=True, title_font='/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf', title_font_size=48, title_location='bottom left', include_legend=True, legend_size=(1000, 1000), legend_location='bottom right'):
    """Adds legend and/or title to an image"""

    # Set constants
    VERTICAL_BUFFER = 10

    # Get dimensions of plot image
    old_image = Image.open(image)
    plot_width, plot_height = old_image.size

    # Resize legend
    legend = Image.open(legend_image)
    legend.thumbnail(legend_size)
    legend_width, legend_height = legend.size

    placement = legend_location.split()
    legend_vertical_placement = placement[0]
    legend_horizontal_placement = placement[1]

    placement = title_location.split()
    title_vertical_placement = placement[0]
    title_horizontal_placement = placement[1]

    # Set coordinates for pasting
    if title_vertical_placement == 'bottom':
        plot_y = 0
        title_y = plot_height
    else:
        plot_y = 100
        title_y = 0

    title_y += VERTICAL_BUFFER

    if title_horizontal_placement == 'left':
        title_x = 50
    else:
        title_x = plot_width - 150

    plot_bottom = plot_y + plot_height

    if legend_vertical_placement == 'bottom':
        legend_y = plot_bottom
    else:
        plot_y = max(legend_height, plot_y)
        legend_y = 0

    if legend_horizontal_placement == 'right':
        legend_x = plot_width - legend_width
    else:
        legend_x = -75

    legend_bottom = legend_y + legend_height

    new_image_height = max(plot_bottom, legend_bottom)

    # Create new blank image
    new_image = Image.new('RGB', (plot_width, new_image_height), (255, 255, 255))

    # Paste in old image
    new_image.paste(old_image, (0, plot_y))
    old_image.close()

    # Paste in legend
    if include_legend:
        new_image.paste(legend, (legend_x, legend_y), legend)
        legend.close()

    # Add title
    if include_title:
        idraw = ImageDraw.Draw(new_image)
        ifont = ImageFont.truetype(title_font, title_font_size)
        idraw.text((title_x, title_y), title, fill=(0, 0, 0), font=ifont)

    # Save new image using old image file name
    new_image.save(image)


def add_border(image, border_color='#000000', border_dimensions=(3, 3)):
    """Adds a border to an image"""

    # Get dimensions of original image
    old_image = Image.open(image)
    old_width, old_height = old_image.size

    # Calculate dimensions of new image
    horizontal_padding = border_dimensions[0]
    vertical_padding = border_dimensions[1]
    new_width = old_width + horizontal_padding*2
    new_height = old_height + vertical_padding*2

    new_image = Image.new('RGB', (new_width, new_height), border_color)
    new_image.paste(old_image, border_dimensions)
    new_image.save(image)


def images_to_pdf(file_list, filename='images.pdf'):
    """
    Converts a list of image files into a single PDF file, with one image per page

    Note: Must have installed fpdf2, not fpdf
    """

    pdf = FPDF(unit='pt')
    for file in file_list:
        # Get image dimensions
        image = Image.open(file)
        dimensions = image.size
        image.close()

        # Create new page in pdf and add image
        pdf.add_page(format=dimensions)
        pdf.image(file, 0, 0)
    pdf.output(filename, 'F')
