import os
import pathlib
from PIL import Image
import moderngl
import numpy as np
from typing import Literal, Optional

from invokeai.app.invocations.primitives import ImageField, ImageOutput
from invokeai.backend.util.devices import TorchDevice
from invokeai.invocation_api import BaseInvocation, Input, InputField, InvocationContext, WithMetadata, WithBoard, invocation



SHADERS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shaders")

def getDirs(filename: str):
    dirs = []
    all_entries = os.listdir(SHADERS_PATH)
    for e in all_entries:
        entry_path = os.path.join(SHADERS_PATH, e)
        if os.path.isdir(entry_path):
            if filename in os.listdir(entry_path):
                dirs.append(e)
    return dirs


VERT_PATHS = Literal[tuple(getDirs('vert.glsl'))]
FRAG_PATHS = Literal[tuple(getDirs('frag.glsl'))]


@invocation(
    "glsl-render",
    title="GLSL Shader",
    tags=["glsl", "shader", "opengl"],
    category="image",
    version="1.1.0",
)
class GLSLShader(BaseInvocation, WithMetadata, WithBoard):
    """Applies a GLSL shader to an image"""

    image: ImageField = InputField(description="The image to apply shader to")
    vertex_shader: VERT_PATHS =      InputField(default='default', input=Input.Direct)
    fragment_shader: FRAG_PATHS = InputField(default='default', input=Input.Direct)



    def invoke(self, context: InvocationContext) -> ImageOutput:
        full_vert = os.path.join(SHADERS_PATH, f"{self.vertex_shader}/vert.glsl")
        full_frag = os.path.join(SHADERS_PATH, f"{self.fragment_shader}/frag.glsl")

        ctx = moderngl.create_standalone_context()
        #ctx.gc_mode = 'auto'

        pil_image = context.images.get_pil(self.image.image_name)

        image_data = np.array(pil_image).astype('f4') / 255.0

        texture = ctx.texture(pil_image.size, 3, data=image_data.tobytes(), dtype='f4')
        texture.use()

        fbo = ctx.framebuffer(color_attachments=[ctx.texture(pil_image.size, 3, dtype='f4')])
        fbo.use()

        program = ctx.program(
            vertex_shader=open(full_vert).read(),
            fragment_shader=open(full_frag).read(),
        )

        vertices = np.array([
            -1.0,  1.0, 0.0, 1.0,
            -1.0, -1.0, 0.0, 0.0,
             1.0, -1.0, 1.0, 0.0,
            -1.0,  1.0, 0.0, 1.0,
             1.0, -1.0, 1.0, 0.0,
             1.0,  1.0, 1.0, 1.0,
        ], dtype='f4')

        vbo = ctx.buffer(vertices)
        vao = ctx.simple_vertex_array(program, vbo, 'in_vert', 'in_uv')
        
        vao.render()

        data = fbo.read(components=3, dtype='f4')
        data = np.frombuffer(data, dtype=np.float32).reshape((*pil_image.size, 3))
        data = (data * 255).astype(np.uint8)

        img_out = Image.frombytes('RGB', pil_image.size, data)

        image_dto = context.images.save(image=img_out)

        return ImageOutput.build(image_dto)