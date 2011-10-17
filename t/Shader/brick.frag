
uniform sampler2D tex;
varying float lightIntensity;

void main() {
    vec3 lightColor = vec3(texture2D(tex, gl_TexCoord[0].st));
    gl_FragColor = vec4(lightColor * lightIntensity, 1.0);
}

