
uniform vec3  lightPosition;
uniform vec3  lightColor;
uniform vec3  eyePosition;
uniform vec3  specular;
uniform vec3  ambient;
uniform float kd;

varying vec3 diffuseColor;
varying vec3 specularColor;

void main() {
    vec3 ecPosition = vec3(gl_ModelViewMatrix * gl_Vertex);
    vec3 tnorm = normalize(gl_NormalMatrix * gl_Normal);
    vec3 lightVec = normalize(lightPosition - ecPosition);
    vec3 viewVec = normalize(eyePosition - ecPosition);
    vec3 hvec = normalize(viewVec + lightVec);

    float spec = clamp(dot(hvec, tnorm), 0.0, 1.0);
    spec = pow(spec, 16.0);

    diffuseColor = lightColor * vec3(kd * dot(lightVec, tnorm));
    diffuseColor = clamp(ambient + diffuseColor, 0.0, 1.0);
    specularColor = clamp(lightColor * specular * spec, 0.0, 1.0);

    gl_TexCoord[0] = gl_MultiTexCoord0;
    gl_Position = ftransform();
}

