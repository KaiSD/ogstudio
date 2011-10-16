
uniform vec3 brickColor;
uniform vec3 mortarColor;
varying vec2 mcPosition;
varying float lightIntensity;

void main() {
    vec3 color;
    vec2 position;
    vec2 useBrick;
    vec2 brickPct = vec2(0.95, 0.9);
    vec2 brickSize = vec2(1, 0.5);
    /*
    brickColor = vec3(0.7, 0.3, 0.3);
    mortarColor = vec3(0.7, 0.7, 0.7);
    */
    position = mcPosition / brickSize;
    if (fract(position.y * 0.5) > 0.5) 
        position.x += 0.5;
    position = fract(position);
    useBrick = step(position, brickPct);

    color = mix(mortarColor, brickColor, useBrick.x * useBrick.y);
    color *= lightIntensity;
    gl_FragColor = vec4(color, 1.0);
    //gl_FragColor = vec4(brickColor, 1.0);
}

