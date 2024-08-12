#version 330

// this shader makes use of the input image size, and so
// we use texture_size which is optionally passed from the node

uniform sampler2D texture0;   // image
uniform vec2 texture_size;    // image size (optional, use it if you need it)
in vec2 uv;                   // position/mapping of pixels
out vec4 fragColor;           // output (you can name this whatever, just make sure to use in your main)

void main() {
    vec3 color = texture(texture0, uv).rgb;

    // Flattened Bayer matrix for dithering
    float bayer[16] = float[](
         0.0,  8.0,  2.0, 10.0,
        12.0,  4.0, 14.0,  6.0,
         3.0, 11.0,  1.0,  9.0,
        15.0,  7.0, 13.0,  5.0
    );

    // Get the pixel coordinates
    vec2 pixelCoord = uv * texture_size; // here's where we use texture_size
    int x = int(mod(pixelCoord.x, 4.0));
    int y = int(mod(pixelCoord.y, 4.0));
    
    // Calculate the index for the flattened Bayer matrix
    int index = y * 4 + x;
    float threshold = bayer[index] / 16.0;

    // Apply dithering effect
    color = step(vec3(threshold), color);
    fragColor = vec4(color, 1.0);
}
