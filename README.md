# PLANG
PLANG is a python library written on top of the brand new C based SDL3 library. Pre-made widgets with a lot of customization make development easier.
> plang stands for Python Library For Apps & Games
----------
# Features
## Low level access via High level API
SDL3 is an excellent low level library to access all aspects of your system. PLANG uses this to the full capacity by implementing a higher level (class based) API on top of it. A clear documentation helps you understand what's going on under the hood and how to implement each feature.

## RenderQueue
PLANG handles the rendering for you, you just need to define where and when you want your shape to be drawn. The RenderQueue optimizes the rendering process to the best of it's ability.

## Widgets
PLANG comes packed with widgets. Widgets are separated in 2 categories: basic widgets and extended widgets.
### Basic widgets
- Button
    - creates a simple buttons
 
- Text
    - displays text on the screen

- TextField
    - creates a text input field where the user can input text

- Slider
    - a linear slider that can be used to select a value

### Extended widgets
- Radio button
    - a radio button that can be connected with other radio buttons

## Z-index
PLANG gives you the ability to set a z-index for each shape or widget. This allows shapes/widgets to be always on top. Using it to the full extend can also improve the speed of the rendering process (
[learn more](#using-z-index) )

----------

# Structure
The structure of PLANG is as follows:<br>
1. initialize windows
2. initialize shapes and widgets
3. main loop (while True loop)
This structure gives full control over each frame of the app/game.
Defining where to draw, when to change a shape/widget and handling inputs and interactions with shapes/widgets is up to you. PLANG will handle the events, rendering and optimization while you focus on the logic of your app/game.


----------

# Optimization
## Using Z-index
Each layer is cached after it has been rendered. This means that when nothing changes on that layer, the layer doesn't have to be recalculated. Static widgets (for example background components) can be grouped with the same z-index to improve rendering speed.

## Group the use of textures
For each texture that is used in a chronological order, a new call has to be made to SDL_RenderGeometry. When doing this a lot of times each frame, the Python to C interface can bottleneck. This can be solved by grouping the shapes that use the same texture together. For reference, making hundreds of calls to SDL_RenderGeometry each frame can really slow down the program, so be mindful of this.


----------

# Important classes
## Window


----------

# Used libraries
- CFFI
    - used to communicate with the SDL3.dll in Python
- Numpy
    - used for vector and matrix operations
- Colorama
    - brings universal color to the terminal
- Typing extensions
    - used to create custom types for better clarity
----------

# Code examples
## Showing a rectangle on the screen

```python
import plang as pl

window = pl.Window(800, 600)

while True:
    window.event_handler()


```
