import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

import { BuildingRenderer }
  from "./city/BuildingRenderer.js";

import { cityToThree }
  from "./city/coordinates.js";

import "./style.css";


class CityRenderer {

  constructor() {

    this.scene =
      new THREE.Scene();


    this.scene.background =
      new THREE.Color(
        0x101218
      );


    // -----------------------------
    // Camera
    // -----------------------------

    this.camera =
      new THREE.PerspectiveCamera(
        60,
        window.innerWidth /
        window.innerHeight,
        0.1,
        5000
      );


    this.camera.position.set(
      180,
      180,
      180
    );


    // -----------------------------
    // Renderer
    // -----------------------------

    this.renderer =
      new THREE.WebGLRenderer({
        antialias: true
      });


    this.renderer.setPixelRatio(
      window.devicePixelRatio
    );


    this.renderer.setSize(
      window.innerWidth,
      window.innerHeight
    );


    document.body.appendChild(
      this.renderer.domElement
    );


    // -----------------------------
    // Camera controls
    // -----------------------------

    this.controls =
      new OrbitControls(
        this.camera,
        this.renderer.domElement
      );


    this.controls.enableDamping = true;


    this.controls.target.set(
      100,
      0,
      100
    );


    // -----------------------------
    // City root
    // -----------------------------

    this.cityRoot =
      new THREE.Group();


    this.scene.add(
      this.cityRoot
    );


    // -----------------------------
    // Renderer groups
    // -----------------------------

    this.blockRoot =
      new THREE.Group();

    this.roadRoot =
      new THREE.Group();

    this.intersectionRoot =
      new THREE.Group();

    this.cityRoot.add(
      this.blockRoot
    );

    this.cityRoot.add(
      this.roadRoot
    );

    this.cityRoot.add(
      this.intersectionRoot
    );


    // -----------------------------
    // Building renderer
    // -----------------------------

    this.buildingRenderer =
      new BuildingRenderer(
        this.cityRoot
      );


    this.setupLights();


    window.addEventListener(
      "resize",
      () => this.onResize()
    );
  }


  setupLights() {

    const ambient =
      new THREE.HemisphereLight(
        0xffffff,
        0x202020,
        2
      );


    this.scene.add(
      ambient
    );


    const directional =
      new THREE.DirectionalLight(
        0xffffff,
        2
      );


    directional.position.set(
      100,
      200,
      100
    );


    this.scene.add(
      directional
    );
  }


  async loadCity(url) {

    const response =
      await fetch(url);


    if (!response.ok) {

      throw new Error(
        `Failed to load city: ${response.status}`
      );
    }


    const city =
      await response.json();


    console.log(
      "City loaded:",
      city
    );


    this.renderCity(
      city
    );
  }


  renderCity(city) {

    console.log(
      "Blocks:",
      city.blocks.length
    );

    console.log(
      "Intersections:",
      city.intersections.length
    );

    console.log(
      "Roads:",
      city.roads.length
    );

    console.log(
      "Nodes:",
      city.nodes.length
    );


    this.renderGround(
      city
    );

    this.renderBlocks(
      city
    );

    this.renderIntersections(
      city
    );

    this.renderRoads(
      city
    );

    this.renderNodes(
      city
    );
  }


  renderGround(city) {

    const geometry =
      new THREE.PlaneGeometry(
        1000,
        1000
      );


    const material =
      new THREE.MeshStandardMaterial({
        color: 0x181a1f
      });


    const ground =
      new THREE.Mesh(
        geometry,
        material
      );


    ground.rotation.x =
      -Math.PI / 2;


    ground.position.y =
      -0.05;


    this.cityRoot.add(
      ground
    );
  }


  renderBlocks(city) {

    for (
      const block of city.blocks
    ) {

      const [
        x,
        y
      ] = block.position;


      const [
        width,
        depth
      ] = block.size;


      const geometry =
        new THREE.BoxGeometry(
          width,
          0.5,
          depth
        );


      const material =
        new THREE.MeshStandardMaterial({
          color: 0x30332f
        });


      const mesh =
        new THREE.Mesh(
          geometry,
          material
        );


      mesh.position.set(
        x,
        0,
        y
      );


      this.blockRoot.add(
        mesh
      );
    }
  }


