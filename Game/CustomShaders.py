from ursina import *
from ursina.shaders import basic_lighting_shader
from ursina.prefabs.trail_renderer import TrailRenderer
from ursina.shader import Shader

class CustomShaders:
    """Holds all custom shader definitions."""

    # Pixelation Shader
    pixelation_shader = Shader(
    fragment='''
#version 150

uniform sampler2D tex;
in vec2 window_size;
in vec2 uv;
out vec4 color;


void main() {
    float Pixels = 1600.0;
    float dx = 9.0 * (0.8 / Pixels);
    float dy = 16.0 * (0.8 / Pixels);
    vec2 new_uv = vec2(dx * floor(uv.x / dx), dy * floor(uv.y / dy));
    color = texture(tex, new_uv);
}
''')

    # Empty/Outline Base Shader (Used for Hybrid Dark World)
    empty_shader = Shader(
    vertex='''
#version 130
// Exactly nothing happens in vertex shading.

in vec4 p3d_Vertex;
uniform mat4 p3d_ModelViewProjectionMatrix;

void main()  {
  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
}
''',
    fragment='''
#version 130
uniform sampler2D tex;
uniform sampler2D dtex;
out vec4 color;

void main () {
  vec4 color_base = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2(0, 0), 0);
  vec4 color_1 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2(-1, -1), 0);
  vec4 color_2 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2(-1,  0), 0);
  vec4 color_3 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2(-1,  1), 0);
  vec4 color_4 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2( 0, -1), 0);
  vec4 color_5 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2( 0,  1), 0);
  vec4 color_6 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2( 1, -1), 0);
  vec4 color_7 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2( 1,  0), 0);
  vec4 color_8 = texelFetch(dtex, ivec2(gl_FragCoord.xy) + ivec2( 1,  1), 0);
  color = (abs(color_base - color_1) +
           abs(color_base - color_2) +
           abs(color_base - color_3) +
           abs(color_base - color_4) +
           abs(color_base - color_5) +
           abs(color_base - color_6) +
           abs(color_base - color_7) +
           abs(color_base - color_8)) * vec4(512, 512, 512, 0);
}
'''
    , geometry='')

    # Toon Outline Shader (The original file had this, but didn't seem to use it)
    toon_outline_shader = Shader(
        language=Shader.GLSL,
        vertex='''
            #version 150
            uniform mat4 p3d_ModelViewProjectionMatrix;
            uniform mat4 p3d_ModelMatrix;
            uniform mat4 p3d_ViewMatrix;

            in vec4 vertex;
            in vec3 normal;
            out vec3 world_normal;
            out vec3 world_pos;

            void main() {
                gl_Position = p3d_ModelViewProjectionMatrix * vertex;
                world_pos = (p3d_ModelMatrix * vertex).xyz;
                world_normal = normalize(mat3(p3d_ModelMatrix) * normal);
            }
        ''',
        fragment='''
            #version 150
            uniform vec3 light_dir = normalize(vec3(0.5, 1.0, 0.3));
            uniform vec3 base_color = vec3(1.0, 0.7, 0.5);

            in vec3 world_normal;
            in vec3 world_pos;
            out vec4 fragColor;

            void main() {
                float light_strength = max(dot(normalize(world_normal), normalize(light_dir)), 0.0);

                vec3 toon_color;

                if (light_strength > 0.75)
                    toon_color = base_color * 1.0;
                else if (light_strength > 0.4)
                    toon_color = base_color * 0.7;
                else
                    toon_color = base_color * 0.4;

                fragColor = vec4(toon_color, 1.0);
            }
        '''
    )

    # Outline Pass Shader (The original file had this, but didn't seem to use it)
    outline_pass_shader = Shader(
        language=Shader.GLSL,
        fragment='''
            #version 150
            uniform sampler2D tex;
            uniform vec2 window_size;
            in vec2 uv;
            out vec4 color;

            void main() {
                float dx = 1.0 / window_size.x;
                float dy = 1.0 / window_size.y;

                float center = texture(tex, uv).r;
                float left   = texture(tex, uv - vec2(dx, 0)).r;
                float right  = texture(tex, uv + vec2(dx, 0)).r;
                float up     = texture(tex, uv + vec2(0, dy)).r;
                float down   = texture(tex, uv - vec2(0, dy)).r;

                float diff = abs(center - left) + abs(center - right) + abs(center - up) + abs(center - down);
                float strength = smoothstep(0.05, 0.2, diff);  // Sensitivity

                vec4 outline = vec4(vec3(0.0), strength);
                color = mix(texture(tex, uv), outline, strength);
            }
        '''
    )
    color_grade_shader = Shader(
        # The vertex shader can be standard, just passing texture coordinates
        vertex='''
        #version 130
        in vec4 p3d_Vertex;
        in vec2 p3d_MultiTexCoord0;
        out vec2 uv;
        uniform mat4 p3d_ModelViewProjectionMatrix;

        void main() {
            gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
            uv = p3d_MultiTexCoord0;
        }
        ''',
        # The fragment shader applies the color adjustment
        fragment='''
        #version 130
        uniform sampler2D tex;
        uniform vec4 u_tint; // New uniform to pass the tint color (RGBA)
        in vec2 uv;
        out vec4 color;

        void main() {
            vec4 original_color = texture(tex, uv);

            // 1. Start with original RGB color
            vec3 processed_rgb = original_color.rgb;

            // 2. Apply a warm color tint for mood. u_tint.a controls intensity.
            // Mix original color with the tint color based on intensity (u_tint.a)
            processed_rgb = mix(processed_rgb, u_tint.rgb, u_tint.a);

            // 3. Color Enhancement (Contrast and Pop)
            // Boosting the overall color strength slightly (Saturation/Brightness)
            processed_rgb = processed_rgb * 1.08; 
            // Applying a slight gamma correction (0.9) to increase contrast in midtones
            processed_rgb = pow(processed_rgb, vec3(0.9)); 

            // 4. Final output
            color = vec4(processed_rgb, original_color.a);
        }
        ''',
        default_input={
            # ENHANCED DEFAULT: Warm, slightly golden tint (R=1, G=0.8, B=0.5) with a medium intensity (A=0.3)
            'u_tint': Vec4(0.2, 0.2, 0.2, 0.2)
        }
    
    )
