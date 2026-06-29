const datasets = [
  {
    id: "random_interfaces_n256_to_n64_interface_patches_v2",
    title: "Random VOF Interface Patches: N256 to N64",
    summary:
      "AI-ready 3D VOF patch dataset generated from randomized analytic interfaces initialized in NGA2, paired between high-resolution N256 fields and low-resolution N64 volume averages.",
    status: "seed",
    modality: "simulation",
    physics: ["VOF", "two-phase flow", "random interfaces", "periodic box"],
    tasks: ["super-resolution", "closure modeling", "interface reconstruction"],
    samples: "362,264 patches",
    resolution: "HR 16^3 patch, LR 4^3 patch",
    format: "NPZ + JSON metadata",
    license: "TBD before release",
    detailUrl: "dataset-random-vof-patches.html",
    metadataUrl: "../datasets/random_interfaces_n256_to_n64_interface_patches_v2.json"
  }
];

const grid = document.querySelector("#dataset-grid");
const search = document.querySelector("#dataset-search");
const count = document.querySelector("#dataset-count");

function render(items) {
  if (count) {
    count.textContent = String(datasets.length);
  }

  grid.innerHTML = items
    .map(
      (dataset) => `
      <article class="dataset-card">
        <div>
          <p class="eyebrow">${dataset.status} dataset</p>
          <h3>${dataset.title}</h3>
          <p>${dataset.summary}</p>
        </div>
        <div class="tags">
          ${[...dataset.physics, ...dataset.tasks].map((tag) => `<span class="tag">${tag}</span>`).join("")}
        </div>
        <div class="meta">
          <span><strong>Samples</strong>${dataset.samples}</span>
          <span><strong>Resolution</strong>${dataset.resolution}</span>
          <span><strong>Format</strong>${dataset.format}</span>
          <span><strong>License</strong>${dataset.license}</span>
        </div>
        <div class="card-actions">
          <a href="${dataset.detailUrl}">Dataset page</a>
          <a href="${dataset.metadataUrl}">Metadata JSON</a>
        </div>
      </article>
    `
    )
    .join("");
}

if (grid && search) {
  search.addEventListener("input", (event) => {
    const query = event.target.value.toLowerCase().trim();
    const filtered = datasets.filter((dataset) =>
      JSON.stringify(dataset).toLowerCase().includes(query)
    );
    render(filtered);
  });

  render(datasets);
}
