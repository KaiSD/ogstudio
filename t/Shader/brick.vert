
const   float specContrib = 0.3;
const   float difContrib  = 1.0 - specContrib;
uniform vec3  lightPosition;
varying float lightIntensity;

void main() {
    vec3 ecPosition = vec3(gl_ModelViewMatrix * gl_Vertex);
    vec3 tnorm = normalize(gl_NormalMatrix * gl_Normal);
    vec3 lightVec = normalize(lightPosition - ecPosition);
    vec3 reflectVec = reflect(-lightVec, tnorm);
    vec3 viewVec = normalize(-ecPosition);

    float diffuse = max(dot(lightVec, tnorm), 0.0);
    float spec = 0.0;
    if (diffuse > 0.0) {
        spec = max(dot(reflectVec, viewVec), 0.0);
        spec = pow(spec, 16.0);
    }
    lightIntensity = difContrib * diffuse + specContrib * spec;
    gl_TexCoord[0] = gl_MultiTexCoord0;
    gl_Position = ftransform();
}

