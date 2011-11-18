
const float specularFactor = 0.5;
uniform sampler2D colorMap;
uniform sampler2D normalMap;
varying vec3 lightDir;
varying vec3 eyeDir;

void main() {
    vec4 surfaceColor = texture2D(colorMap, gl_TexCoord[0].st);
    vec3 normDelta = texture2D(normalMap, gl_TexCoord[0].st).rgb * 2.0 - 1.0;
    vec4 litColor = surfaceColor * max(dot(normDelta, lightDir), 0.0);
    vec3 reflectDir = reflect(lightDir, normDelta);
    float spec = max(dot(eyeDir, reflectDir), 0.0);
    spec = pow(spec, 6.0);
    spec *= specularFactor;
    litColor = min(litColor + spec, vec4(1.0));
    gl_FragColor = litColor;
}

