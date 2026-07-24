 #!/usr/bin/env python3
 """Generate website/datasets.js from datasets/*.json catalogue records.
 
 Run this script whenever you add or update a JSON record in datasets/.
 """
 
 from __future__ import annotations
 
 import json
 from pathlib import Path
 
 ROOT = Path(__file__).resolve().parents[1]
 DATASETS_DIR = ROOT / "datasets"
 OUTPUT = ROOT / "website" / "datasets.js"
 
 
 def build_entry(record: dict) -> dict:
     data = record.get("data", {})
     domain = record.get("domain", {})
     visuals = record.get("visuals", {})
     license_info = record.get("license", {})
 
     physics: list[str] = []
     if domain.get("flow_type"):
         physics.append(domain["flow_type"].replace("_", " "))
     if domain.get("interface_method"):
         physics.append(domain["interface_method"])
     if domain.get("configuration"):
         physics.append(domain["configuration"])
 
     tasks = record.get("tasks") or ["interface dynamics", "flow-field learning"]
 
     snapshots = data.get("snapshot_selection", {}).get("selected_snapshots", "?")
     samples = f"{snapshots} snapshots"
 
     cell_shape = data.get("grid", {}).get("cell_shape", [])
     if cell_shape:
         resolution = f"{cell_shape[0]}^{len(cell_shape)} cells"
     else:
         resolution = "unknown"
 
     image = visuals.get("main", "assets/placeholder.png")
    if image.startswith('website/'):
        image = image[len('website/'):]
 
     data_url = (
         data.get("modelscope_url")
         or data.get("kaggle_url")
         or data.get("zenodo_url")
         or data.get("repository_url")
         or "#"
     )
 
     return {
         "id": record.get("id", ""),
         "title": record.get("title", ""),
         "summary": record.get("description", ""),
         "status": record.get("status", "seed").replace("_dataset", ""),
         "modality": record.get("modality", "simulation"),
         "physics": physics,
         "tasks": tasks,
         "samples": samples,
         "resolution": resolution,
         "format": data.get("format", "unknown"),
         "license": license_info.get("data_license", "TBD"),
         "imageUrl": image,
         "dataUrl": data_url,
         "detailUrl": f"dataset-{record.get('id', 'unknown')}.html",
     }
 
 
 def main() -> int:
     if not DATASETS_DIR.exists():
         print("datasets/ directory not found, skipping")
         return 1
 
     json_files = sorted(DATASETS_DIR.glob("*.json"))
     if not json_files:
         print("No dataset JSON files found, skipping")
         return 0
 
     entries = []
     for path in json_files:
         try:
             record = json.loads(path.read_text(encoding="utf-8"))
             entries.append(build_entry(record))
         except (json.JSONDecodeError, KeyError) as exc:
             print(f"Warning: skipping {path.name}: {exc}")
 
     header = "// Auto-generated from datasets/*.json â€?do not edit manually.\n"
     data_block = f"const datasets = {json.dumps(entries, indent=2, ensure_ascii=False)};\n\n"
 
     render_logic = """\
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
         (dataset) => `
         <article class="dataset-tile">
           <a href="${dataset.detailUrl}" aria-label="${dataset.title}">
             <img src="${dataset.imageUrl}" alt="${dataset.title}" />
             <span>${dataset.title}</span>
           </a>
         </article>
       `
       )
       .join("");
     return;
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
           <a href="${dataset.dataUrl}">ModelScope</a>
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
 """
 
     OUTPUT.write_text(header + data_block + render_logic, encoding="utf-8")
     print(f"Generated {OUTPUT} with {len(entries)} dataset(s)")
     return 0
 
 
 if __name__ == "__main__":
     raise SystemExit(main())
