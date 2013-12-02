
// Execution path controls.
uniform int useBumpMap;
uniform int useCubeMap;
uniform int useGlowMap;
uniform int crawlDiffMap;
uniform int crawlBumpMap;

uniform sampler2D diffMap;
uniform sampler2D bumpMap;
uniform sampler2D glowMap;
const int GLOW_ID = 3;
uniform samplerCube cubeMap;
uniform sampler2D   cubeMapMask;
const int CUBE_ID = 4;
uniform float osg_FrameTime;

varying vec3 pos_worldspace;
varying vec3 n_worldspace;
varying vec3 t_worldspace;
varying vec3 b_worldspace;
// For cube mapping.
varying vec3 cubeMapNormal;
varying vec3 cubeMapEye;

void main()
{
    float factor = osg_FrameTime;
    gl_FragData[0] = vec4(pos_worldspace, gl_FragCoord.z);
    vec3 nn = vec3(1.0);
    if (useBumpMap > 0)
    {
        // Convert [0; 1] range to [-1; 1].
        if (crawlBumpMap == 0)
            nn = 2.0 * texture2D(bumpMap, gl_TexCoord[0].xy).xyz - vec3(1.0);
        else
        {
            vec2 uv = vec2(0.4 * sin(factor), 0.4 * cos(factor));
            nn = 2.0 * texture2D(bumpMap, gl_TexCoord[0].xy + uv).xyz - vec3(1.0);
        }
    }
    // Convert Tangent space to World space with TBN matrix.
    gl_FragData[1] = vec4(nn.x * t_worldspace + nn.y * b_worldspace + nn.z * n_worldspace, 1.0);
    if (crawlDiffMap == 0)
        gl_FragData[2] = texture2D(diffMap, gl_TexCoord[0].xy);
    else
    {
        vec2 uv = vec2(0.4 * sin(factor), 0.4 * cos(factor));
        gl_FragData[2] = texture2D(diffMap, gl_TexCoord[0].xy + uv);
    }
    // Glow.
    if (useGlowMap == 0)
        gl_FragData[GLOW_ID] = vec4(0, 0, 0, 0);
    else
        gl_FragData[GLOW_ID] = texture2D(glowMap, gl_TexCoord[0].xy);
    if (useCubeMap == 0)
        gl_FragData[CUBE_ID] = vec4(1, 1, 1, 1);
    else
    {
        vec3 reflectedDirection = reflect(cubeMapEye, cubeMapNormal);
        reflectedDirection.z = -reflectedDirection.z;
        vec4 cubeMapColor = textureCube(cubeMap, reflectedDirection.xzy);
        vec4 cubeMapMaskColor = texture2D(cubeMapMask, gl_TexCoord[0].xy);
        gl_FragData[CUBE_ID] = cubeMapColor * cubeMapMaskColor;
    }
}

