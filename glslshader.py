import os
import pathlib
from PIL import Image
import moderngl
import numpy as np
from typing import Literal, Optional

from invokeai.app.invocations.primitives import ImageField, ImageOutput
from invokeai.backend.util.devices import TorchDevice
from invokeai.invocation_api import BaseInvocation, InputField, InvocationContext, WithMetadata, WithBoard, invocation

VERT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shaders/invert-example/vert.glsl")
FRAG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shaders/simple-postprocess-example/frag.glsl")

@invocation(
    "glsl-render",
    title="GLSL Shader",
    tags=["glsl", "shader", "opengl"],
    category="image",
    version="1.0.0",
)
class GLSLShader(BaseInvocation, WithMetadata, WithBoard):
    """Applies a GLSL shader to an image"""

    image: ImageField = InputField(description="The image to apply shader to")



    def invoke(self, context: InvocationContext) -> ImageOutput:
        ctx = moderngl.create_standalone_context()
        #ctx.gc_mode = 'auto'

        pil_image = context.images.get_pil(self.image.image_name)

        image_data = np.array(pil_image).astype('f4') / 255.0

        texture = ctx.texture(pil_image.size, 3, data=image_data.tobytes(), dtype='f4')
        texture.use()

        fbo = ctx.framebuffer(color_attachments=[ctx.texture(pil_image.size, 3, dtype='f4')])
        fbo.use()

        program = ctx.program(
            vertex_shader=open(VERT_PATH).read(),
            fragment_shader=open(FRAG_PATH).read(),
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