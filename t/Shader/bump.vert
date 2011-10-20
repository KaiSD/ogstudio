
const vec3 lightPosition = vec3(0, 50, 50);
attribute vec3 tangent;
varying vec3 lightDir;
varying vec3 eyeDir;

void main() {
    eyeDir = vec3(gl_ModelViewMatrix * gl_Vertex);
    gl_Position = ftransform();
    gl_TexCoord[0] = gl_MultiTexCoord0;
    vec3 n = normalize(gl_NormalMatrix * gl_Normal);
    vec3 t = normalize(gl_NormalMatrix * tangent);
    vec3 b = cross(n, t);
    vec3 v;
    v.x = dot(lightPosition, t);
    v.y = dot(lightPosition, b);
    v.z = dot(lightPosition, n);
    lightDir = normalize(v);
    v.x = dot(eyeDir, t);
    v.y = dot(eyeDir, b);
    v.z = dot(eyeDir, n);
    eyeDir = normalize(v);
}

