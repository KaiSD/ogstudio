
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
    vec3 lightV = gl_LightSource[0].position.xyz - eyeDir;
    v.x = dot(lightV, t);
    v.y = dot(lightV, b);
    v.z = dot(lightV, n);
    lightDir = normalize(v);
    v.x = dot(eyeDir, t);
    v.y = dot(eyeDir, b);
    v.z = dot(eyeDir, n);
    eyeDir = normalize(v);
}

