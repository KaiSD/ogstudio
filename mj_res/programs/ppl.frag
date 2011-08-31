// Per-pixel lighting for spot lights.
varying vec4 diffuse, ambient, ambientGlobal;
varying vec3 normal, lightDir, halfVector;
varying float dist;
uniform sampler2D tex;

void main()
{
    vec3 n, halfV;
    float NdotL, NdotHV;
    vec4 color = ambientGlobal;
    vec4 texel;
    float att, spotEffect;
    n = normalize(normal);
    NdotL = max(dot(n, lightDir), 0.0);
    if (NdotL > 0.0) {
        spotEffect = dot(normalize(gl_LightSource[0].spotDirection), normalize(-lightDir));
        if (spotEffect > gl_LightSource[0].spotCosCutoff) {
            spotEffect = pow(spotEffect, gl_LightSource[0].spotExponent);
            att = spotEffect / (gl_LightSource[0].constantAttenuation +
                                gl_LightSource[0].linearAttenuation * dist +
                                gl_LightSource[0].quadraticAttenuation * dist * dist);
            color += att * (diffuse * NdotL + ambient);
            halfV = normalize(halfVector);
            NdotHV = max(dot(n, halfV), 0.0);
            color += att *
                     gl_FrontMaterial.specular *
                     gl_LightSource[0].specular *
                     pow(NdotHV, gl_FrontMaterial.shininess);
        }
    }
    texel = texture2D(tex, gl_TexCoord[0].st);
	gl_FragColor = color * texel;
}

