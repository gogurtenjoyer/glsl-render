# glsl-render
GLSL Shader node for InvokeAI

Not ready for use yet; I just posted it here for version control. Nevertheless,

## Installation
`git clone` this into your `nodes` folder as usual. 
In your InvokeAI venv, `pip install moderngl glcontext`.

## Usage
Choose a vert and frag shader from the dropdown menus. `default` for vert is usually fine.

Shaders are named `vert.glsl` and `frag.glsl`. To make a new one, just make a folder with your shader name, then name your file `frag.glsl` in it. Make sure to have an input like:

```python
in vec2 uv;
```

as the default `vert.glsl` outputs this `vec2 uv` type and name.

If there's a problem with your shader, you'll get an error in the UI and console/terminal. You don't need to restart InvokeAI once you've fixed your shader, as the node will reload it each time you invoke. However, if you add a new shader (folder, etc), then you do need to restart InvokeAI to reload the folders. So, the basic workflow would be to add a new folder with your shader file in it, then start InvokeAI, and if there's any problems, you can edit it 'semi-live' without having to restart InvokeAI. Have fun, and please share what you make!
