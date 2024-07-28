#version 330

uniform sampler2D texture0;
in vec2 uv;
out vec4 fragColor;

void main() {
    vec3 color = texture(texture0, uv).rgb;
    // Apply any adjustments to the color here, for example:
    color = vec3(1.0) - color;  // Invert colors
    fragColor = vec4(color, 1.0);
}