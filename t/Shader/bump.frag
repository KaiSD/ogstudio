
const vec3 surfaceColor    = vec3(0.7, 0.6, 0.18);
const float bumpDensity    = 16.0;
const float bumpSize       = 0.15;
const float specularFactor = 0.5;

varying vec3 lightDir;
varying vec3 eyeDir;

void main() {
    vec3 litColor;
    vec2 c = bumpDensity * gl_TexCoord[0].st;
    vec2 p = fract(c) - vec2(0.5);
    float d, f;
    d = p.x * p.x + p.y * p.y;
    f = 1.0 / sqrt(d + 1.0);
    if (d >= bumpSize) {
        p = vec2(0, 0);
        f = 1.0;
    }
    vec3 normDelta = vec3(p.x, p.y, 1.0) * f;
    litColor = surfaceColor * max(dot(normDelta, lightDir), 0.0);
    vec3 reflectDir = reflect(lightDir, normDelta);
    float spec = max(dot(eyeDir, reflectDir), 0.0);
    spec = pow(spec, 6.0);
    spec *= specularFactor;
    litColor = min(litColor + spec, vec3(1.0));
    gl_FragColor = vec4(litColor, 1.0);
}