  renderIntersections(city) {

    for (
      const intersection
      of city.intersections
    ) {

      const [
        x,
        y
      ] = intersection.position;


      const geometry =
        new THREE.BoxGeometry(
          3,
          0.2,
          3
        );


      const material =
        new THREE.MeshStandardMaterial({
          color: 0xffaa00
        });


      const mesh =
        new THREE.Mesh(
          geometry,
          material
        );


      mesh.position.set(
        x,
        0.35,
        y
      );


      this.intersectionRoot.add(
        mesh
      );
    }
  }


  renderRoads(city) {

    const intersections =
      new Map();


    for (
      const intersection
      of city.intersections
    ) {

      intersections.set(
        intersection.id,
        intersection
      );
    }


    for (
      const road of city.roads
    ) {

      if (
        !road.metadata ||
        !road.metadata.physical
      ) {
        continue;
      }


      const source =
        intersections.get(
          road.source_id
        );


      const destination =
        intersections.get(
          road.destination_id
        );


      if (
        !source ||
        !destination
      ) {
        continue;
      }


      const [
        sx,
        sy
      ] = source.position;


      const [
        dx,
        dy
      ] = destination.position;


      const centerX =
        (sx + dx) / 2;


      const centerY =
        (sy + dy) / 2;


      const length =
        Math.sqrt(
          Math.pow(
            dx - sx,
            2
          ) +
          Math.pow(
            dy - sy,
            2
          )
        );


      const geometry =
        new THREE.BoxGeometry(
          length,
          0.15,
          6
        );


      const material =
        new THREE.MeshStandardMaterial({
          color: 0x111216
        });


      const mesh =
        new THREE.Mesh(
          geometry,
          material
        );


      mesh.position.set(
        centerX,
        0.2,
        centerY
      );


      const angle =
        Math.atan2(
          dy - sy,
          dx - sx
        );


      mesh.rotation.y =
        -angle;


      this.roadRoot.add(
        mesh
      );
    }
  }


  renderNodes(city) {

    for (
      const node of city.nodes
    ) {

      if (!node.active) {
        continue;
      }


      if (
        node.render_type ===
        "building"
      ) {

        this.buildingRenderer.create(
          node
        );

        continue;
      }


      this.renderGenericNode(
        node
      );
    }
  }


  renderGenericNode(node) {

    const position =
      cityToThree(
        node.position
      );


    const height =
      node.render_type ===
        "infrastructure"
        ? 8 +
        node.utilization * 20
        : 5;


    const geometry =
      new THREE.BoxGeometry(
        6,
        height,
        6
      );


    const material =
      new THREE.MeshStandardMaterial({
        color:
          this.getNodeColor(
            node
          )
      });


    const mesh =
      new THREE.Mesh(
        geometry,
        material
      );


    mesh.position.set(
      position.x,
      height / 2,
      position.z
    );


    this.cityRoot.add(
      mesh
    );
  }


  getNodeColor(node) {

    switch (
    node.render_type
    ) {

      case "infrastructure":
        return 0xb54b4b;

      case "external":
        return 0x4caf50;

      default:
        return 0x888888;
    }
  }


  onResize() {

    this.camera.aspect =
      window.innerWidth /
      window.innerHeight;


    this.camera.updateProjectionMatrix();


    this.renderer.setSize(
      window.innerWidth,
      window.innerHeight
    );
  }


  animate() {

    requestAnimationFrame(
      () => this.animate()
    );


    this.controls.update();


    this.renderer.render(
      this.scene,
      this.camera
    );
  }
}


async function main() {

  const city =
    new CityRenderer();


  await city.loadCity(
    "/city.json"
  );


  city.animate();
}


main().catch(error => {

  console.error(error);


  document.body.innerHTML = `
        <pre style="
            color: white;
            padding: 20px;
            font-family: monospace;
        ">
${error.stack || error}
        </pre>
    `;
});