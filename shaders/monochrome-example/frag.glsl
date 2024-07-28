#version 330

uniform sampler2D texture0;
in vec2 uv;
out vec4 fragColor;

void main() {
    vec3 color = texture(texture0, uv).rgb;
    float v = (color[0] + color[1] + color[2])/3.0; // average all colors
    fragColor = vec4(v, v, v, 1.0); // all channels same
}