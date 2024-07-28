#version 330

uniform sampler2D Texture; // image
in vec2 v_text;            // res
out vec4 f_color;

vec3 rgb2hsb(vec3 c) {
  vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
  vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
  vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
  float d = q.x - min(q.w, q.y);
  float e = 1.0e-10;
  return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}


vec3 hsb2rgb(vec3 c){
  vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
  vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
  return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

float rand(vec2 co){
  return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 43758.5453);
}


vec4 grain(vec4 fragColor, vec2 uv){
  vec4 color = fragColor;
  float diff = (rand(uv) - 0.0) * 0.1;
  color.r += diff;
  color.g += diff;
  color.b += diff;
  return color;
}

void main() {

    vec4 texel = texture(Texture, v_text);
    f_color = texel;

    vec4 grain = grain(f_color, v_text);

    f_color = mix(f_color, grain, 1.0);
}
