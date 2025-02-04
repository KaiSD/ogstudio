
// Execution path controls.
uniform int useCubeMap;
uniform int useHeightMap;

uniform mat4 osg_ViewMatrix;
uniform mat4 osg_ViewMatrixInverse;

varying vec3 pos_worldspace;
varying vec3 n_worldspace;
varying vec3 t_worldspace;
varying vec3 b_worldspace;
// For cube mapping.
varying vec3 cubeMapNormal;
varying vec3 cubeMapEye;
// For height mapping.
varying vec3 viewDir_tangentspace;

attribute vec3 Tangent;

void main()
{
    // Model space * Model matrix = World space
    // World space * View matrix = Camera (eye) space
    // Camera (eye) space * Projection matrix = Screen space
    // We simply translate vertex from Model space to Screen space.
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    // Pass the texture coordinate further to the fragment shader.
    gl_TexCoord[0] = gl_MultiTexCoord0;
    // gl_ModelViewMatrix, gl_NormalMatrix, etc. are in Camera(eye) space
    // Discussion: http://forum.openscenegraph.org/viewtopic.php?p=44257#44257
    // Camera (eye) space * inverse View matrix = World space
    mat4 modelMatrix = osg_ViewMatrixInverse * gl_ModelViewMatrix;
    mat3 modelMatrix3x3 = mat3(modelMatrix);
    // Convert everything to World space.
    // Position.
    pos_worldspace = modelMatrix * gl_Vertex;
    // Normal.
    n_worldspace   = modelMatrix3x3 * gl_Normal;
    // Tangent.
    t_worldspace   = modelMatrix3x3 * Tangent;
    // Bitangent / binormal.
    b_worldspace   = cross(n_worldspace, t_worldspace);
    if (useCubeMap > 0)
    {
        cubeMapNormal = gl_NormalMatrix * gl_Normal;
        cubeMapEye    = vec3(gl_ModelViewMatrix * gl_Vertex);
    }
    if (useHeightMap > 0)
    {
        // View direction = Camera position - vertex position.
        // Since Camera is always at (0, 0, 0) in Camera (eye) space,
        // we simply get -vertex position.
        vec3 viewDir_cameraspace = -vec3(gl_ModelViewMatrix * gl_Vertex);
        viewDir_cameraspace = normalize(viewDir_cameraspace);
        vec3 n_cameraspace = normalize(gl_NormalMatrix * gl_Normal);
        vec3 t_cameraspace = normalize(gl_NormalMatrix * Tangent);
        vec3 b_cameraspace = cross(n_cameraspace, t_cameraspace);
        // Convert view direction from Camera (eye) space to Tangent one
        // using the inverse of TBN matrix.
        viewDir_tangentspace.x = dot(viewDir_cameraspace, t_cameraspace);
        viewDir_tangentspace.y = dot(viewDir_cameraspace, b_cameraspace);
        viewDir_tangentspace.z = dot(viewDir_cameraspace, n_cameraspace);
    }
}

