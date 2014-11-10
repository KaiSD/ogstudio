
// Position map.
const   int       POSITION_MAP_ID = 0;
// Diffuse map.
uniform sampler2D diffuseMap;
const   int       DIFFUSE_MAP_ID  = 1;
// Normal map.
uniform sampler2D normalMap;
const   int       NORMAL_MAP_ID   = 2;
uniform int       useNormalMap;
// Glow map.
uniform sampler2D glowMap;
const   int       GLOW_MAP_ID     = 3;
uniform int       useGlowMap;

varying vec3 pos_worldspace;
varying vec3 n_worldspace;
varying vec3 t_worldspace;
varying vec3 b_worldspace;

void main()
{
    gl_FragData[POSITION_MAP_ID] = vec4(pos_worldspace, gl_FragCoord.z);
    vec2 texCoord = gl_TexCoord[0].xy;
    gl_FragData[DIFFUSE_MAP_ID] = texture2D(diffuseMap, texCoord);
    vec3 nn = vec3(1.0);
    if (useNormalMap > 0)
        // Convert [0; 1] range to [-1; 1].
        nn = 2.0 * texture2D(normalMap, texCoord).xyz - vec3(1.0);
    // Convert Tangent space to World space with TBN matrix.
    gl_FragData[NORMAL_MAP_ID] = vec4(nn.x * t_worldspace +
                                      nn.y * b_worldspace +
                                      nn.z * n_worldspace,
                                      1.0);
    if (useGlowMap == 0)
        gl_FragData[GLOW_MAP_ID] = vec4(0, 0, 0, 0);
    else
        gl_FragData[GLOW_MAP_ID] = texture2D(glowMap, texCoord);
}

