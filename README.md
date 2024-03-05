# Color Quiver

This is a package that provides a new way to visualize two dimensional vector field, using hue to indicate the direction of each vector, and saturation (or value, or both) to indicate the modulus.

This type of chart can visualize the one-to-one correspondence between two-dimensional vectors and colors, visualizing two-dimensional vector fields continuously, quantitatively, and with high preservation of original data in the form of planar legends. It has low computational complexity and high efficiency when generating legends, making it suitable for dynamic display.

![Figure_1](https://raw.githubusercontent.com/IcEarthlight/ColorQuiver/master/Images/Figure_1.png "The figure of the demonstration code")

Map all vectors in a two-dimensional vector field to a circular (or fan-shaped, circular, fan-shaped, etc.) scale table, so that each color represents the vector from the center to the position of that color in the scale table. Clarify the direction of the hue and two-dimensional vector in the legend, and the correspondence between brightness, brightness, or saturation and the size of the two-dimensional vector. After visualizing the two-dimensional vector field, the size and direction of each vector are quantified, thereby improving the information content and density conveyed by the legend without losing its intuitiveness.

![water_flow_field](https://raw.githubusercontent.com/IcEarthlight/ColorQuiver/master/Images/water_flow_field.png "Water Flow Field around a Cylinder")

Based on the characteristic that the visualized chart does not express directionality in the form of graphical trends, while not losing its readability, it can be overlaid with other charts or different visualization scheme legends of the same two-dimensional vector field. For different data analysis scenarios, it forms the advantage of complementing the advantages of multiple visualization schemes and emphasizing the correspondence between the two-dimensional vector field and other information (such as geographical location) for easy data analysis.

![global_windfield_map](https://raw.githubusercontent.com/IcEarthlight/ColorQuiver/master/Images/global_windfield_map.png "Golbal Windfield Map")

![electric_field_diagram_between_electrostatic_charges](https://raw.githubusercontent.com/IcEarthlight/ColorQuiver/master/Images/electric_field_diagram_between_electrostatic_charges.png "Electric Field Diagram Between Electrostatic Charges")

## Requirements

- Python 3.6 or higher
- [Numpy](https://pypi.python.org/pypi/numpy)
- [Matplotlib](https://pypi.org/project/matplotlib)
