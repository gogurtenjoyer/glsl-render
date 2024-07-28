#version 330

uniform sampler2D texture0;      // the input texture (image)
in vec2 uv;                      // the position/shape of the quad (basically, 2d flat image from the vert shader)
out vec4 fragColor;              // the output changed image pixel colors

// some simple functions to adjust brightness, contrast, and saturation

vec3 adjustBrightness(vec3 color, float brightness) {
  return color + brightness;
}

vec3 adjustContrast(vec3 color, float contrast) {
  return 0.5 + (contrast + 1.0) * (color.rgb - 0.5);
}

vec3 adjustSaturation(vec3 color, float saturation) {
  // WCAG 2.1 relative luminance base
  const vec3 luminanceWeighting = vec3(0.2126, 0.7152, 0.0722);
  vec3 grayscaleColor = vec3(dot(color, luminanceWeighting));
  return mix(grayscaleColor, color, 1.0 + saturation);
}

vec3 addGrain(vec3 color, float amount) {
    float grain = (fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453) - 0.5) * 2.0;
    return(color + (grain * amount));
}

// then, in main, we call those functions
// you could use any of these as the start of a new shader if needed

void main() {
  vec3 color = texture(texture0, uv).rgb;
  color = adjustBrightness(color, 0.2);
  color = adjustSaturation(color, -0.2);
  color = adjustContrast(color, 0.2);
  color = addGrain(color, 0.1);
  color = clamp(color, 0.0, 1.0);        // clamp to valid range
    
  fragColor = vec4(color, 1.0);         // fragColor is the 'out', and we add full 1.0 alpha to it
}