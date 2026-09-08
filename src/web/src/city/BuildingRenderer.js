import * as THREE from "three";
import { cityToThree } from "./coordinates.js";


export class BuildingRenderer {

    constructor(scene) {
        this.scene = scene;
        this.buildings = new Map();
    }


    create(building) {

        if (this.buildings.has(building.id)) {
            return this.buildings.get(building.id);
        }

        const group = new THREE.Group();

        group.name = `building-${building.id}`;


        const height = this.getHeight(building);


        // -----------------------------
        // Building body
        // -----------------------------

        const bodyGeometry =
            new THREE.BoxGeometry(
                6,
                height,
                6
            );


        const bodyMaterial =
            new THREE.MeshStandardMaterial({
                color: this.getColor(building),
                roughness: 0.75,
                metalness: 0.15
            });


        const body =
            new THREE.Mesh(
                bodyGeometry,
                bodyMaterial
            );


        body.position.y =
            height / 2;


        group.add(body);


        // -----------------------------
        // Windows
        // -----------------------------

        this.createWindows(
            group,
            building,
            height
        );


        // -----------------------------
        // Position
        // -----------------------------

        const position =
            cityToThree(
                building.position
            );


        group.position.set(
            position.x,
            position.y,
            position.z
        );


        this.scene.add(group);

        this.buildings.set(
            building.id,
            group
        );


        return group;
    }


    createWindows(
        group,
        building,
        height
    ) {

        const rows =
            Math.max(
                2,
                Math.floor(height / 4)
            );


        const columns = 3;


        const windowGeometry =
            new THREE.BoxGeometry(
                0.7,
                1.0,
                0.12
            );


        const windowMaterial =
            new THREE.MeshStandardMaterial({

                color: 0xbfd8ff,

                emissive: 0x26364d,

                emissiveIntensity: 0.5
            });


        for (
            let row = 0;
            row < rows;
            row++
        ) {

            for (
                let column = 0;
                column < columns;
                column++
            ) {

                const window =
                    new THREE.Mesh(
                        windowGeometry,
                        windowMaterial
                    );


                const x =
                    (column - 1) * 1.5;


                const y =
                    2 +
                    row * 3;


                window.position.set(
                    x,
                    y,
                    3.01
                );


                group.add(window);
            }
        }
    }


    getHeight(building) {

        const activity =
            Math.max(
                0,
                Math.min(
                    1,
                    building.activity ?? 0
                )
            );


        return 6 + activity * 24;
    }


    getColor(building) {

        switch (
        building.building_type
        ) {

            case "network":
                return 0x286f82;

            case "commercial":
                return 0x3d6fa3;

            case "industrial":
                return 0x8a572c;

            case "warehouse":
                return 0x666666;

            case "infrastructure":
                return 0x8b3f3f;

            case "temporary":
                return 0x684080;

            default:
                return 0x4c5f7a;
        }
    }


    update(building) {

        const group =
            this.buildings.get(
                building.id
            );


        if (!group) {
            return this.create(building);
        }


        const position =
            cityToThree(
                building.position
            );


        group.position.set(
            position.x,
            position.y,
            position.z
        );


        const height =
            this.getHeight(building);


        const body =
            group.children[0];


        if (body) {

            body.scale.y =
                height /
                body.geometry.parameters.height;

            body.position.y =
                height / 2;
        }
    }


    remove(id) {

        const building =
            this.buildings.get(id);


        if (!building) {
            return;
        }


        building.traverse(
            object => {

                if (object.geometry) {
                    object.geometry.dispose();
                }

                if (object.material) {
                    object.material.dispose();
                }

            }
        );


        building.removeFromParent();

        this.buildings.delete(id);
    }
}