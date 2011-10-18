
const vec3 stripeColor = vec3(0.7, 0.3, 0.3);
const vec3 backColor   = vec3(0.0, 0.0, 0.0);
const float width = 1.0;
const float fuzz = 2.0;
const float scale = 20.0;

varying vec3 diffuseColor;
varying vec3 specularColor;

void main() {
    float scaledT = fract(gl_TexCoord[0].t * scale);
    float frac1 = clamp(scaledT / fuzz, 0.0, 1.0);
    float frac2 = clamp((scaledT - width) / fuzz, 0.0, 1.0);
    frac1 = frac1 * (1.0 - frac2);
    frac1 = frac1 * frac1 * (3.0 - (2.0 * frac1));
    vec3 finalColor = mix(backColor, stripeColor, frac1);
    finalColor = finalColor * diffuseColor + specularColor;
    gl_FragColor = vec4(finalColor, 1.0);
}

