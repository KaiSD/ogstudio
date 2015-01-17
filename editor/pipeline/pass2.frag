
uniform mat4 osg_ViewMatrixInverse;
uniform vec3 lightPos;
uniform sampler2DRect positionMap;
uniform sampler2DRect colorMap;
uniform sampler2DRect normalMap;
uniform sampler2DRect glowMap;
uniform sampler2DRect shadowMap;

vec3 glowBlur(sampler2DRect glowMap,
              vec2          xy,
              int           blurSamples,
              vec2          blurSizeFactor)
{
    vec3 glow = texture2DRect(glowMap, xy).xyz;
    vec3 result = vec3(0);
    int blurRange = (blurSamples - 1) / 2;
    for (int x = -blurRange; x < blurRange; ++x)
        for (int y = -blurRange; y < blurRange; ++y)
        {
            vec2 offset = vec2(x, y) * blurSizeFactor;
            result += texture2DRect(glowMap, xy + offset).xyz;
        }
    return (result / float(blurSamples * blurSamples)) + glow;
}

void main()
{
    vec3 p_worldspace = texture2DRect(positionMap, gl_FragCoord.xy).xyz;
    vec3 c_worldspace = texture2DRect(colorMap,    gl_FragCoord.xy).xyz;
    vec3 n_worldspace = texture2DRect(normalMap,   gl_FragCoord.xy).xyz;
    vec3 s_worldspace = texture2DRect(shadowMap,   gl_FragCoord.xy).xyz;
    vec3 g_worldspace = glowBlur(glowMap, gl_FragCoord.xy, 10, vec2(3, 3));
    // Direction from point to light (not vice versa!)
    vec3 lightDir_worldspace = normalize(lightPos - p_worldspace);
    // Lambertian diffuse color.
    float diff = max(0.2, dot(lightDir_worldspace, n_worldspace));
    // Convert camera position from Camera (eye) space (it's always at 0, 0, 0
    // in there) to World space. Don't forget to use mat4 and vec4!
    vec4 cameraPos_worldspace = osg_ViewMatrixInverse * vec4(0, 0, 0, 1);
    // Direction from point to camera.
    vec3 viewDir_worldspace = normalize(vec3(cameraPos_worldspace) - p_worldspace);
    // Blinn-Phong specular highlights.
    vec3 h_worldspace = normalize(lightDir_worldspace + viewDir_worldspace);
    float spec = pow(max(0.0, dot(h_worldspace, n_worldspace)), 40.0);
    // Final fragment color.
    vec3 color = diff * c_worldspace * s_worldspace;
    // Only add specular if the fragment is NOT in the shadow.
    if (s_worldspace.x == 1.0)
        color += spec;
    // Add glow.
    color += g_worldspace;
    gl_FragColor = vec4(color, 1.0);
}
