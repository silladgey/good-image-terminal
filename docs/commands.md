<!-- commands.md -->

# Commands

## `bg`

Sets the background color of the canvas. All subsequent drawing will be rendered on top of this background.

### Usage

```
bg <color>
```

![bg command](_media/showcase/bg.gif)

## `draw_circle`

Draws a circle on the canvas at a specified position with customizable radius, colors, and outline thickness.

### Usage

```
draw_circle <x> <y> <radius> [--fg <color>] [--bg <color>] [--outline <int>] [--no-fill]
```

![draw_circle command](_media/showcase/draw_circle.gif)

## `draw_line`

Draws a straight line between two points. The line color can be customized.

### Usage

```
draw_line <x1> <y1> <x2> <y2> [--fg <color>]
```

![draw_line command](_media/showcase/draw_line.gif)

## `draw_pixel`

Places a single pixel at the specified coordinates. The color can be defined with the foreground option.

### Usage

```
draw_pixel <x> <y> [--fg <color>]
```

![draw_pixel command](_media/showcase/draw_pixel.gif)

## `draw_polygon`

Draws a polygon using the provided vertices, with options for fill, outline, and colors.

### Usage

```
draw_rectangle <x> <y> <width> <height> [--fg <color>] [--bg <color>] [--outline <int>] [--no-fill]
```

![draw_polygon command](_media/showcase/draw_polygon.gif)

## `draw_rectangle`

Draws a rectangle on the canvas at the specified position and dimensions.

### Usage

```
draw_rectangle <x> <y> <width> <height>
```

![draw_rectangle command](_media/showcase/draw_rectangle.gif)

## `fg`

Sets the foreground color for use in drawing commands.

### Usage

```
fg <color>
```

![fg command](_media/showcase/fg.gif)

## `help`

Displays information about available commands. When a specific command is given, it shows detailed usage instructions.

### Usage

```
help [command] [page]
```

## `image_info`

Displays details about the currently loaded image, such as dimensions and format.

### Usage

```
image_info
```

## `load_image`

Loads an image file into the canvas for editing or manipulation.

### Usage

```
load_image <filename>
```

## `ls`

Lists available files in the current working directory.

### Usage

```
ls
```

## `ping`

Pong!

### Usage

```
ping
```

## `save_image`

Saves the current canvas to an image file with the specified name.

### Usage

```
save_image <filename>
```

## `terminal_background`

Changes the background color of the terminal (not the canvas).

### Usage

```
terminal_background <color>
```

## `undo`

Reverts the most recent drawing action on the canvas.

### Usage

```
undo
```
