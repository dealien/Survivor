mapgen: The Groundwork
**********************

``mapgen`` is key to Survivor. It is responsible for generating the terrain and creating the map. Without it, Survivor simply could not exist.

================
\_\_init\_\_.py
================

.. py:function:: generate_terrain(width, height, smoothness, values)

    Generates and returns a new procedurally-generated terrain

    Generates and returns a two-dimensional list with the passed
    values spread throughout in a terrain-like fashion.

    :param width: The width of the terrain to generate.
    :param height: The height of the terrain to generate.
    :param smoothness: The number of times to run the smoothing
            algorithm on the terrain. Used when calling :func:`_smooth()`.
    :param values: A dictionary containing the values to spread
            throughout the terrain paired to their relative
            probabilities of appearing. For example:
            ``{"X": 0.2442, "#": 0.2558, ".": 0.2442, " ": 0.2558}``
            In this example, ``"X"`` and ``"."`` are slightly less likely
            to appear than ``"#"`` or ``" "``.
    :raises ValueError: Mapgen terrains must be at least 3x3
            (Attempted: (dimensions attempted)).



.. py:function:: _create_blank(width, height)

    Returns a 2D list filled with ``None`` elements.

    Creates and returns a list of lists of the given dimensions
    filled with ``None`` elements.

    :param width: The width of the blank terrain to generate.
    :param height: The height of the blank terrain to generate.



.. py:function:: _create_noise(terrain, values)

    Fills the given terrain with noise made with the given values.

    :param terrain: The terrain to fill with noise.
    :param values: The values to create noise with.



.. py:function:: _choose_value(values)

    Chooses a value from the given values.

    This takes into account the respective probabilities
    of each value.

    :param values: The dictionary from which to choose a value.
            For example: ``{"X": 1, "#": 2}``
    :returns: A weighted, but randomly chosen value from the given
        dictionary.



.. py:function:: _smooth(terrain, values)

    Smooths the terrain.

    Iterates over the terrain by choosing random indices
    and setting said indices to the majority neighbor value.

    :param terrain: The terrain to smooth.
    :param values: The values of the terrain. These are used to simplify computation in :func:`_determine_value()`.
    :returns: A more smoothly-bordered terrain (less noisy).



.. py:function:: _generate_indices_list(terrain)

    Returns a unordered list of valid coordinates for given terrain.

    :param terrain: The terrain to find coordinates for.
    :returns: A scrambled list of indices



.. py:function:: _get_neighbors(terrain, pos)

    Returns a list of a given element's neighbor values.

    :param terrain: The terrain to look for neighbors in.
    :param pos: The position of the element to find neighbors for.



.. py:function:: _determine_value(neighbors, values)

    Returns the value to set an element to based on its neighbors.

    :param neighbors: The neighbors of the element in question.
    :param values: The values of the terrain. This is passed in so that
            a new dictionary doesn't have to be created and added to.



.. py:function:: display_terrain(terrain)

    Prints an ASCII representation of a given terrain to the console.

    :param terrain: The terrain to display to the console.



.. py:function:: generate_tilemap(terrain, key)

    Generates a 2D array of objects containing specific
    information for each tile on the map. The function uses a key to
    determine what symbols in the terrain map correspond with what
    tiles.

    :param terrain: The terrain to convert into a tilemap.
    :param key: An object list showing the symbols in the terrain
        map and their corresponding tiles.
    :returns: The completed tilemap.

=========
mapgen.py
=========

.. py:class:: Map(height, width, smoothness)

    Stores information about the map, including terrain,
    tilemap, and the arguments used to generate the map.

    Uses :func:`generate_terrain()` to generate terrain and
    :func:`generate_tilemap()` to generate the tilemap.

    :param height: Height of map to generate
    :param width: Width of map to generate
    :param smoothness: Number of times the terrain should be smoothed



.. py:class:: Tile(material, image, x, y)

    Holds information about a specific tile on the map.

    :param material: The name of the material
    :param image: The name of the image to be used when rendering the tile
    :param x: The x position on the map
    :param y: The y position on the map
