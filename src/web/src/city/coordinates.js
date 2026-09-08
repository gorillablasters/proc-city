export function cityToThree(position) {
    const [x, y, z] = position;

    return {
        x: x,
        y: z,
        z: y
    };
}