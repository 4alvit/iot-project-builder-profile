# Profile preview

The README hero is a browser capture of the existing public `docs/index.html`
report, dated **28 September 2026**. It demonstrates the generator's HTML
output. Its counts, assessments and descriptions are historical generated
results, not independently verified current capabilities or release status.
The report itself is unchanged.

The original [`iot-profile-report.jpg`](iot-profile-report.jpg) is preserved.
The renderer includes its complete heading, summary and overview and omits the
partially visible next section. It applies perspective, rounded outer corners,
a neutral background and a soft shadow; it does not redraw text or values.

## Capture and regenerate

Serve the existing report locally:

```sh
python3 -m http.server 18480 --bind 127.0.0.1 --directory docs
```

Open `http://127.0.0.1:18480/` in a browser, wait for the report to render, and
capture its top at a 1280-pixel width. The checked-in browser JPEG is
1280 × 1260; its SHA-256 and source commit are recorded in
[capture-provenance.json](capture-provenance.json). Review a new capture for
private repository names or personal information before committing it. The
page's existing charts use the Plotly CDN; this preview adds no external script.

Install ImageMagick 7, then regenerate the hero from the repository root:

```sh
./scripts/render-docs-hero.sh
```

The script verifies the source dimensions before cropping the first 1090 rows.
Update the crop, provenance and caption when replacing the source. Click the
README image for the original flat screenshot and follow the published-profile
link for the complete report.
