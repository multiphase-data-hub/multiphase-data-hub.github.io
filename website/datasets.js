// Auto-generated from datasets/*.json
// Regenerate with: python scripts/generate_datasets_js.py
const datasets = [{"id":"dns_droplet_breakup_hit_we15","physics":["two phase flow","VOF","droplet breakup in homogeneous isotropic turbulence"],"license":"CC-BY-4.0","dataUrl":"https://modelscope.cn/datasets/yangqianqi/dns-droplet-breakup-hit-we15","samples":"81 snapshots","title":"Droplet breakup in HIT","modality":"simulation","format":"custom binary","detailUrl":"dataset-dns_droplet_breakup_hit_we15.html","status":"seed","summary":"Direct numerical simulation data of a liquid droplet breaking up in forced homogeneous isotropic turbulence at Weber number 15. The dataset provides volume-fraction, pressure, and velocity fields over 81 snapshots.","imageUrl":"assets/hit_droplet_breakup_3d.png","resolution":"256^3 cells","tasks":["interface dynamics","flow-field learning"]},{"id":"test_submit_dataset","physics":["two phase flow","VOF","droplet breakup in homogeneous isotropic turbulence"],"license":"CC-BY-4.0","dataUrl":"https://modelscope.cn/datasets/yangqianqi/dns-droplet-breakup-hit-we15","samples":"81 snapshots","title":"Droplet breakup in HIT","modality":"simulation","format":"custom binary","detailUrl":"dataset-test_submit_dataset.html","status":"seed","summary":"Direct numerical simulation data of a liquid droplet breaking up in forced homogeneous isotropic turbulence at Weber number 15. The dataset provides volume-fraction, pressure, and velocity fields over 81 snapshots.","imageUrl":"assets/hit_droplet_breakup_3d.png","resolution":"256^3 cells","tasks":["interface dynamics","flow-field learning"]}]
;

const grid = document.querySelector("#dataset-grid");
const search = document.querySelector("#dataset-search");
const count = document.querySelector("#dataset-count");

function render(items) {
  if (count) {
    count.textContent = String(datasets.length);
  }

  if (grid.dataset.layout === "gallery") {
    grid.innerHTML = items
      .map(
        (dataset) => ` + '"`' + @'
        <article class="dataset-tile">
          <a href="${dataset.detailUrl}" aria-label="${dataset.title}">
            <img src="${dataset.imageUrl}" alt="${dataset.title}" />
            <span>${dataset.title}</span>
          </a>
        </article>
      ` + '"`' + @'
      )
      .join("");
    return;
  }

  grid.innerHTML = items
    .map(
      (dataset) => ` + '"`' + @'
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
          <a href="${dataset.dataUrl}">ModelScope</a>
        </div>
      </article>
    ` + '"`' + @'
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